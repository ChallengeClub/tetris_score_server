from abc import ABCMeta, abstractmethod
from ..model.entity import Evaluation

class EvaluationResultRepository(metaclass=ABCMeta):
    @abstractmethod
    def update(self, result: Evaluation):
        raise NotImplementedError

    @abstractmethod
    def update_started_at(self, result: Evaluation):
        raise NotImplementedError
    
    @abstractmethod
    def get_status(self, evaluation: Evaluation):
        raise NotImplementedError