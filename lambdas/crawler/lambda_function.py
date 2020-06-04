import boto3
import botocore
from classutil import scrape
import json
from time import time
import re
import gzip

BUCKET = "classful-data-testing"
KEY = "classutil.json.gz"
TABLE = "classful-testing-pending"

CLASS_REGEX = r"^(\d{4}[STU][123])_([A-Z]{4}\d{4})_(\d{1,5})$"

s3 = boto3.resource("s3")
dynamo = boto3.resource("dynamodb")
ses = boto3.client("ses")

def lambda_handler(event, context):
    last_updated = 0
    obj = s3.Object(BUCKET, KEY)
    try:
        current_data = json.loads(gzip.decompress(obj.get()["Body"].read()))
        last_updated = current_data["correct_at"]
    except botocore.exceptions.ClientError as e:
        if e.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            print("File {} does not currently exist in bucket {}, will create.".format(KEY, BUCKET))
        else:
            raise e
    except json.JSONDecodeError as e:
        # attempt to delete
        print("Invalid json in file {}, deleting".format(KEY))
        obj.delete()

    res = scrape(concurrency=8, last_updated=last_updated)
    data = convert_to_indexed(res)
    
    if res["correct_at"] != last_updated:
        obj.put(
            Body=gzip.compress(json.dumps(data).encode("utf-8"), compresslevel=9)
        )
        if last_updated != 0:
            send_notifications(data)
    else:
        print("Not updated, current version: {}".format(last_updated))

def convert_to_indexed(data):
    courses = {}
    for i in data["courses"]:
        session = "{}{}".format(i["year"], i["term"])
        if session not in courses:
            courses[session] = {}
        courses[session][i["code"]] = {
            "name": i["name"],
            "components": {str(j["id"]): {k: j[k] for k in j if k != "id"} for j in i["components"]}
        }
    return {
        "correct_at": data["correct_at"],
        "courses": courses
    }

def get_section_if_not_full(class_id, data):
    groups = re.search(CLASS_REGEX, class_id)
    if not groups:
        return False
    
    session_id = groups.group(1)
    course_id = groups.group(2)
    component_id = groups.group(3)

    if (session_id not in data["courses"] or 
        course_id not in data["courses"][session_id] or
        component_id not in data["courses"][session_id][course_id]["components"]):
        return False
    
    component = data["courses"][session_id][course_id]["components"][component_id]

    if component["filled"] < component["maximum"] and component["status"].startswith("Open"):
        return {"full_id": class_id, **component}
    
    return False


def send_notifications(data):
    # grab all from dynamodb
    # todo: in the unlikely event there is over 1MB of data in the row
    try:
        res = dynamo.Table(TABLE).scan()
    except botocore.exceptions.ClientError as e:
        print("Error with retrieving records from dynamodb")
        raise e

    # for each user
    # send email once we check preconditions
    for i in res["Items"]:
        found = []
        remain = []
        for s in i["sections"].split(","):
            section = get_section_if_not_full(s, data)
            if section:
                found.append(section)
            else:
                remain.append(s)

        if len(found) > 0:
            ses.send_email(
                Source="Classful <noreply@classful.tomn.me>",
                Destination={
                    "ToAddresses": [i["email"]]
                },
                Message={
                    "Subject": {
                        "Data": "Classful - A spot has opened up!"
                    },
                    "Body": {
                        "Text": {
                            "Data": "Hi,\n" + 
                                "{}\n\nare now open. ".format("\n".join("\t{} - {} {}".format(i["full_id"], i["cmp_type"], i["times"]) for i in found)) +
                                "Enrol quickly before someone else does."
                        }
                    }
                }
            )

        if len(remain) > 0:
            dynamo.Table(TABLE).update_item(
                Key={
                    "id": i["id"],
                },
                UpdateExpression="SET sections = :value",
                ExpressionAttributeValues={
                    ":value": ",".join(remain)
                }
            )
        else:
            dynamo.Table(TABLE).delete_item(
                Key={
                    "id": i["id"]
                }
            )