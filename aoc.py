#!/usr/bin/python3

from importlib import import_module
import argparse
import logging
import requests
import os
from io import StringIO

parser = argparse.ArgumentParser(description='Run/test Advent of Code solution')
parser.add_argument('year', metavar='YEAR', type=int)
parser.add_argument('day', metavar='DAY', type=int)
parser.add_argument('part', metavar='PART', type=int, nargs='?', default=1)
parser.add_argument('--data', help='Data file for challenge')
parser.add_argument('--nocache', help='Ignore cache and force (re)download of data', action='store_true')
parser.add_argument('--config', help='Config file', default='config.txt')
parser.add_argument('--loglevel', help='Set log level', default='warn')

args = parser.parse_args()
logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

# Probably overkill, but maybe I'll think of something else to use the config file for
config = {}
try:
    for line in open(args.config):
        key, val = line.split('=')
        config[key] = val
except FileNotFoundError:
    pass

# Use datafile if given on command line
if args.data:
    logging.info(f'Using local data file f{args.data}')
    data = open(args.data, 'r')
# Otherwise check cache and/or try to download
else:
    cachename = f'data{args.year}-{args.day}.txt'
    if args.nocache or not os.path.exists(f'cache/{cachename}'):
        try:
            logging.info(f'Downloading data for {args.year} day {args.day}')
            data = requests.get(f'https://adventofcode.com/{args.year}/day/{args.day}/input',
                                cookies={'session': config['sessionid']}).text
            if not args.nocache:
                logging.info('Caching data')
                try:
                    os.mkdir('cache')
                except FileExistsError:
                    pass
                cachefile = open(f'cache/{cachename}', 'w')
                cachefile.write(data)
                cachefile.close()
            data = StringIO(data)
        except KeyError:
            logging.error('No session id to download data. Try using --data option to specify filename.')
            exit()
    else:
        logging.info(f'Using cached data for {args.year} day {args.day}')
        data = open(f'cache/{cachename}')

logging.info(f'Running code for {args.year} day {args.day} part {args.part}')
advent = import_module(f'{args.year}.advent{args.day}')
advent.main(data, args.part, logging)