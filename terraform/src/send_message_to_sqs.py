import boto3
import os
from score_evaluation_message_pb2 import ScoreEvaluationMessage

sqs_url = os.environ["SQS_URL"]

def lambda_handler(event: dict, context):
    client = boto3.client("sqs")
    msg = ScoreEvaluationMessage()
    try:
        msg.ParseFromString(event.body)
        response = client.send_message(
            QueueUrl=sqs_url,
            MessageBody=event.body
        )
    except:
        response = {
            "error": {
                "message": "including invalid fields in request",
                "type": "ProtobufException",
                "code": 501
            }            
        }
    return response