from abc import ABCMeta, abstractmethod
from ..model.entity import Evaluation

class EvaluationResultRepository(metaclass=ABCMeta):
    @abstractmethod
    def update(self, result: Evaluation):
        raise NotImplementedError
