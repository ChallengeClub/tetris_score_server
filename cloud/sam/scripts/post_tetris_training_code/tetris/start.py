#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from argparse import ArgumentParser

def get_option(random_seed, art_config_filepath):
    argparser = ArgumentParser()
    argparser.add_argument('-r', '--random_seed', type=int,
                           default=random_seed,
                           help='Specify random seed if necessary') 
    argparser.add_argument('--art_config_filepath', type=str,
                           default=art_config_filepath,
                           help='art_config file path')
    return argparser.parse_args()

def start():
    ## default value
    INPUT_RANDOM_SEED = -1
    ART_CONFIG = "default.json"

    ## update value if args are given
    args = get_option(INPUT_RANDOM_SEED,
                      ART_CONFIG)
    if args.random_seed >= 0:
        INPUT_RANDOM_SEED = args.random_seed
    if len(args.art_config_filepath) != 0:
        ART_CONFIG = args.art_config_filepath

    ## set field parameter for level 1
    RANDOM_SEED = 0            # random seed for field
    OBSTACLE_HEIGHT = 0        # obstacle height (blocks)
    OBSTACLE_PROBABILITY = 0   # obstacle probability (percent)

    ## update field parameter level
    RANDOM_SEED = 0

    ## update random seed
    if INPUT_RANDOM_SEED >= 0:
        RANDOM_SEED = INPUT_RANDOM_SEED

    ## print
    print('RANDOM_SEED: ' + str(RANDOM_SEED))
    print('OBSTACLE_HEIGHT: ' + str(OBSTACLE_HEIGHT))
    print('OBSTACLE_PROBABILITY: ' + str(OBSTACLE_PROBABILITY))
    print('ART_CONFIG: ' + str(ART_CONFIG))

    ## start game
    cmd = 'python game_manager.py' \
        + ' ' + '--seed' + ' ' + str(RANDOM_SEED) \
        + ' ' + '--obstacle_height' + ' ' + str(OBSTACLE_HEIGHT) \
        + ' ' + '--obstacle_probability' + ' ' + str(OBSTACLE_PROBABILITY) \
        + ' ' + '--art_config_filepath' + ' ' + str(ART_CONFIG)

    ret = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)
    if ret.returncode != 0:
        raise Exception(ret.stderr)

if __name__ == '__main__':
    start()
