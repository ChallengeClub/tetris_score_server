import os
import shutil
import json
from statistics import mean, stdev
import subprocess

from ..domain.model.entity import Evaluation

class ScoreEvaluationApplication:
    def __init__(self, evaluation: Evaluation) -> None:
        self.evaluation = evaluation

    def evaluate(self, log_folder="/server/log")-> Evaluation:
        res = clone_repository(url=self.evaluation.repository_url, branch=self.evaluation.branch)
        if res.returncode:
            self.evaluation.status = "error"
            self.evaluation.error_message = res.stderr
            return self.evaluation
        
        res = pip_install()
        if res.returncode:
            self.evaluation.status = "error"
            self.evaluation.error_message = res.stderr
            return self.evaluation
            
        # execute tetris_start asynchronously
        results = []
        for i in range(self.evaluation.trial_num):
            _result = tetris_start(
                game_time=self.evaluation.game_time,
                log_file=f"{log_folder}/result-{i}.json", 
                level=self.evaluation.level,
                drop_interval=self.evaluation.drop_interval,
                game_mode=self.evaluation.game_mode,
                value_predict_weight=self.evaluation.value_predict_weight,
                timeout=self.evaluation.timeout,
                seed=self.evaluation.random_seeds["values"][i],
            )
            results.append(_result)
        scores = []
        random_seeds = []
        for i, _result in enumerate(results):
            with open(f"{log_folder}/result-{i}.log", 'w', encoding='utf-8') as f:
                if _result.stdout is not None:
                    f.write(_result.stdout)
                else:
                    f.write(_result.stderr)
                if _result.returncode:
                    self.evaluation.status = "error"
                    self.evaluation.error_message = _result.stdout
                    return self.evaluation
            with open(f"{log_folder}/result-{i}.json", 'r', encoding='utf-8') as f:
                res = json.load(f)
                scores.append(int(res["judge_info"]["score"]))
                _seed = int(res["debug_info"].get("random_seed", -1)) # if res["debug_info"]["random_seed"] is null, put invalid seed
                if _seed != -1: # if valid seed, append to list
                    random_seeds.append(_seed)

        # calculate statics
        self.evaluation.scores["values"] = scores
        self.evaluation.random_seeds["values"] = random_seeds
        self.evaluation.score_mean = mean(scores)
        self.evaluation.score_max = max(scores)
        self.evaluation.score_min = min(scores)
        if len(scores) > 1:
            self.evaluation.score_stdev = stdev(scores)
        self.evaluation.status = "succeeded"
        return self.evaluation

def clone_repository(url: str, branch: str):
    """
    clone repository in /home/tetris
    if tetris folder is already exists, git clone after removing
    """
    os.chdir("/home")
    if os.path.exists("tetris"):
        shutil.rmtree("tetris")
    git_clone_command = f"git clone {url} -b {branch} tetris --depth=1" # --depth=1: clone only head
    result = subprocess.run(git_clone_command.split(), capture_output=True, encoding='utf-8')
    return result

def tetris_start(level: int, game_time: int, drop_interval: int, game_mode: str, value_predict_weight: str, timeout: int, seed: int, log_file="result.json"):
    os.chdir("/home/tetris")
    tetris_start_command = f"xvfb-run -a python start.py -l {level} -t {game_time} -d {drop_interval} -m {game_mode} -f {log_file}"
    if value_predict_weight != "":
        tetris_start_command += f" --predict_weight {value_predict_weight}"
    if seed != 0:
        tetris_start_command += f" -r {str(seed)}"

    try:
        result = subprocess.run(
            tetris_start_command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8',
            timeout=timeout
        )
    except subprocess.SubprocessError as e:
        result = subprocess.CalledProcessError(
            returncode=10,
            cmd=tetris_start_command.split(),
            stderr=str(e)
        )
    return result

def pip_install(requiments_file="requirements.txt"):
    os.chdir("/home/tetris")
    pip_install_command = f"pip install -r {requiments_file}"
    result = subprocess.run(pip_install_command.split(), capture_output=True, encoding='utf-8')
    return result