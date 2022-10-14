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

# glob, glob, glob if pred do action
def move(f, t, doPrompt = False):
    if doPrompt:
        if not prompt(f):
            return
    os.renames(f, t)

def copy(f, t, doPrompt = False):
    if doPrompt:
        if not prompt(f):
            return
    pathEntities = t.split(filedelimiter)
    parent = filedelimiter.join(pathEntities[0:len(pathEntities) - 1])
    print(parent)
    try:
        os.makedirs(parent)
    except FileExistsError:
        pass
    shutil.copy(f, t)

def delete(f, doPrompt = False):
    if doPrompt:
        if not prompt(f):
            return
    os.remove(f)

def prompt(f):
    print(f + ": Are you sure? (y/n)")
    reply = input().lower()
    if reply == 'y':
        return True
    else:
        return False


def cmd(line):
    parts = re.split(r'\s+IF|DO\s+', line)
    pattern = parts[0]
    pattern = pattern.strip()
    if len(parts) == 2:
        predicate = 'True'
    else:
        predicate = parts[1]
    predicate = predicate.replace('KB', '* 1000')
    predicate = predicate.replace('MB', '* 1000000')
    predicate = predicate.replace('GB', '* 1000000000')
    predicate = predicate.replace('MIN', '* 60')
    predicate = predicate.replace('HR', '* 3600')
    predicate = predicate.replace('DAY', '* 86400')
    action = parts[-1]
    global path
    for path in glob.glob(pattern, recursive = True):
        if os.path.isfile(path):
            stat = os.stat(path)
            global size
            size = stat.st_size # in bytes
            global name
            name = path.split(filedelimiter)[-1]
            global extension
            extension = path.split('.')[-1]
            global mimetype
            mimetype = mimetypes.guess_type(path)[0]
            if mimetype == None:
                mimetype = ''
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
