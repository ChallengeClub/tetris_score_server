from abc import ABCMeta, abstractmethod
from ..model.models import Evaluation


class EvaluationMessageRepository(metaclass=ABCMeta):
    @abstractmethod
    def fetch_message(self)-> Evaluation:
        raise NotImplementedError
    
    @abstractmethod
    def delete_message(self: Evaluation):
        raise NotImplementedError
