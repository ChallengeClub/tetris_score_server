import base64
import boto3
import os

from ..domain.model.entity import Evaluation
from ..domain.repository.evaluation_message_repository import EvaluationMessageRepository
from ..domain.repository.evaluation_result_repository import EvaluationResultRepository

from ..domain.model.score_evaluation_message_pb2 import ScoreEvaluationMessage
from ..domain.model.convert import protobuf_message_to_django_model

class EvaluationMessageRepositoryInterface(EvaluationMessageRepository):
    def __init__(self, sqs_url=os.environ["sqs_url"]) -> None:
        self.sqs = boto3.client('sqs', region_name='ap-northeast-1')
        self.sqs_url = sqs_url
        
    def fetch_message(self)-> Evaluation:
        response = self.sqs.receive_message(
            QueueUrl=self.sqs_url            
        )
        
        msg = ScoreEvaluationMessage() # receive base64 encoded str message
        try:
            message = response["Messages"][0]['Body'][2:-1] # remove b'' from message
            message = base64.b64decode(message) # base64 decode
            msg.ParseFromString(message)
            eval = protobuf_message_to_django_model(msg)
            eval.status = "EV"
            eval.receipt_handle = response["Messages"][0]['ReceiptHandle']
        except KeyError:
            eval = Evaluation()
        return eval

    def delete_message(self, eval: Evaluation):
        response = self.sqs.delete_message(
            QueueUrl=self.sqs_url,
            ReceiptHandle=eval.receipt_handle
        )
        return response
        