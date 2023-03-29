import boto3
import os
from time import time
import base64
from score_evaluation_message_pb2 import ScoreEvaluationMessage

dynamodb_table_name = os.environ["DYNAMODB_COMPETITION_TABLE_NAME"]


def lambda_handler(event: dict, context):
    msg = ScoreEvaluationMessage()
    data = base64.b64decode(event["body"].encode('utf-8'))
    try:
        msg.ParseFromString(data)
    except Exception as e:
        response = {
            "error": {
                "message": "failed to parse request",
                "body": str(e),
                "type": "ProtobufException",
            },
            "code": 401
        }
        return response
    msg.created_at = int(time())
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table_name)
    item = {
        "Name": msg.name,
        "CreatedAt": msg.created_at,
        "RepositoryURL": msg.repository_url,
        "Branch": msg.branch,
        "GameTime": msg.game_time,
        "Level": msg.level,
        "Status": "waiting",
        "GameMode": msg.game_mode,
        "ValuePredictWeight": msg.predict_weight_path
        }
    try:
        response = table.put_item(
            Item = item
        )
        response = {
                "message": "successfully registerd to DynamoDB",
                "body": response,
                "code": 200
        }
    except Exception as e:
        response = {
            "error": {
                "message": "failed to register request to dynamodb",
                "body": str(e),
                "type": "DynamodbException",
            },
            "code": 500
        }
          
    return response