import os
import boto3

from ..domain.repository.evaluation_result_repository import EvaluationResultRepository
from ..domain.model.entity import Evaluation

class EvaluationResultDynamoDBRepositoryInterface(EvaluationResultRepository):
    def __init__(self, dynamodb_table_name=os.environ["dynamodb_table"]):
        self.dynamo = boto3.resource('dynamodb')
        self.table = self.dynamo.Table(dynamodb_table_name)        
    
    def update(self, evaluation: Evaluation):
        print(evaluation.id)
        response = self.table.update_item(
            Key = {
                "Id": evaluation.id,
                "CreatedAt": evaluation.created_at
            },
            UpdateExpression='set \
                #StartedAt = :started_at, \
                #EndedAt = :ended_at, \
                #ErrorMessage = :error_message, \
                #Status = :status, \
                #MeanScore = :score_mean, \
                #StdDevScore = :score_stddev, \
                #MaxScore = :score_max, \
                #MinScore = :score_min\
                ',
            ExpressionAttributeNames= {
			    '#StartedAt' : 'StartedAt',
                '#EndedAt' : 'EndedAt',
                '#ErrorMessage' : 'ErrorMessage',
                '#Status' : 'Status',
                '#MeanScore' : 'MeanScore',
                '#StdDevScore' : 'StdDevScore',
                '#MaxScore' : 'MaxScore',
                '#MinScore' : 'MinScore'
		    },
            ExpressionAttributeValues={
                ':started_at' : evaluation.started_at,
                ':ended_at' : evaluation.ended_at,
                ':error_message' : evaluation.error_message,
                ':status' : evaluation.status,
                ':score_mean' : evaluation.score_mean,
                ':score_stddev' : evaluation.score_stdev,
                ':score_max' : evaluation.score_max,
                ':score_min' : evaluation.score_min
            },
        )
        return response
