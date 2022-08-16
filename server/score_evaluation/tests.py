from django.test import TestCase

from .strategy import strategy

class ScoreEvaluationTests(TestCase):
    def test_default_evaluation(self):
        result = strategy(
            url="https://github.com/seigot/tetris",
            branch="master",
            trial_num=5,
            level=1,
            game_time=20
        )
        self.assertEqual(result.status, "S")
