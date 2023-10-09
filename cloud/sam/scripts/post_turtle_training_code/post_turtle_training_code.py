import boto3
import os
import subprocess
import shutil
import base64

FRONTEND_ORIGIN = os.environ["FRONTEND_ORIGIN"]
LAMBDA_TASK_ROOT = os.environ["LAMBDA_TASK_ROOT"]
SUBPROCESS_TIMEOUT_LIMIT = 60


def lambda_handler(event: dict, context):
    response = evaluation(event, context)
    
    directory = "/tmp"
    _list = os.listdir(directory)
    for f in _list:
        l = os.path.join(directory, f)
        if os.path.isdir(l):
            shutil.rmtree(l)
        else:
            os.remove(l)
           
    return response

def evaluation(event: dict, context):
    python_file_path = "/tmp/main.py"
    with open(python_file_path , mode='w') as f:
        f.write(event["body"])
    
    try:
        proc = subprocess.run(["xvfb-run", "-a", "python", python_file_path], capture_output=True, timeout=SUBPROCESS_TIMEOUT_LIMIT, check=True)
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/jpeg",
            },
            "isBase64Encoded": True, 
            "body": base64.b64encode(open('/tmp/canvas.jpg', 'rb').read()).decode('utf-8')
        }
    except subprocess.TimeoutExpired:
        response = {
            "statusCode": 400,
            "body": "Time expired error",
            "headers": {
                "Content-Type": "text/plain",
            },
        }
    except subprocess.CalledProcessError as e:
        response = {
            "statusCode": 400,
            "body": f"Runtime error\n{e.stderr.decode('utf-8')}",
            "headers": {
                "Content-Type": "text/plain",
            },
        }

    return response
