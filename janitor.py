#!/bin/python3
import glob
import os
import sys
import re
import mimetypes
import time
import shutil
import platform
from tkinter import *
from pathlib import Path

system = platform.platform()
if 'win' in system:
    filedelimiter = "\\"
else:
    opener = 'xdg-open'
    filedelimiter = "/"

# glob, glob, glob if pred do action
def move(f, t):
    os.renames(f, t)

def copy(f, t):
    pathEntities = t.split(filedelimiter)
    parent = filedelimiter.join(pathEntities[0:len(pathEntities) - 1])
    try:
        os.makedirs(parent)
    except FileExistsError:
        pass
    shutil.copy(f, t)

def delete(f):
    os.remove(f)

def prompt(f, preview = False):
    # not cross platform
    if preview:
        os.system(opener + ' ' + f)
    print(f + ": Are you sure? (y/n)", end = '')
    reply = input().lower()
    if reply == 'y':
        return True
    else:
        return False

# returns pattern, cond, action
def parse(source):
    if 'IF' not in source:
        source = source.replace('DO', ' IF DO');
    parts = list(re.findall('(.*)IF(.*)DO(.*)', source)[0])
    for i in range(3):
        parts[i] = parts[i].strip()
    return parts

folder = os.getcwd()
def cmd(line):
    paths = []
    global folder
    # change directory
    if 'DO' not in line:
        os.chdir(line)
        folder = os.getcwd()
        print(folder)
        return
    # parsing
    pattern, predicate, action = parse(line)
    if pattern == '':
        pattern = '*'
    pattern = folder + filedelimiter + pattern
    if predicate == '':
        predicate = 'True'
    if action == '':
        action = 'print(path)';
    # macros
    predicate = predicate.replace('KB', '* 1000')
    predicate = predicate.replace('MB', '* 1000000')
    predicate = predicate.replace('GB', '* 1000000000')
    predicate = predicate.replace('MIN', '* 60')
    predicate = predicate.replace('HR', '* 3600')
    predicate = predicate.replace('DAY', '* 86400')
    action = re.sub('^preview\s+print$', 'print(path) if prompt(path, True) else None', action)
    action = re.sub('^alert\s+print$', 'print(path) if prompt(path) else None', action)
    action = re.sub('^print$', 'print(path)', action)

    action = re.sub('^preview\s+delete$', 'delete(path) if prompt(path, True) else None', action)
    action = re.sub('^alert\s+delete$', 'delete(path) if prompt(path) else None', action)
    action = re.sub('^delete$', 'delete(path)', action)

    action = re.sub('^preview\s+move\s+to\s+(.*)$', 'move(path, \'\\1\' + filedelimiter + name) if prompt(path, True) else None', action)
    action = re.sub('^alert\s+move\s+to\s+(.*)$', 'move(path, \'\\1\' + filedelimiter + name) if prompt(path) else None', action)
    action = re.sub('^move\s+to\s+(.*)$', 'move(path, \'\\1\' + filedelimiter + name)', action)

    action = re.sub('^preview\s+copy\s+to\s+(.*)$', 'copy(path, \'\\1\' + filedelimiter + name) if prompt(path, True) else None', action)
    action = re.sub('^alert\s+copy\s+to\s+(.*)$', 'copy(path, \'\\1\' + filedelimiter + name) if prompt(path) else None', action)
    action = re.sub('^copy\s+to\s+(.*)$', 'copy(path, \'\\1\' + filedelimiter + name)', action)
    global path
    for path in glob.glob(pattern, recursive = True):
        if os.path.isfile(path):
            stat = os.stat(path)
            global size
            size = stat.st_size # in bytes
            global name
            name = path.split(filedelimiter)[-1]
            global parent
            parent = path.split(filedelimiter)[-2]
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
                paths.append(path)
                exec(action)
    return paths

def gui():
    window = Tk()
    window.title('Automatic file organizer')
    window.resizable(False, False)
    Label(window, text= 'Files',  fg = 'white' ).grid(row=0, column=0)
    fileName = Entry(window, width= 40, bg = 'black', fg = 'white')
    fileName.grid(row=0, column=1, columnspan=4)
    Label(window, text= 'Condition',  fg = 'white' ).grid(row=1, column=0)
    condition = Entry(window, width= 40, bg = 'black', fg = 'white')
    condition.grid(row=1, column=1, columnspan=4)
    Label(window, text= 'Destination (?)', fg = 'white' ).grid(row=2, column=0)
    dest = Entry(window, width= 40, bg = 'black', fg = 'white' )
    dest.grid(row=2, column=1, columnspan=4)
    Button(window, text='MOVE', command=lambda : cmd(f"{fileName.get()} {'' if condition.get() == ''  else 'IF'} {condition.get()} DO move to {dest.get()}")).grid(row=3, column=0)
    Button(window, text='COPY', command=lambda : cmd(f"{fileName.get()} {'' if condition.get() == ''  else 'IF'} {condition.get()} DO copy to {dest.get()}")).grid(row=3, column=1)
    Button(window, text='TRASH', command=lambda : cmd(f"{fileName.get()} {'' if condition.get() == ''  else 'IF'} {condition.get()} DO move to {Path.home()}/trash")).grid(row=3, column=3)
    Button(window, text='DELETE', command=lambda : cmd(f"{fileName.get()} {'' if condition.get() == ''  else 'IF'} {condition.get()} DO delete")).grid(row=3, column=4)
    box = Listbox(window, width=70, height=32)
    box.grid(row=4, columnspan=5)
    def view():
        box.delete(0, END)
        for file in cmd(f'{fileName.get()} DO None'):
            box.insert(END, file)
    Button(window, text='VIEW', command=view).grid(row=3, column=0, columnspan=5)
    window.mainloop()
# MAIN
if len(sys.argv) < 2:
    command = ''
    while(command != 'quit'):
            if command != '':
                cmd(command);
            print('\x1b[1;33m' + os.getcwd() + '> ', end='');
            print('\x1b[0;33m', end='');
            command = input().strip();
            print('\x1b[0m', end='');
elif sys.argv[1] == 'gui':
    gui()
else:
    with open(sys.argv[1]) as f:
        for line in f:
            cmd(line)


