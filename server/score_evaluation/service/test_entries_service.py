import os
import shutil
import json
import subprocess

from ..domain.model.entity import Evaluation

class TestEntriesService:
    def __init__(self, evaluation: Evaluation) -> None:
        self.evaluation = evaluation

    def evaluate(self)-> Evaluation:
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
            
        # execute tetris_start
        res = tetris_start(
            game_time=self.evaluation.game_time, 
            level=self.evaluation.level,
            drop_interval=self.evaluation.drop_interval,
            game_mode=self.evaluation.game_mode,
            value_predict_weight=self.evaluation.value_predict_weight,
            timeout=self.evaluation.timeout
        )
        if res.returncode: # if error occured in the subprocess
            self.evaluation.status = "error"
            self.evaluation.error_message = res.stdout
            return self.evaluation

        # calculate statics
        with open("tetris/result.json", mode="r") as f:
            _dict = json.load(f)
        self.evaluation.error = ""
        self.evaluation.score_mean = int(_dict["judge_info"]["score"])
        self.evaluation.status = "succeeded"
        
        return self.evaluation

def clone_repository(url: str, branch: str):
    """
    clone repository in /tetris
    if tetris folder is already exists, git clone after removing
    """
    if os.path.exists("tetris"):
        # permission error would occurs, without write permission. `os.chmod` cannot give white permission in Windows OS`
        # https://docs.python.org/ja/3/library/os.html 
        subprocess.run("chmod -R 777 tetris".split(), encoding='utf-8')
        shutil.rmtree("tetris")
    git_clone_command = f"git clone {url} -b {branch} tetris --depth=1" # --depth=1: clone only head
    result = subprocess.run(git_clone_command.split(), capture_output=True, encoding='utf-8')
    return result

def tetris_start(level: int, game_time: int, drop_interval: int, game_mode: str, value_predict_weight: str, timeout: int):
    os.chdir("tetris")
    tetris_start_command = f"python start.py -l {level} -t {game_time} -d {drop_interval} -m {game_mode}"
    if value_predict_weight != "":
        tetris_start_command += f" --predict_weight {value_predict_weight}"
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
    os.chdir("..")
    return result

def pip_install(requiments_file="requirements.txt"):
    pip_install_command = f"pip install -r {requiments_file}"
    result = subprocess.run(pip_install_command.split(), capture_output=True, encoding='utf-8')
    return result