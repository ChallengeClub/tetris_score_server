import os
import boto3

from ..domain.repository.evaluation_result_repository import EvaluationResultRepository
from ..domain.model.entity import Evaluation

class EvaluationResultDynamoDBRepositoryInterface(EvaluationResultRepository):
    def __init__(self, dynamodb_table_name=os.environ["dynamodb_table"]):
        self.dynamo = boto3.resource('dynamodb')
        self.table = self.dynamo.Table(dynamodb_table_name)        
    
    def update(self, evaluation: Evaluation):
        item = evaluation.to_dict()
        response = self.table.put_item(
            Item = item
        )
        return response
