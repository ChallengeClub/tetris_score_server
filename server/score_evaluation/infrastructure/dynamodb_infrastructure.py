import os
import boto3
from decimal import Decimal

from ..domain.repository.evaluation_result_repository import EvaluationResultRepository
from ..domain.repository.entry_test_result_repository import EntryTestResultRepository
from ..domain.model.entity import Evaluation

class EvaluationResultDynamoDBRepositoryInterface(EvaluationResultRepository):
    def __init__(self, dynamodb_table_name=os.environ.get("DYNAMODB_TABLE")):
        self.dynamo = boto3.resource('dynamodb')
        self.table = self.dynamo.Table(dynamodb_table_name)      
    
    def update(self, evaluation: Evaluation):
        response = self.table.update_item(
            Key = {
                "Id": evaluation.id
            },
            UpdateExpression='set \
                #StartedAt = :started_at, \
                #EndedAt = :ended_at, \
                #ErrorMessage = :error_message, \
                #Status = :status, \
                #MeanScore = :score_mean, \
                #StdDevScore = :score_stddev, \
                #MaxScore = :score_max, \
                #MinScore = :score_min, \
                #Scores = :scores,\
                #RandomSeeds = :random_seeds, \
                #GameOverCount = :gameover_count, \
                #BlockIndex = :block_index, \
                #LineScoreStat = :line_score_stat, \
                #ShapeInfoStat = :shape_info_stat \
                ',
            ExpressionAttributeNames= {
                '#StartedAt' : 'StartedAt',
                '#EndedAt' : 'EndedAt',
                '#ErrorMessage' : 'ErrorMessage',
                '#Status' : 'Status',
                '#MeanScore' : 'MeanScore',
                '#StdDevScore' : 'StdDevScore',
                '#MaxScore' : 'MaxScore',
                '#MinScore' : 'MinScore',
                '#Scores' : 'Scores',
                '#RandomSeeds' : 'RandomSeeds',
                '#GameOverCount' : 'GameOverCount',
                '#BlockIndex' : 'BlockIndex',
                '#LineScoreStat' : 'LineScoreStat',
                '#ShapeInfoStat' : 'ShapeInfoStat',
		    },
            ExpressionAttributeValues={
                ':started_at' : evaluation.started_at,
                ':ended_at' : evaluation.ended_at,
                ':error_message' : evaluation.error_message,
                ':status' : evaluation.status,
                ':score_mean' : Decimal(str(evaluation.score_mean)),
                ':score_stddev' : Decimal(str(evaluation.score_stdev)),
                ':score_max' : Decimal(str(evaluation.score_max)),
                ':score_min' : Decimal(str(evaluation.score_min)),
                ':scores' : evaluation.scores.get("values", []),
                ':random_seeds' : evaluation.random_seeds.get("values", []),
                ':gameover_count' : evaluation.gameover_count.get("values", []),
                ':block_index' : evaluation.block_index.get("values", []),
                ':line_score_stat' : evaluation.line_score_stat.get("values", []),
                ':shape_info_stat' : evaluation.shape_info_stat.get("values", []),
            },
        )
        return response
    
    def update_started_at(self, evaluation: Evaluation):
        response = self.table.update_item(
            Key = {
                "Id": evaluation.id
            },
            UpdateExpression='set \
                #StartedAt = :started_at, \
                #Status = :status \
                ',
            ExpressionAttributeNames= {
                '#StartedAt' : 'StartedAt',
                '#Status' : 'Status',
		    },
            ExpressionAttributeValues={
                ':started_at' : evaluation.started_at,
                ':status' : evaluation.status,
            },
        )
        return response

class EntriesResultDynamoDBRepositoryInterface(EntryTestResultRepository):
    def __init__(self, dynamodb_table_name=os.environ.get("dynamodb_competition_table", "")):
        self.dynamo = boto3.resource('dynamodb')
        self.table = self.dynamo.Table(dynamodb_table_name)      
    
    def update_entry(self, evaluation: Evaluation):
        response = self.table.update_item(
            Key = {
                "RepositoryURL": evaluation.repository_url,
                "Level": evaluation.level
            },
            UpdateExpression='set \
                #StartedAt = :started_at, \
                #EndedAt = :ended_at, \
                #ErrorMessage = :error_message, \
                #Status = :status, \
                #MeanScore = :score_mean \
                ',
            ExpressionAttributeNames= {
                '#StartedAt' : 'StartedAt',
                '#EndedAt' : 'EndedAt',
                '#ErrorMessage' : 'ErrorMessage',
                '#Status' : 'Status',
                '#MeanScore' : 'MeanScore',
		    },
            ExpressionAttributeValues={
                ':started_at' : evaluation.started_at,
                ':ended_at' : evaluation.ended_at,
                ':error_message' : evaluation.error_message,
                ':status' : evaluation.status,
                ':score_mean' : Decimal(str(evaluation.score_mean))
            },
        )
        return response
