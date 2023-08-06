#!python
import sys

part1_prev = 'zzzzz'

with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('S'):
            parts = line.split('\t', 1)
            part1 = parts[0].split('/')[0]
            part2 = parts[1]
            if part1 != part1_prev:
                print(part1 + '\t' + part2, end='')
                part1_prev = part1
        else:
            print(line, end='')
