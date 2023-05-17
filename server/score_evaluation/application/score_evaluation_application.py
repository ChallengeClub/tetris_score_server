from time import sleep
from ..usecase.score_evaluation_usecase import ScoreEvaluationUsecase

class ScoreEvaluationApplication:
    def __init__(self):
        self.score_evaluation_usecase = ScoreEvaluationUsecase()
    
    def start(self, time):
        print("start polling")
        while True:
            _eval = self.score_evaluation_usecase.execute()
            if _eval is not None:                
                print("result\t", _eval.to_json()) 
                continue
            print(f"no message in sqs, wait for {time} s")
            sleep(time)
    