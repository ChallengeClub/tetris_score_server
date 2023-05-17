from ..domain.model.entity import Evaluation
from ..infrastructure.dynamodb_infrastructure import EvaluationResultDynamoDBRepositoryInterface

class StatusMonitorService:
    def __init__(self) -> None:
        self.dynamodb_repository_interface = EvaluationResultDynamoDBRepositoryInterface()
    
    def check_is_status_canceled(self, evaluation: Evaluation)->bool:
        status = self.dynamodb_repository_interface.get_status(evaluation)
        return status == "canceled"
