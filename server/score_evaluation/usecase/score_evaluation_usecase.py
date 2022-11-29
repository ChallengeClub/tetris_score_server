from time import sleep, time

from ..application.score_evaluation_application import ScoreEvaluationApplication
from ..infrastructure.sqs_infrastructure import EvaluationMessageRepositoryInterface
from ..infrastructure.dynamodb_infrastructure import EvaluationResultDynamoDBRepositoryInterface

class ScoreEvaluationUsecase:
    def __init__(self) -> None:
        self.evaluation_message_repository_interface = EvaluationMessageRepositoryInterface()
        self.evaluation_dynamodb_repository_interface = EvaluationResultDynamoDBRepositoryInterface()

    def execute(self):
        _eval = self.evaluation_message_repository_interface.fetch_message()
        if _eval is None: # if no message in sqs `None` is returned`
            return None
        
        if _eval.level==0: # level 0, endless mode is not supported now
            _eval.error_message = "level 0, endless mode is not supported now"
            _eval.status = "error"
        else:
            eval_app = ScoreEvaluationApplication(_eval)
            print("start evaluation:\t", _eval)
            _eval.started_at = int(time())
            _eval = eval_app.evaluate()
            _eval.ended_at = int(time())
            print("finish evaluation:\t", _eval)

        self.evaluation_message_repository_interface.delete_message(_eval)
        res = self.evaluation_dynamodb_repository_interface.update(_eval)
        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            print("failed update to dynamodb:\t", res)
        
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
