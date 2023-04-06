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
            "statusCode": 401,
            "body": "ProtobufException: failed to parse request" + str(e)
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
        _res = table.put_item(
            Item = item
        )
        response = {
            "body": "successfully registered competition entry to DynamoDB",
            "statusCode": 200
        }
    except Exception as e:
        response = {
            "body": "failed to register competition entry to dynamodb, " + str(e),
            "statusCode": 500
        }
          
    return response