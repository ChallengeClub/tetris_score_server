import boto3
import os
import subprocess
import json
import glob

FRONTEND_ORIGIN = os.environ["FRONTEND_ORIGIN"]
BUCKET_NAME = os.environ["TURTLE_TRAINING_BUCKET_NAME"]
LAMBDA_TASK_ROOT = os.environ["LAMBDA_TASK_ROOT"]
SUBPROCESS_TIMEOUT_LIMIT = 3


def lambda_handler(event: dict, context):
    section = event['pathParameters']['section']
    response = evaluation(event, context)
    
    for p in glob.glob("/tmp/*"):
       if os.path.isfile(p):
           os.remove(p)
           
    return response


def evaluation(event: dict, context):
    section = event['pathParameters']['section']
    id = event['pathParameters']['id']

    python_file_path = "/tmp/main.py"
    with open(python_file_path , mode='w') as f:
        f.write(event["body"])
    
    try:
        proc = subprocess.run(["xvfb-run", "-a", "python", python_file_path], capture_output=True, timeout=SUBPROCESS_TIMEOUT_LIMIT, check=True)
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/plain",
            },
            "isBase64Encoded": True,
            "body": open('/tmp/canvas.svg', 'rb').read().encode('base64')
        }
    except subprocess.TimeoutExpired:
        response = {
            "statusCode": 400,
            "body": "Time expired error",
            "headers": {
                "Content-Type": "text/plain",
            },
        }
    except subprocess.CalledProcessError:
        response = {
            "statusCode": 400,
            "body": "Runtime error",
            "headers": {
                "Content-Type": "text/plain",
            },
        }

    for f in os.listdir("/tmp"):
        os.remove(os.path.join(dir, f))

    return response

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
        except subprocess.CalledProcessError as e:
            results.append("RE")
            print("Stdout:", e.stdout)
            print("Error message:", e.stderr)
    
    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': FRONTEND_ORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        "body": json.dumps(results),
    }
    return response