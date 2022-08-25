from ..domain.repository.evaluation_result_repository import EvaluationResultRepository
from ..domain.model.entity import Evaluation

class EvaluationResultRDSRepositoryInterface(EvaluationResultRepository):
    def update(self, evalution: Evaluation):
        pass
