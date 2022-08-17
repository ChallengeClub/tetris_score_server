import boto3
import os
import base64
from score_evaluation_message_pb2 import ScoreEvaluationMessage

sqs_url = os.environ["SQS_URL"]

def lambda_handler(event: dict, context):
    client = boto3.client("sqs")
    msg = ScoreEvaluationMessage()
    data = base64.b64decode(event["body"].encode('utf-8'))
    try:
        msg.ParseFromString(data)
    except:
        response = {
            "error": {
                "message": "including invalid fields in request",
                "body": event["body"],
                "type": "ProtobufException",
                "code": 501
            }            
        }
        return response
        
    message = str(msg.SerializeToString())
    try:
        response = client.send_message(
            QueueUrl=sqs_url,
            MessageBody=message
        )
        response = {
                "message": "successfully sent message to SQS",
                "body": response,
                "code": 200
        }
    except:
        response = {
            "error": {
                "message": "failed to send message to SQS",
                "body": message,
                "type": "SQSClientError",
                "code": 501
            }            
        }
    return response