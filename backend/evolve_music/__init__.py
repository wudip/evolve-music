#!/usr/bin/env python

import json
import sys
from evolution import Evolution
import logging


def serialize_individuals(generation):
    arr = []
    for individual in generation:
        arr.append(individual.to_midi())
    return arr


def main():
    logging.basicConfig(filename='example.log', level=logging.INFO)
    logging.info('Start')
    evolution = Evolution()
    while True:
        line = sys.stdin.readline()
        logging.info('Loaded:')
        logging.info(line)
        if not line:
            logging.info('Finished')
            break
        ranks = json.loads(line)
        logging.info('Rank')
        evolution.rank_generation(ranks)
        evolution.next_generation()
        to_rank = evolution.individuals_to_rank()
        serialized = serialize_individuals(to_rank)
        json_data = json.dumps(serialized)
        print(json_data)
        logging.info('Ahoj')
        # print(evolution.individuals_to_rank())
        sys.stdout.flush()
    print('HALELUJA')
    return 0


# start process
if __name__ == '__main__':
    main()
