from time import sleep, time
import pathlib

from ..application.score_evaluation_application import ScoreEvaluationApplication
from ..infrastructure.dynamodb_infrastructure import EvaluationResultDynamoDBRepositoryInterface
from ..infrastructure.file_infrastructure import EntryTestRepositoryInterface

class TestEntriesEvaluationUsecase:
    def __init__(self) -> None:
        self.evaluation_dynamodb_repository_interface = EvaluationResultDynamoDBRepositoryInterface()
        self.entry_test_repository_interface = EntryTestRepositoryInterface()
        

    def execute(self, path: str):
        csv_path = pathlib.Path(path)
        if not csv_path.exists():
            raise Exception(f"No such file, {csv_path}")
        
        _evals = self.entry_test_repository_interface.read(csv_path)
        if len(_evals) == 0:
            raise Exception(f"No records in {csv_path}")
        
        _results = []
        for _eval in _evals:
            if _eval.level==0: # level 0, endless mode is not supported now
                _eval.error_message = "level 0, endless mode is not supported now"
                _eval.status = "error"
            else:
                eval_app = ScoreEvaluationApplication(_eval)
                print("start evaluation:\t", _eval)
                _eval.started_at = int(time())
                _eval = eval_app.evaluate()
                _eval.ended_at = int(time())
                print("finish evaluation:\t", _eval)
            _results.append(_eval)
        
        self.entry_test_repository_interface.write(_results, csv_path)
        

    def polling(self, time):
        print("start polling")
        while True:
            _eval = self.execute()
            if _eval is not None:                
                print("result\t", _eval.to_json()) 
                continue
            print(f"no message in sqs, wait for {time} s")
            sleep(time)
