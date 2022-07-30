import boto3
import json

def lambda_handler(event: dict, context):
    client = boto3.client("sqs")
    response = client.send_message(
        QueueUrl="https://sqs.ap-northeast-1.amazonaws.com/086656038367/score-evaluation-queue",
        MessageBody=json.dumps(event)
    )
    return response