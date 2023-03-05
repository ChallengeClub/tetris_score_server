import boto3
import os

table_name = os.environ["dynamodb_table_name"]

def lambda_handler(event: dict, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        response = table.scan(
            Limit=200,  
        )
    except Exception as e:
        response = {
            "error": {
                "message": "failed to scan dynamodb: " + str(e),
                "body": event,
                "type": "dynamodb access exception",
            },
            "code": 501
        }
    return response

def get_result_detail(event: dict, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(
            Key={
                'Id': event["body"]["id"],
            }
        )
    except Exception as e:
        response = {
            "error": {
                "message": "failed to scan dynamodb: " + str(e),
                "body": event,
                "type": "dynamodb access exception",
            },
            "code": 501
        }
    return response
