import boto3
import os

table_name = os.environ["DYNAMODB_TABLE_NAME"]
frontend_origin = os.environ["FRONTEND_ORIGIN"]

def lambda_handler(event: dict, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    id = event['pathParameters']['id']
    try:
        _res = table.get_item(
            Key={
                'Id': id,
            },
            AttributesToGet=[
                'Status',
            ],
        )
    except Exception as e:
        response = {
            "statusCode": 500,
            'headers': {
                'Access-Control-Allow-Origin': frontend_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            "body": "failed to get item from dynamodb: " + str(e),
        }
        return response
    
    status = _res.get("Status", "")
    if not status:
        response = {
            "statusCode": 404,
            'headers': {
                'Access-Control-Allow-Origin': frontend_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            "body": "No such record, id: " + id,
        }
        return response
    
    if status not in ("evaluating", "waiting"):
        response = {
            "statusCode": 204,
            'headers': {
                'Access-Control-Allow-Origin': frontend_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            "body": "stop request was rejected, current status was " + status,
        }
        return response

    try:
        response = table.update_item(
            Key = {
                "Id": id
            },
            UpdateExpression='set \
                #Status = :status \
                ',
            ExpressionAttributeNames= {
                '#Status' : 'Status',
		    },
            ExpressionAttributeValues={
                ':status' : 'stopping',
            },
        )

    except Exception as e:
        response = {
            "statusCode": 500,
            'headers': {
                'Access-Control-Allow-Origin': frontend_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            "body": "failed to update item on dynamodb: " + str(e),
        }
    return response
