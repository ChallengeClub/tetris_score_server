from django.test import TestCase

from .strategy import strategy

class ScoreEvaluationTests(TestCase):
    def test_default_evaluation(self):
        result = strategy(
            url="https://github.com/seigot/tetris",
            branch="master",
            trial_num=5,
            level=1,
            game_time=2
        )
        print(result.to_json())
        self.assertEqual(result.status, "S")

    def test_error_branch(self):
        result = strategy(
            url="https://github.com/seigot/tetris",
            branch="masterrr",
            trial_num=1,
            level=1,
            game_time=2
        )
        print(result.to_json())
        self.assertEqual(result.status, "ER")