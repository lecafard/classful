import boto3
import json
import gzip
from httplib import send_response, send_error
from classutil import get_classutil, validate_section
from lambdarest import lambda_handler
from db import add_to_db
import recaptcha

MAX_COURSES = 6

# do the get here to save some billing
get_classutil()

@lambda_handler.handle("get", path="/terms")
def get_terms(event):
    return send_response(list(get_classutil()['courses'].keys()))

@lambda_handler.handle("get", path="/terms/<string:term>")
def get_courses_by_term(event, term):
    data = get_classutil()
    if term not in data['course_names']:
        return send_error("NotFound", 404)
    return send_response(data['course_names'][term])

@lambda_handler.handle("get", path="/terms/<string:term>/<string:course>")
def get_course_by_term(event, term, course):
    data = get_classutil()
    if term not in data['courses'] or course not in data['courses'][term]:
        return send_error("NotFound", 404)
    return send_response(data['courses'][term][course])

@lambda_handler.handle("post", path="/submit")
def submit_notification(event):
    body = json.loads(event["body"])
    data = get_classutil()
    
    captcha = body["captcha"]
    ip = event["requestContext"]["identity"]["sourceIp"]
    if not recaptcha.verify(captcha, ip):
        return send_error("CaptchaFailed", 400)
    
    if len(body["sections"]) > MAX_COURSES:
        return send_error("TooManySections", 400)
    for i in body["sections"]:
        if not validate_section(data, i):
            return send_error("InvalidSection", 400)
    
    # commit to dynamodb
    add_to_db(body["email"], body["sections"])
    return send_response(True)