#!/usr/bin/env python
#
# 2012-2014 (BSD) Ioannis Filippidis
"""
create/delete junctions based on "dirlink" files
(win, mac, linux)
"""

import sys, shlex, os, time, subprocess, fnmatch, platform

# locate() is used in case of exporting only to a .pdf (w/o latex export)
# Only in that case \includegraphics{} is still able to find the .pdf
# without a path.
# If latex export is used, then the produced .pdf_tex should be used
# with an \input{} command in latex and a relative path is mandatory for
# the \input{} command to work.
def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)
#

def create_delete_dirlinks_darwin(dirlink, operation):
    fid = open(dirlink, "r")
    igot = fid.readlines()
    fid.close()
    
    path = dirlink.replace("dirlink", "");
    path = path.replace("\\", "/")
    #print("current dirlink file in: "+path)
    
    n = 0;
    for line in igot:
        n = n +1;
        #print("Line No.", n)
        line = line.replace('\\', "/");
        if line.find("target") > -1:
            target = line.replace("target = ", "");
            #print("The target is: "+target)
        elif line.find("link") > -1:
            junction = line.replace("link = ", "");
            #print("The Link is :"+junction)
            
            junction = path +junction;
            target = path +target;
            
            if operation in ["-c", "--create"]:
                args = shlex.split("ln -s "+target+" "+junction);
            elif operation in ["-d", "--delete"]:
                args = shlex.split("rm -f -v "+junction);
            else:
                raise sys.exit("Unknown operation. Available operations: -c | --create | -d | --delete")
            
            p = subprocess.call(args);

def create_delete_dirlinks_windows(dirlink, operation):
    fid = open(dirlink, "r")
    igot = fid.readlines()
    fid.close()
    
    path = dirlink.replace("dirlink", "");
    path = path.replace("\\", "\\\\")
    #print("current dirlink file in: "+path)
    
    n = 0;
    for line in igot:
        n = n +1;
        #print("Line No.", n)
        line = line.replace('\\', "\\\\");
        if line.find("target") > -1:
            target = line.replace("target = ", "");
            #print("The target is: "+target)
        elif line.find("link") > -1:
            junction = line.replace("link = ", "");
            #print("The Link is :"+junction)
            
            junction = path +junction;
            target = path +target;
            
            if operation in ["-c", "--create"]:
                args = shlex.split("ln1 --junction "+junction+" "+target);
            elif operation in ["-d", "--delete"]:
                args = shlex.split("junction -d "+junction);
            else:
                raise sys.exit("Unknown operation. Available operations: -c | --create | -d | --delete")
            
            p = subprocess.call(args);

def save_dirlinks(dirlink):
    print("Saving not yet implemented. Please do this manually for now.")

# main

# any args ?
if len(sys.argv) <= 1:
    raise sys.exit("Input missing. Available operations: -c | --create | -d | --delete")
    exit()

# operation = ?
if len(sys.argv) >= 2:
    operation = sys.argv[1];
    if operation in ["-h", "--help"]:
        print("junctions.py [options] [filename],\nwhere: options = -c | --create | -d | --delete | -l | --list | -h | --help")
        exit();
    else:
        operation = sys.argv[1];

# filename = ? | default
if len(sys.argv) >= 3:
    filename = sys.argv[2];
else:
    filename = "dirlink"; # default

#print("instruction in filename = "+filename+", operation = "+operation)

# log newly appeared junctions in dirlink files
if operation in ["-s", "--save"]:
    save_dirlinks(filename)
    exit()

# list junctions recursively
if operation in ["-l", "--list"]:
    args = shlex.split("junction -s");
    p = subprocess.call(args);
    exit()

# create | delete junctions
file_generator = locate(filename, "./");
osname = platform.system();
for file in file_generator:
    flag = 1;
    #print("Found file named: ", file)
    if osname == "Darwin":
        create_delete_dirlinks_darwin(file, operation)
    else:
        create_delete_dirlinks_windows(file, operation)
