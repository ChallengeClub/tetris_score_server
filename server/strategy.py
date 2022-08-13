from curses import resetty
import os
import shutil
import subprocess
from urllib import response

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


def tetris_start(level=1, game_time=180, drop_interval=1000, value_mode="sample", value_predict_weight=""):
    os.chdir("/home/tetris")
    os.environ["QT_QPA_PLATFORM"]="offscreen"
    if value_predict_weight == "":
        tetris_start_command = f"env \\n python start.py -l {level} -t {game_time} -d {drop_interval} -m {value_mode}"
    else:
        tetris_start_command = f"env \\n python start.py -l {level} -t {game_time} -d {drop_interval} -m {value_mode} --predict_weight {value_predict_weight}"
    # tetris_start_command = "QT_QPA_PLATFORM=offscreen && " + tetris_start_command

    result = subprocess.run(tetris_start_command.split(), capture_output=True, encoding='utf-8')
    print(result)

if __name__=="__main__":
    clone_repository(url="https://github.com/seigot/tetris", branch="master")
    tetris_start()
