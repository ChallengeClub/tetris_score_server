from abc import ABCMeta, abstractmethod
from ..model.entity import Evaluation

class EvaluationResultRepository(metaclass=ABCMeta):
    @abstractmethod
    def save_result(self, result: Evaluation):
        raise NotImplementedError
