import pathlib
import csv

from ..domain.model.entity import Evaluation
from ..domain.repository.entry_test_repository import EntryTestRepository

class EntryTestRepositoryInterface(EntryTestRepository):
    def read(self, csv_path: pathlib.Path) -> list[Evaluation]:
        with open(csv_path) as f:
            _reader = csv.DictReader(f)
            _results = []
            
            for _dict in _reader:
                print(_dict)
                _eval = Evaluation()
                _eval.name = _dict["name"]
                _eval.repository_url = _dict["repository_url"]
                _eval.status = _dict["status"]
                _eval.branch = _dict["branch"]
                _eval.created_at = _dict["created_at"]
                _eval.level = int(_dict["level"])
                _eval.game_mode = _dict["game_mode"]
                _eval.predict_weight_path = _dict["predict_weight_path"]                    

                _results.append(_eval)
            return _results
    
    def write(self, results: list[Evaluation], csv_path: pathlib.Path):
        _fields = [
            "name",
            "repository_url",
            "status",
            "branch",
            "created_at",
            "started_at",
            "level",
            "game_mode",
            "predict_weight_path",
            "error_message"
        ]
        with open(csv_path, mode="w") as f:
            _writer = csv.DictWriter(f, fieldnames=_fields)
            _writer.writeheader()
            _writer.writerows(map(lambda result: result.to_dict(), results))
        