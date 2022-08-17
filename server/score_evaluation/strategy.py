import os
import shutil
import json
from datetime import datetime
from statistics import mean, stdev
import subprocess
from concurrent.futures import ThreadPoolExecutor

from .models import EvaluationResult

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

def tetris_start(level=1, game_time=180, drop_interval=1000, value_mode="default", value_predict_weight="", log_file="result.json"):
    os.chdir("/home/tetris")
    tetris_start_command = f"xvfb-run -a python start.py -l {level} -t {game_time} -d {drop_interval} -m {value_mode} -f {log_file}"
    if value_predict_weight != "":
        tetris_start_command += f" --predict_weight {value_predict_weight}"
    result = subprocess.run(tetris_start_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    return result

def strategy(url: str, branch: str, trial_num=10, level=1, game_time=180, drop_interval=1000, value_mode="default", value_predict_weight=""):
    log_folder = "/server/log"

    # create EvaluationResult instance 
    eval_res = EvaluationResult(
        created_at = str(datetime.now()),
        repository_url = url,
        branch = branch,
        level = level,
        game_time = game_time,
        drop_interval = drop_interval,
        value_mode = value_mode,
        trial_num = trial_num,
    )
    
    res = clone_repository(url=url, branch=branch)
    if res.returncode:
        eval_res.status = "ER"
        eval_res.error_message = res.stderr
        eval_res.ended_at = str(datetime.now())
        return eval_res
    
    # execute tetris_start asynchronously
    futures = []
    with ThreadPoolExecutor() as pool:
        for i in range(trial_num):
            future = pool.submit(
                tetris_start, 
                game_time=game_time, 
                log_file=f"{log_folder}/result-{i}.json", 
                level=level,
                drop_interval=drop_interval,
                value_mode=value_mode,
                value_predict_weight=value_predict_weight,
                )
            futures.append(future)
    scores = []
    for i, future in enumerate(futures):
        with open(f"{log_folder}/result-{i}.log", 'w', encoding='utf-8') as f:
            f.write(future.result().stdout)
        with open(f"{log_folder}/result-{i}.json", 'r', encoding='utf-8') as f:
            res = json.load(f)
            scores.append(int(res["judge_info"]["score"]))

    # calculate statics
    eval_res.ended_at = str(datetime.now())
    eval_res.score_mean = mean(scores)
    eval_res.score_max = max(scores)
    eval_res.score_min = min(scores)
    eval_res.score_stdev = stdev(scores)
    eval_res.status = "S"
    

    return eval_res
