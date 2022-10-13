import glob
import os
import sys
import re
import mimetypes
import time

# glob, glob, glob if pred do action

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
        name = re.split("/", path)[-1]
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

cmd('/home/crayonie/* IF lastaccess < 1 HR DO print("FOUND")')
