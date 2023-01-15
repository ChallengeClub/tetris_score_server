import pathlib
from abc import ABCMeta, abstractmethod
from ..model.entity import Evaluation

class EntryTestResultRepository(metaclass=ABCMeta):
    @abstractmethod
    def update(self, evaluation: Evaluation):
        raise NotImplementedError