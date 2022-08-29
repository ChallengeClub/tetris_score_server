from ..application.score_evaluation_application import ScoreEvaluationApplication
from ..infrastructure.sqs_infrastructure import EvaluationMessageRepositoryInterface

class ScoreEvaluationUsecase:
    def __init__(self) -> None:
        self.evaluation_message_repository_interface = EvaluationMessageRepositoryInterface()

    def execute(self):
        eval = self.evaluation_message_repository_interface.fetch_message()
        if not eval.repository_url:
            return None
        eval_app = ScoreEvaluationApplication(eval)
        eval_result = eval_app.evaluate()
        if eval_result.status == "S":
            self.evaluation_message_repository_interface.delete_message(eval_result)
        return eval_result
