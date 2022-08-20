from django.test import TestCase

from .usecase.usecases import ScoreEvaluationUsecase
from .infrastructure.interface import EvaluationMessageRepositoryInterface
from .model.models import Evaluation

# class ScoreEvaluationTests(TestCase):
#     def test_default_evaluation(self):
#         eval = Evaluation(
#             repository_url="https://github.com/seigot/tetris",
#             branch="master",
#             trial_num=5,
#             level=1,
#             game_time=2
#         )
#         usecase = ScoreEvaluationUsecase(eval)
#         eval = usecase.evaluate()
#         self.assertEqual(eval.status, "S")

#     def test_error_branch(self):
#         """
#         with invalid branch name, git clone would be failed
#         """   
#         eval = Evaluation(
#             repository_url="https://github.com/seigot/tetris",
#             branch="masterrr",
#             trial_num=1,
#             level=1,
#             game_time=2
#         )
#         usecase = ScoreEvaluationUsecase(eval)
#         eval = usecase.evaluate()
#         self.assertEqual(eval.status, "ER")
    
#     def test_error_empty_value_mode(self):
#         """
#         with brank value mode, tetris start cmd would be failed
#         """  
#         eval = Evaluation(
#             repository_url="https://github.com/seigot/tetris",
#             branch="master",
#             game_mode = "",
#             trial_num=1,
#             level=1,
#             game_time=2
#         )
#         usecase = ScoreEvaluationUsecase(eval)
#         eval = usecase.evaluate()
#         self.assertEqual(eval.status, "ER")
    
#     def test_error_time_out(self):
#         """
#         with brank value mode, tetris start cmd would be failed
#         """  
#         eval = Evaluation(
#             repository_url="https://github.com/seigot/tetris",
#             branch="master",
#             trial_num=1,
#             level=1,
#             game_time=10,
#             timeout=1
#         )
#         usecase = ScoreEvaluationUsecase(eval)
#         eval = usecase.evaluate()
#         print(eval.error_message)
#         self.assertEqual(eval.status, "ER")
        

class InterfaceTests(TestCase):
    def test_fetch_message(self):
        mes_if = EvaluationMessageRepositoryInterface()
        res = mes_if.fetch_message()
        print(res)
        print(type(res))