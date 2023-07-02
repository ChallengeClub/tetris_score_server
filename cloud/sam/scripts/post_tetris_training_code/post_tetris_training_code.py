import boto3
import os
import subprocess
import json
import glob

frontend_origin = os.environ["FRONTEND_ORIGIN"]
BUCKET_NAME = os.environ["TETRIS_TRAINING_BUCKET_NAME"]

s3 = boto3.resource('s3')

def lambda_handler(event: dict, context):
    section = event['pathParameters']['section']
    if section.startWith("tetris"):
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
                'Access-Control-Allow-Origin': frontend_origin,
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
                'Access-Control-Allow-Origin': frontend_origin,
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
        proc = subprocess.Popen(["python", python_file_path], text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            outs, errs = proc.communicate(input=input_text.decode('utf-8')+"\n", timeout=1)
        except subprocess.TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        expected_outs = output_text.decode('utf-8') + "\n"
        results.append("AC" if expected_outs==outs else "WA")
        
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
                'Access-Control-Allow-Origin': frontend_origin,
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
                'Access-Control-Allow-Origin': frontend_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            "body": "could not read output object",
        }
        return response
    
    with open("tmp/block_controller.py" , mode='w') as f:
        f.write(event["body"])
    
    results = []
    for input_json, output_json in zip(input_jsons, output_jsons):
        proc = subprocess.Popen(["python", "tetris/game_manager.py"], text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            input_text = input_json["block_list"] + "\n" + input_json["initial_board"] + "\n"
            outs, errs = proc.communicate(input=input_text.decode('utf-8'), timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        expected_outs = output_json.decode('utf-8') + "\n"
        results.append("AC" if expected_outs==outs else "WA")

    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': frontend_origin,
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        "body": json.dumps(results),
    }
    return response