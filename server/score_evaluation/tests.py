from django.test import TestCase
import base64
import boto3

from .usecase.usecases import ScoreEvaluationUsecase
from .infrastructure.sqs_infrastructure import EvaluationMessageRepositoryInterface
from .model.models import Evaluation
from .model.score_evaluation_message_pb2 import ScoreEvaluationMessage

class ScoreEvaluationTests(TestCase):
    def test_default_evaluation(self):
        eval = Evaluation(
            repository_url="https://github.com/seigot/tetris",
            branch="master",
            trial_num=5,
            level=1,
            game_time=2
        )
        usecase = ScoreEvaluationUsecase(eval)
        eval = usecase.evaluate()
        self.assertEqual(eval.status, "S")

    def test_error_branch(self):
        """
        with invalid branch name, git clone would be failed
        """   
        eval = Evaluation(
            repository_url="https://github.com/seigot/tetris",
            branch="masterrr",
            trial_num=1,
            level=1,
            game_time=2
        )
        usecase = ScoreEvaluationUsecase(eval)
        eval = usecase.evaluate()
        self.assertEqual(eval.status, "ER")
    
    def test_error_empty_value_mode(self):
        """
        with brank value mode, tetris start cmd would be failed
        """  
        eval = Evaluation(
            repository_url="https://github.com/seigot/tetris",
            branch="master",
            game_mode = "",
            trial_num=1,
            level=1,
            game_time=2
        )
        usecase = ScoreEvaluationUsecase(eval)
        eval = usecase.evaluate()
        self.assertEqual(eval.status, "ER")
    
    def test_error_time_out(self):
        """
        with brank value mode, tetris start cmd would be failed
        """  
        eval = Evaluation(
            repository_url="https://github.com/seigot/tetris",
            branch="master",
            trial_num=1,
            level=1,
            game_time=10,
            timeout=1
        )
        usecase = ScoreEvaluationUsecase(eval)
        eval = usecase.evaluate()
        self.assertEqual(eval.status, "ER")
        

class InterfaceTests(TestCase):
    def setUp(self):
        self.sqs_client = boto3.client('sqs', region_name='ap-northeast-1')
        response = self.sqs_client.create_queue(
            QueueName='test_evaluation_message_queue2'
        )
        self.sqs_url = response["QueueUrl"]
        test_msg = ScoreEvaluationMessage()
        test_msg.repository_url = "https://github.com/seigot/tetris"
        test_msg.branch = "master"
        test_msg.drop_interval = 1000
        test_msg.level = 1
        test_msg.game_mode = "default"
        test_msg.game_time=10
        test_msg.timeout=200
        test_msg.trial_num=1
        message = str(base64.b64encode(test_msg.SerializeToString()))
        self.sqs_client.send_message(
            QueueUrl=self.sqs_url,
            MessageBody=message
        )
    
    def tearDown(self):
        self.sqs_client.delete_queue(
            QueueUrl=self.sqs_url
        )
        return 

    def test_fetch_message(self):
        mes_if = EvaluationMessageRepositoryInterface(self.sqs_url)
        res = mes_if.fetch_message()
        self.assertNotEqual(res.repository_url, "")
    