import boto3
import os

table_name = os.environ["dynamodb_table_name"]

def lambda_handler(event: dict, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        response = table.scan(
            IndexName="CreatedAt",
            Limit=30,            
        )
    except:
        response = {
            "error": {
                "message": "failed to scan dynamodb",
                "body": event["body"],
                "type": "dynamodb access exception",
            },
            "code": 501
        }
    return response
        