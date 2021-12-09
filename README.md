# Advent of Code

This is just a repo for my solutions to the [Advent of Code](https://adventofcode.com/2021/about) programming contest. It also contains a small utility to make grabbing the day's test data and feeding it to the day-specific code a little easier. Right now it just for Python; maybe at some point I'll make other languages an option.

```
usage: aoc.py [-h] [--data DATA] [--nocache] [--config CONFIG]
              [--loglevel LOGLEVEL]
              YEAR DAY [PART]

Run/test Advent of Code solution

positional arguments:
  YEAR
  DAY
  PART

optional arguments:
  -h, --help           show this help message and exit
  --data DATA          File with data for part
  --nocache            Ignore cache and force (re)download of data
  --config CONFIG      Config file to use
  --loglevel LOGLEVEL  Set log level
```

By default, the utility downloads the data from the Advent of Code website. This depends on having your session key from an authenticated web session. This can be provided through a file called `config.txt` in the main directory with the very simple format:

```shell
sessionid=YOUR_SESSION_ID_HERE
```

## Solutions

They are what they are. For some of them I strove for some level of elegance. Others, not so much. If some of the data handling seems rococo, the first few solutions were written without this framework and I just did the minimal amount of work to make them fit.

## A Personal Note

I'm looking for a job. Most of my work experience has been in education, but I have a degree in CS and I've been programming forever. If you know of something please contact me.