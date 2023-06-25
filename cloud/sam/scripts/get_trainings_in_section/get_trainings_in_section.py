import boto3
from boto3.dynamodb.conditions import Key
import os
import json
import decimal

table_name = os.environ["DYNAMODB_TRAINIG_TABLE_NAME"]

def lambda_handler(event: dict, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        _res = table.query(
            IndexName = "TrainingSetionIndex",
            Select = 'ALL_PROJECTED_ATTRIBUTES',
            ScanIndexForward = False,
            KeyConditionExpression=Key('Section').eq(event["queryStringParameters"]["section"]),
        )

        body = {
            "Items": _res["Items"],
            "LastEvaluatedKey": _res.get("LastEvaluatedKey", ""),
        }

        response = {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': frontend_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            "body":  json.dumps(body, default=lambda x : float(x) if isinstance(x, decimal.Decimal) else TypeError)
        }
    except Exception as e:
        response = {
            "statusCode": 501,
            'headers': {
                'Access-Control-Allow-Origin': frontend_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            "body": "failed to scan dynamodb: " + str(e),
        }
    return response
