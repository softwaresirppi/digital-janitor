#!/bin/python3
import glob
import os
import sys
import re
import mimetypes
import time
import shutil
import platform

system = platform.platform()
if 'win' in system:
    filedelimiter = "\\"
else:
    filedelimiter = "/"
print(filedelimiter)
# glob, glob, glob if pred do action
def move(f, t):
    os.renames(f, t)

def copy(f, t):
    pathEntities = t.split(filedelimiter)
    parent = filedelimiter.join(pathEntities[0:len(pathEntities) - 1])
    print(parent)
    try:
        os.makedirs(parent)
    except FileExistsError:
        pass
    shutil.copy(f, t)

def delete(f):
    os.remove(f)

def cmd(line):
    parts = re.split(r'\s+IF|DO\s+', line)
    pattern = parts[0]
    predicate = parts[1]
    predicate = predicate.replace('KB', '* 1000')
    predicate = predicate.replace('MB', '* 1000000')
    predicate = predicate.replace('GB', '* 1000000000')
    predicate = predicate.replace('MIN', '* 60')
    predicate = predicate.replace('HR', '* 3600')
    predicate = predicate.replace('DAY', '* 86400')
    action = parts[2]
    global path
    for path in glob.glob(pattern, recursive = True):
        stat = os.stat(path)
        global size
        size = stat.st_size # in bytes
        global name
        name = path.split(filedelimiter)[-1]
        global extension
        extension = path.split('.')[-1]
        global mimetype
        mimetype = mimetypes.guess_type(path)[0]
        global accessed
        accessed = time.time() - stat.st_atime
        global modified
        modified = time.time() - stat.st_mtime
        if eval(predicate, globals()) == True:
            print('PROCESSING ', path)
            exec(action)

if len(sys.argv) < 2:
    print("No script file is given")
    exit(0)
with open(sys.argv[1]) as f:
    for line in f:
        cmd(line)
