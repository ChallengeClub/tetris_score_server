import boto3
import os
import subprocess
import json
import glob

FRONTEND_ORIGIN = os.environ["FRONTEND_ORIGIN"]
BUCKET_NAME = os.environ["TETRIS_TRAINING_BUCKET_NAME"]
LAMBDA_TASK_ROOT = os.environ["LAMBDA_TASK_ROOT"]
SUBPROCESS_TIMEOUT_LIMIT = 30

s3 = boto3.resource('s3')

def lambda_handler(event: dict, context):
    response = evaluation(event, context)
    
    for p in glob.glob("/tmp/*"):
       if os.path.isfile(p):
           os.remove(p)
           
    return response


def evaluation(event: dict, context):
    bucket = s3.Bucket(BUCKET_NAME)

    section = "algorithm"
    id = event['pathParameters']['id']

    try:
        input_obj = bucket.Object(f"{section}/{id}/input.txt")
        input_generator = input_obj.get()['Body'].iter_lines()
    except Exception as e:
        response = {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': FRONTEND_ORIGIN,
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            "body": "could not find input object",
        }
        return response
    try:
        output_obj = bucket.Object(f"{section}/{id}/output.txt")
        output_generator = output_obj.get()['Body'].iter_lines()
    except Exception as e:
        response = {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': FRONTEND_ORIGIN,
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            "body": "could not find output object",
        }
        return response
    python_file_path = "/tmp/main.py"
    with open(python_file_path , mode='w') as f:
        f.write(event["body"])
    
    results = []
    for input_text, output_text in zip(input_generator, output_generator):
        try:
            proc = subprocess.run(["python", python_file_path], input=input_text+b"\n", capture_output=True, timeout=SUBPROCESS_TIMEOUT_LIMIT, check=True)
            expected_outs = output_text + b"\n"
            results.append("AC" if expected_outs==proc.stdout else "WA")
        except subprocess.TimeoutExpired:
            results.append("TLE")
        except subprocess.CalledProcessError:
            results.append("RE")
        
    if os.path.exists(python_file_path):
        os.remove(python_file_path)

    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': FRONTEND_ORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        "body": json.dumps(results),
    }
    return response
