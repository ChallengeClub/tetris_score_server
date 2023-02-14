import base64
import boto3
import os

from ..domain.model.entity import Evaluation
from ..domain.repository.evaluation_message_repository import EvaluationMessageRepository
from ..domain.repository.evaluation_result_repository import EvaluationResultRepository

from ..domain.model.score_evaluation_message_pb2 import ScoreEvaluationMessage
from ..domain.model.convert import protobuf_message_to_django_model

class EvaluationMessageRepositoryInterface(EvaluationMessageRepository):
    def __init__(self, sqs_url=os.environ.get("SQS_URL")) -> None:
        self.sqs = boto3.client('sqs', region_name='ap-northeast-1')
        self.sqs_url = sqs_url
        
    def fetch_message(self)-> Evaluation:
        response = self.sqs.receive_message(
            QueueUrl=self.sqs_url
        )
        
        msg = ScoreEvaluationMessage() # receive base64 encoded str message
        message = response.get("Messages", "")
        if message=="": # if there is no message in sqs
            return None
        message = response["Messages"][0]['Body']
        message = message[2:-1] # remove b'' from message 
        message = base64.b64decode(message.encode("utf-8")) # base64 decode
        msg.ParseFromString(message)
        eval = protobuf_message_to_django_model(msg)
        eval.receipt_handle = response["Messages"][0]['ReceiptHandle']
        
        # if random seeds are not fully configured, set default values
        # ensure random_seeds count equals to trial_num
        seeds = [0]*eval.trial_num
        for i, x in enumerate(eval.random_seeds["values"]):
            seeds[i] = x
        eval.random_seeds["values"] = seeds

        return eval

    def delete_message(self, eval: Evaluation):
        response = self.sqs.delete_message(
            QueueUrl=self.sqs_url,
            ReceiptHandle=eval.receipt_handle
        )
        return response
        