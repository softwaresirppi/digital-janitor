import glob
import os
import sys

# Plan for config syntax,
# PATTERN [if COND] | ACTION
# ACTION > move = copy

def fileName(path):
    return path.split('/')[-1]

def interpret(line):
    tokens = line.split('>');
    pattern = tokens[0].strip();
    action = tokens[1].strip();
    print(pattern)
    print(action)
    for f in glob.glob(pattern):
        print(f)
        print(action + fileName(f))
        os.renames(f, action + fileName(f))

with open(sys.argv[1], 'r') as script:
    for line in script.readlines():
        print(line)
        interpret(line)
