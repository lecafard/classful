import boto3
import uuid
from time import time

TABLE = "classful-testing-pending"
EXPIRES = 86400 * 8

dynamo = boto3.resource('dynamodb')

def add_to_db(email, classes):
    with dynamo.Table(TABLE).batch_writer() as batch:
        for i in classes:
            batch.put_item(
                Item={
                    "id": str(uuid.uuid4()),
                    "email": email,
                    "class": i,
                    "expires": int(time()) + EXPIRES
                }
            )