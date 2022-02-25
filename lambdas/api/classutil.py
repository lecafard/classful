from http import HTTPStatus
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta, timezone, tzinfo
import json
import gzip
import re
import os

# reload classutil
CACHE_TIME = timedelta(minutes=10)
BUCKET = os.getenv("CLASSUTIL_BUCKET", "classful-data-testing")
FILENAME = "classutil.json.gz"
CLASS_REGEX = re.compile(r'^(\d{4}[STU][123])_([A-Z]{4}\d{4})_(\d{1,5})$')

s3 = boto3.resource('s3')

classutil_data = {}
classutil_etag = ""
classutil_expires = datetime(1970, 1, 1, tzinfo=timezone.utc)

# get classutil data,
def get_classutil():
    global classutil_etag
    global classutil_expires
    global classutil_data
    if datetime.now(timezone.utc) > classutil_expires:
        # fetch new classutil data
        obj = s3.Object(BUCKET, FILENAME)
        
        try:
            res = obj.get(IfNoneMatch=classutil_etag)
            classutil_data = convert_to_indexed(json.loads(gzip.decompress(res["Body"].read())))
            classutil_etag = res['ResponseMetadata']['HTTPHeaders']['etag']
            classutil_expires = datetime.now(timezone.utc) + CACHE_TIME
        except ClientError as ex:
            if ex.response['ResponseMetadata']['HTTPStatusCode'] == HTTPStatus.NOT_MODIFIED:
                classutil_expires = datetime.now(timezone.utc) + CACHE_TIME
            else:
                raise ex
    return classutil_data

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
        "courses": courses,
        "course_names": {
            term: {
                code: courses[term][code]["name"] for code in courses[term]
            } for term in courses
        }
    }

def validate_section(data, class_id):
    match = CLASS_REGEX.match(class_id)
    if not match:
        return False

    session_id = match.group(1)
    course_id = match.group(2)
    component_id = match.group(3)

    if (session_id not in data["courses"] or 
        course_id not in data["courses"][session_id] or
        component_id not in data["courses"][session_id][course_id]["components"]):
        return False
    
    return True
