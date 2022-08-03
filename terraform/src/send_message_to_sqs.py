import boto3
import json
import os

sqs_url = os.environ["SQS_URL"]

def lambda_handler(event: dict, context):
    client = boto3.client("sqs")
    response = client.send_message(
        QueueUrl=sqs_url,
        MessageBody=json.dumps(event)
    )
    return response