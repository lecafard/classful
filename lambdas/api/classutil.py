from time import time
import boto3
import json
import gzip
import re
import os

# reload classutil
CACHE_TIME = 900
BUCKET = os.getenv("CLASSUTIL_BUCKET", "classful-data-testing")
FILENAME = "classutil.json.gz"
CLASS_REGEX = re.compile(r'^(\d{4}[STU][123])_([A-Z]{4}\d{4})_(\d{1,5})$')

s3 = boto3.resource('s3')

classutil_data = {}
classutil_expires = 0
# get classutil data,
def get_classutil():
    global classutil_expires
    global classutil_data
    if int(time()) > classutil_expires:
        # fetch new classutil data
        obj = s3.Object(BUCKET, FILENAME)
        classutil_data = json.loads(gzip.decompress(obj.get()["Body"].read()))
        classutil_expires = int(time()) + CACHE_TIME
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
