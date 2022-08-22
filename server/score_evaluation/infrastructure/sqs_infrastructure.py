import base64
import boto3
import os
import json

from ..model.models import Evaluation
from ..repository.evaluation_message_repository import EvaluationMessageRepository
from ..repository.evaluation_result_repository import EvaluationResultRepository

from ..model.score_evaluation_message_pb2 import ScoreEvaluationMessage

class EvaluationMessageRepositoryInterface(EvaluationMessageRepository):
    def __init__(self, sqs_url=os.environ["sqs_url"]) -> None:
        self.sqs = boto3.client('sqs', region_name='ap-northeast-1')
        self.sqs_url = sqs_url
        
    def fetch_message(self)-> ScoreEvaluationMessage:
        response = self.sqs.receive_message(
            QueueUrl=self.sqs_url            
        )
        
        msg = ScoreEvaluationMessage() # receive base64 encoded str message
        message = response["Messages"][0]['Body'][2:-1] # remove b'' from message
        message = base64.b64decode(message) # base64 decode
        msg.ParseFromString(message)
        
        return msg

    def delete_message(self: Evaluation):
        pass
        


class EvaluationResultRDSRepositoryInterface(EvaluationResultRepository):
    def update(self, evalution: Evaluation):
        pass
