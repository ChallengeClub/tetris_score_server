import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

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

def tetris_start(level=1, game_time=180, drop_interval=1000, value_mode="sample", value_predict_weight=""):
    os.chdir("/home/tetris")
    os.environ["QT_QPA_PLATFORM"]="offscreen"
    if value_predict_weight == "":
        tetris_start_command = f"xvfb-run -a python start.py -l {level} -t {game_time} -d {drop_interval} -m {value_mode}"
    else:
        tetris_start_command = f"xvfb-run -a python start.py -l {level} -t {game_time} -d {drop_interval} -m {value_mode} --predict_weight {value_predict_weight}"
    result = subprocess.run(tetris_start_command.split(), capture_output=True, encoding='utf-8')
    return result

def strategy():
    url = "https://github.com/seigot/tetris"
    branch = "master"
    repeet = 5
    game_time = 10
    res = clone_repository(url=url, branch=branch)
    if res.returncode:
        return res
    
    # execute tetris_start asynchronously
    futures = []
    with ThreadPoolExecutor() as pool:
        for i in range(repeet):
            future = pool.submit(tetris_start, game_time=game_time)
            futures.append(future)
    for i, future in enumerate(futures):
        with open(f"/server/log/result-{i}.log", 'w', encoding='utf-8') as f:
            f.write(future.result().stdout)


if __name__=="__main__":
    strategy()
