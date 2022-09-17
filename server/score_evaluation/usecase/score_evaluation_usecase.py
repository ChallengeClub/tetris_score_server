from time import sleep

from ..application.score_evaluation_application import ScoreEvaluationApplication
from ..infrastructure.sqs_infrastructure import EvaluationMessageRepositoryInterface

class ScoreEvaluationUsecase:
    def __init__(self) -> None:
        self.evaluation_message_repository_interface = EvaluationMessageRepositoryInterface()

    def execute(self):
        _eval = self.evaluation_message_repository_interface.fetch_message()
        if _eval is None: # if no message in sqs `None` is returned`
            return None
        eval_app = ScoreEvaluationApplication(_eval)
        print("start evaluation:\t", _eval)
        _eval = eval_app.evaluate()
        if _eval.status == "S":
            self.evaluation_message_repository_interface.delete_message(_eval)
        print("finish evaluation:\t", _eval)
        return _eval

    def polling(self, time):
        print("start polling")
        while True:
            _eval = self.execute()
            if _eval is not None:                
                print("result\t", _eval.to_json()) 
                continue
            print(f"no message in sqs, wait for {time} s")
            sleep(time)
