import boto3
import os

table_name = os.environ["DYNAMODB_COMPETITION_TABLE_NAME"]

def lambda_handler(event: dict, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        response = table.scan( 
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