from abc import ABCMeta, abstractmethod

import inject

class ScoreResultRepository(metaclass=ABCMeta):
    @abstractmethod
    def update_result(self, result):
        raise NotImplementedError
    

class ScoreResultRDSRepository(ScoreResultRepository):
    def update_result(self, result):
        pass