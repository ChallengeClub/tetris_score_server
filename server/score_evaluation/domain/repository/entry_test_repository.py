import pathlib
from abc import ABCMeta, abstractmethod
from ..model.entity import Evaluation

class EntryTestFileRepository(metaclass=ABCMeta):
    @abstractmethod
    def read(self, csv_path: pathlib.Path) -> list[Evaluation]:
        raise NotImplementedError

    @abstractmethod
    def write(self, results: list[Evaluation], csv_path: pathlib.Path):
        raise NotImplementedError