import boto3
import os
import subprocess
import json

frontend_origin = os.environ["FRONTEND_ORIGIN"]
BUCKET_NAME = os.environ["TETRIS_TRAINING_BUCKET_NAME"]

s3 = boto3.resource('s3')

def lambda_handler(event: dict, context):
    bucket = s3.Bucket(BUCKET_NAME)

    section = event['pathParameters']['section']
    id = event['pathParameters']['id']

    try:
        input_obj = bucket.Object(f"{section}/{id}/input.txt")
        input_generator = input_obj.get()['Body'].iter_lines()
    except Exception as e:
        response = {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': frontend_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            "body": "could not find input object",
        }
    try:
        output_obj = bucket.Object(f"{section}/{id}/output.txt")
        output_generator = output_obj.get()['Body'].iter_lines()
    except Exception as e:
        response = {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': frontend_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            "body": "could not find output object",
        }
    python_file_path = "/tmp/main.py"
    with open(python_file_path , mode='w') as f:
        f.write(event["body"])
    
    results = []
    for input_text, output_text in zip(input_generator, output_generator):
        proc = subprocess.Popen(["python", python_file_path], text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            outs, errs = proc.communicate(input=input_text.decode('utf-8')+"\n", timeout=1)
        except subprocess.TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        expected_outs = output_text.decode('utf-8') + "\n"
        
        results.append(expected_outs==outs)
        
    if os.path.exists(python_file_path):
        os.remove(python_file_path)

    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': frontend_origin,
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        "body": json.dumps(results),
    }
    return response