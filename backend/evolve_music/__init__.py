#!/usr/bin/env python

import json
import sys
from evolution import Evolution
#import logging
def main():
    # logging.basicConfig(filename='example.log', level=logging.INFO)
    # logging.info('Start')
    evolution = Evolution()
    while True:
        line = sys.stdin.readline()
        # logging.info('Loaded:')
        # logging.info(line)
        print(line)
        if not line:
            # logging.info('Finished')
            break
        ranks = json.loads(line)
        # logging.info('Rank')
        evolution.rank_generation(ranks)
        evolution.next_generation()
        print('AHOJ')
        # print(evolution.individuals_to_rank())
    print('HALELUJA')
    return 0


# start process
if __name__ == '__main__':
    main()
