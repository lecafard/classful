import boto3
import json
import gzip
from httplib import send_response
from classutil import get_classutil, validate_class
from lambdarest import lambda_handler
from db import add_to_db

MAX_COURSES = 6

@lambda_handler.handle("get", path="/terms")
def get_terms(event):
    return send_response(list(get_classutil()['courses'].keys()))

@lambda_handler.handle("get", path="/terms/<string:term>")
def get_courses_by_term(event, term):
    data = get_classutil()
    if term not in data['courses']:
        return {"error": "NotFound"}, 404
    return send_response({i: data['courses'][term][i]['name'] for i in data['courses'][term]})

@lambda_handler.handle("get", path="/terms/<string:term>/<string:course>")
def get_course_by_term(event, term, course):
    data = get_classutil()
    if term not in data['courses'] or course not in data['courses'][term]:
        return {"error": "NotFound"}, 404
    return send_response(data['courses'][term][course])

@lambda_handler.handle("post", path="/submit")
def submit_notification(event):
    body = json.loads(event["body"])
    data = get_classutil()
    # todo: add recaptcha
    
    if len(body["classes"]) > MAX_COURSES:
        return {"error": "TooManyClasses"}, 400
    for i in body["classes"]:
        if not validate_class(data, i):
            return {"error": "InvalidClass"}, 400
    
    # commit to dynamodb
    add_to_db(body["email"], body["classes"])
    return send_response(True)