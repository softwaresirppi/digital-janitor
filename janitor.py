import glob
import os
import sys
import re

# glob, glob, glob if pred do action

def cmd(line):
    parts = re.split(r'\s+IF|DO\s+', line)
    pattern = parts[0]
    predicate = parts[1]
    action = parts[2]
    for f in glob.glob(pattern):
        stat = os.stat(f)
        global size
        size = stat.st_size # in bytes
        global extension
        extension = f.split('.')[-1]
        if eval(predicate, globals()) == True:
            print('PROCESSING ', f)
            exec(action)


cmd('/home/crayonie/notebook/* IF size < 800 DO print("found")')
