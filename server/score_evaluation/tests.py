from django.test import TestCase

from .usecases import ScoreEvaluationUsecase
from .models import Evaluation

class ScoreEvaluationTests(TestCase):
    def test_default_evaluation(self):
        eval = Evaluation(
            repository_url="https://github.com/seigot/tetris",
            branch="master",
            trial_num=5,
            level=1,
            game_time=10
        )
        usecase = ScoreEvaluationUsecase(eval)
        eval = usecase.evaluate()
        self.assertEqual(eval.status, "S")

    def test_error_branch(self):        
        eval = Evaluation(
            repository_url="https://github.com/seigot/tetris",
            branch="masterrr",
            trial_num=1,
            level=1,
            game_time=10
        )
        usecase = ScoreEvaluationUsecase(eval)
        eval = usecase.evaluate()
        self.assertEqual(eval.status, "ER")