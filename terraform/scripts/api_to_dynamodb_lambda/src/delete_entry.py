import boto3
import os

table_name = os.environ["dynamodb_competition_table_name"]

def lambda_handler(event: dict, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        response = table.delete_item(
            Key = {
                "RepositoryURL": event["body"]["repository_url"],
                "Level": event["body"]["level"]
            }
        )
    except Exception as e:
        response = {
            "error": {
                "message": "failed to delete item: " + str(e),
                "body": event,
                "type": "dynamodb access exception",
            },
            "code": 501
        }
    return response
