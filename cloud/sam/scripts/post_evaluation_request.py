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
    except Exception as e:
        response = {
            "statusCode": 401,
            "body": "ProtobufException: failed to parse message, " + str(e),
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
        "Status": "waiting",
        "DropInterval": msg.drop_interval,
        "GameMode": msg.game_mode,
        "ValuePredictWeight": msg.predict_weight_path,
        "TrialNum": msg.trial_num,
        "RandomSeeds": list(map(int, msg.random_seeds)),
    }
    try:
        response = table.put_item(
            Item = item
        )
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": "failed to register request to dynamodb, " + str(e),
        }
        return response
        
    message = str(base64.b64encode(msg.SerializeToString()))
    try:
        response = client.send_message(
            QueueUrl=sqs_url,
            MessageBody=message
        )
        response = {
            "statusCode": 200,
            "body": "successfully sent message to SQS",
        }
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": "failed to send message to SQS, " + str(e),
        }
    return response