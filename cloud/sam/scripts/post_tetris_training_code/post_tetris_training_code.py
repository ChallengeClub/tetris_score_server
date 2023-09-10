import boto3
import os
import subprocess
import json
import glob

FRONTEND_ORIGIN = os.environ["FRONTEND_ORIGIN"]
BUCKET_NAME = os.environ["TETRIS_TRAINING_BUCKET_NAME"]
SUBPROCESS_TIMEOUT_LIMIT = 30

s3 = boto3.resource('s3')

def lambda_handler(event: dict, context):
    section = event['pathParameters']['section']
    if section.startswith("tetris"):
        response = tetris_evaluation(event, context)
    else:
        response = evaluation(event, context)
    
    for p in glob.glob("/tmp/*"):
       if os.path.isfile(p):
           os.remove(p)
           
    return response


def evaluation(event: dict, context):
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
        except subprocess.CalledProcessError as e:
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

def tetris_evaluation(event, context):
    bucket = s3.Bucket(BUCKET_NAME)

    section = event['pathParameters']['section']
    id = event['pathParameters']['id']

    try:
        input_obj = bucket.Object(f"{section}/{id}/input.json")
        input_jsons = json.loads(input_obj.get()['Body'].read())
    except Exception as e:
        response = {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': FRONTEND_ORIGIN,
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            "body": "could not read input object",
        }
        return response
    try:
        output_obj = bucket.Object(f"{section}/{id}/output.json")
        output_jsons = json.loads(output_obj.get()['Body'].read())
    except Exception as e:
        response = {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': FRONTEND_ORIGIN,
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            "body": "could not read output object",
        }
        return response
    
    with open("/tmp/block_controller.py" , mode='w') as f:
        f.write(event["body"])
    
    results = []
    for input_json, output_json in zip(input_jsons, output_jsons):
        try:
            input_text = ",".join(map(str, input_json["block_list"])) + "\n" + ",".join(map(str, input_json["initial_board"])) + "\n"
            proc = subprocess.run(["python", "tetris/game_manager.py"],text=True, input=input_text, capture_output=True, timeout=SUBPROCESS_TIMEOUT_LIMIT, check=True)
            expected_outs = ",".join(map(str, output_json["output"])) + "\n"
            results.append("AC" if expected_outs==proc.stdout else "WA")
        except subprocess.TimeoutExpired:
            results.append("TLE")
        except subprocess.CalledProcessError:
            results.append("RE")
    
    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': FRONTEND_ORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        "body": json.dumps(results),
    }
    return response