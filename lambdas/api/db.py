import boto3
import uuid
from time import time
import os

TABLE = os.getenv("DYNAMODB_TABLE", "classful-testing-pending")
EXPIRES = 86400 * 15

dynamo = boto3.resource('dynamodb')

def add_to_db(email, classes):
    dynamo.Table(TABLE).put_item(
        Item={
            "id": str(uuid.uuid4()),
            "email": email,
            "sections": ",".join(classes),
            "expires": int(time()) + EXPIRES
        }
    )
