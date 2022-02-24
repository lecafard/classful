from http import HTTPStatus
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta, timezone, tzinfo
import json
import gzip
import re
import os

# reload classutil
CACHE_TIME = timedelta(minutes=5)
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
            classutil_data = json.loads(gzip.decompress(res["Body"].read()))
            classutil_etag = res['ResponseMetadata']['HTTPHeaders']['etag']
            classutil_expires = datetime.now(timezone.utc) + CACHE_TIME
        except ClientError as ex:
            if ex.response['ResponseMetadata']['HTTPStatusCode'] == HTTPStatus.NOT_MODIFIED:
                classutil_expires = datetime.now(timezone.utc) + CACHE_TIME
            else:
                raise ex
    return classutil_data

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
