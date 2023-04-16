import boto3
import os
import json
import decimal

table_name = os.environ["DYNAMODB_TABLE_NAME"]
frontend_origin = os.environ["FRONTEND_ORIGIN"]

def lambda_handler(event: dict, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        if event["exclusive_start_key"]:
            _res = table.query(
                IndexName = "CreatedAtIndex",
                Select = 'ALL_PROJECTED_ATTRIBUTES',
                Limit = event["limit"],
                ScanIndexForward = False,
                ExclusiveStartKey = event["exclusive_start_key"],
                KeyConditionExpression=Key('Competition').eq(event["competition"]),
            )
        else:
            _res = table.query(
                IndexName = "CreatedAtIndex",
                Select = 'ALL_PROJECTED_ATTRIBUTES',
                Limit = event["limit"],
                ScanIndexForward = False,
                KeyConditionExpression=Key('Competition').eq(event["competition"]),
                Limit=event["limit"],  
            )

        response = {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': frontend_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            "body": json.dumps(_res["Items"], default=lambda x : float(x) if isinstance(x, decimal.Decimal) else TypeError)
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
