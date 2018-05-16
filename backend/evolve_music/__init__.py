#!/usr/bin/env python

import json
import sys
from musicgenerator import MusicGenerator
import logging


def serialize_individuals(generation):
    arr = []
    for individual in generation:
        arr.append(individual.to_midi())
    return arr


def main():
    logging.basicConfig(filename='example.log', level=logging.INFO)
    logging.info('Start')
    generator = MusicGenerator()
    while True:
        to_rank = generator.get_music()
        serialized = serialize_individuals(to_rank)
        json_data = json.dumps(serialized)
        print(json_data)
        sys.stdout.flush()

        line = sys.stdin.readline()
        logging.info('Loaded:')
        logging.info(line)
        if not line:
            logging.info('Finished')
            break
        ranks = json.loads(line)
        logging.info('Rank')
        generator.rank_generation(ranks)
    print('Killed')
    return 0


# start process
if __name__ == '__main__':
    main()
