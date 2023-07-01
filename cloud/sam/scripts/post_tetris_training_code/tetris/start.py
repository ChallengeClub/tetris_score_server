#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess

def start():
    cmd = 'python game_manager.py'

    ret = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)
    if ret.returncode != 0:
        raise Exception(ret.stderr)

if __name__ == '__main__':
    start()
