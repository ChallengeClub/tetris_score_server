#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from argparse import ArgumentParser

def get_option(art_config_filepath):
    argparser = ArgumentParser()
    argparser.add_argument('--art_config_filepath', type=str,
                           default=art_config_filepath,
                           help='art_config file path')
    return argparser.parse_args()

def start():
    ## default value
    ART_CONFIG = "default.json"

    ## update value if args are given
    args = get_option(ART_CONFIG)
    if len(args.art_config_filepath) != 0:
        ART_CONFIG = args.art_config_filepath

    ## print
    print('ART_CONFIG: ' + str(ART_CONFIG))

    ## start game
    cmd = 'python game_manager.py' \
        + ' ' + '--art_config_filepath' + ' ' + str(ART_CONFIG)

    ret = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)
    if ret.returncode != 0:
        raise Exception(ret.stderr)

if __name__ == '__main__':
    start()
