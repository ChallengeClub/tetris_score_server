import boto3
import os
from time import time
from uuid import uuid4
import base64
from score_evaluation_message_pb2 import ScoreEvaluationMessage

sqs_url = os.environ["SQS_URL"]
dynamodb_table_name = os.environ["DYNAMODB_TABLE_NAME"]

def lambda_handler(event: dict, context):
    client = boto3.client("sqs")
    msg = ScoreEvaluationMessage()
    data = base64.b64decode(event["body"].encode('utf-8'))
    try:
        msg.ParseFromString(data)
    except:
        response = {
            "error": {
                "message": "failed to parse request",
                "body": event["body"],
                "type": "ProtobufException",
            },
            "code": 401
        }
        return response
    msg.id = str(uuid4()) # generate Id when register request to dynamodb
    msg.created_at = int(time())
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table_name)
    item = {
        "Id": msg.id, 
        "Name": msg.name,
        "CreatedAt": msg.created_at,
        "RepositoryURL": msg.repository_url,
        "Branch": msg.branch,
        "GameTime": msg.game_time,
        "Level": msg.level,
        "Status": "W",
        "DropInterval": msg.drop_interval,
        "GameMode": msg.game_mode,
        "ValuePredictWeight": msg.predict_weight_path,
        "TrialNum": msg.trial_num
        }
    try:
        response = table.put_item(
            Item = item
        )
    except:
        response = {
            "error": {
                "message": "failed to register request to dynamodb",
                "body": event["body"],
                "type": "DynamodbException",
            },
            "code": 500
        }
        return response
        
    message = str(base64.b64encode(msg.SerializeToString()))
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
    except Exception as e:
        response = {
            "error": {
                "message": "failed to send message to SQS",
                "body": e,
                "type": "SQSClientError",
            },
            "code": 501
        }
    return response