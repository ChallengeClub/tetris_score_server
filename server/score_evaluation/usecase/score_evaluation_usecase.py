from time import sleep, time

from ..service.score_evaluation_service import ScoreEvaluationService
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
            eval_app = ScoreEvaluationService(_eval)
            print("start evaluation:\t", _eval)
            _eval.started_at = int(time())
            _eval.status = "evaluating"
            res = self.evaluation_dynamodb_repository_interface.update_started_at(_eval)
            if res['ResponseMetadata']['HTTPStatusCode'] != 200:
                print("failed update to dynamodb:\t", res)

            _eval = eval_app.evaluate(log_folder="/server/log")
            _eval.ended_at = int(time())
            print("finish evaluation:\t", _eval)
        
        res = self.evaluation_dynamodb_repository_interface.update(_eval)
        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            print("failed update to dynamodb:\t", res)
        self.evaluation_message_repository_interface.delete_message(_eval)
        
        return _eval

