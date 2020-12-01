import boto3
import datetime
import os

STACK_NAME = os.getenv("STACK_NAME", "classful-dev")
CLEANUP_MONTHS_THRESHOLD = int(os.getenv("CLEANUP_MONTHS_THRESHOLD", 2))
client = boto3.client("logs")

def lambda_handler(event, context):

    today = datetime.date.today()
    
    month = today.month - CLEANUP_MONTHS_THRESHOLD
    year = today.year

    if month < 1:
        year -= 1
        month += 12
    
    prefix = f"{year}/{month:02}"

    groups = list(map(
        lambda x: x["logGroupName"],
        client.describe_log_groups(
            logGroupNamePrefix=f"/aws/lambda/{STACK_NAME}"
        )["logGroups"]
    ))

    for g in groups:
        streams = list(map(
            lambda x: x["logStreamName"],
            client.describe_log_streams(
                logGroupName=g,
                logStreamNamePrefix=prefix
            )["logStreams"]
        ))
        for s in streams:
            print(f"Deleting group={repr(g)} stream={repr(s)}")
            client.delete_log_stream(logGroupName=g, logStreamName=s)

    client.describe_log_groups(logGroupNamePrefix=f"/aws/lambda/{STACK_NAME}")
