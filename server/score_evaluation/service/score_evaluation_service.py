import os
import shutil
import json
from statistics import mean, stdev
from collections import defaultdict
import subprocess

from ..domain.model.entity import Evaluation
from .status_monitor_service import StatusMonitorService
status_monitor_service = StatusMonitorService()

class ScoreEvaluationService:
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
            if status_monitor_service.check_is_status_interrupted(self.evaluation):
                self.evaluation.status = "canceled"
                print("evaluation was successfully canceled")
                return self.evaluation
            
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
        infos = defaultdict(list)
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
                infos["scores"].append(int(res["judge_info"]["score"]))
                _seed = int(res["debug_info"].get("random_seed", -1)) # if res["debug_info"]["random_seed"] is null, put invalid seed
                if _seed != -1: # if valid seed, append to list
                    infos["random_seeds"].append(_seed)
                infos["gameover_count"].append(int(res["judge_info"]["gameover_count"]))
                infos["block_index"].append(int(res["judge_info"]["block_index"]))
                infos["line_score_stat"].append(res["debug_info"]["line_score_stat"])
                infos["shape_info_stat"].append(res["debug_info"]["shape_info_stat"])

        # calculate statics
        self.evaluation.scores["values"] = infos["scores"]
        self.evaluation.random_seeds["values"] = infos["random_seeds"]
        self.evaluation.score_mean = mean(infos["scores"])
        self.evaluation.score_max = max(infos["scores"])
        self.evaluation.score_min = min(infos["scores"])
        if len(infos["scores"]) > 1:
            self.evaluation.score_stdev = stdev(infos["scores"])
        self.evaluation.status = "succeeded"
        self.evaluation.gameover_count["values"] = infos["gameover_count"]
        self.evaluation.block_index["values"] = infos["block_index"]
        self.evaluation.line_score_stat["values"] = infos["line_score_stat"]
        self.evaluation.shape_info_stat["values"] = infos["shape_info_stat"]

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
    print(tetris_start_command)
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