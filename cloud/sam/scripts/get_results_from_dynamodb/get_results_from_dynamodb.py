import boto3
import os
import json
import decimal

table_name = os.environ["DYNAMODB_TABLE_NAME"]

def lambda_handler(event: dict, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        _res = table.scan(
            Limit=200,  
        )
        response = {
            "statusCode": 200,
            "body": json.dumps(_res["Items"], default=lambda x : float(x) if isinstance(x, decimal.Decimal) else TypeError)
        }
    except Exception as e:
        response = {
            "statusCode": 501,
            "body": "failed to scan dynamodb: " + str(e),
        }
    return response
