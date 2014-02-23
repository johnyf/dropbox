#!/usr/local/bin/python3#
#
# Purpose:   copy/restore windows Desktop.ini files through Dropbox (win, mac, linux)
# Author:    Ioannis Filippidis
# Contact:   jfilippidis@gmail.com
# Date:      2012.06.13 - 2012.10.01
# Python:    3.3
# Licence:   GPLv3, Copyright (c) 2012 Ioannis Filippidis

import sys, shlex, os, time, subprocess, fnmatch

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

def create_delete_dirlinks(filelink, operation):
    if operation in ["-c", "--copy"]:
        path = filelink.replace("Desktop.ini", "");
        path = path.replace("\\", "\\\\")
        
        source = path +"Desktop.ini";
        target = path +"myDesktop.ini";
    elif operation in ["-r", "--restore"]:
        path = filelink.replace("myDesktop.ini", "");
        path = path.replace("\\", "\\\\")
        
        path1 = filelink.replace("\\myDesktop.ini", "");
        path1 = path1.replace("\\", "\\\\")
        
        source = path +"myDesktop.ini";
        target = path +"Desktop.ini";
    else:
        raise sys.exit("Unknown operation. Available operations: -c | --copy | -r | --restore")
	
    print("copying target to source file.")
    args = shlex.split("cp "+source+" "+target);
    p = subprocess.call(args);
    
    print("Set hidden and system attributes of .ini file.")
    args = shlex.split("attrib +H +S "+target);
    p = subprocess.call(args);
    
    if operation in ["-r", "--restore"]:
        print("Set read-only attribute of directory.")
        print(path1)
        args = shlex.split("attrib +R "+path1);
        p = subprocess.call(args);

# main

# any args ?
if len(sys.argv) <= 1:
    raise sys.exit("Input missing. Available operations: -c | --copy | -r | --restore")
    exit()

# operation = ?
if len(sys.argv) >= 2:
    operation = sys.argv[1];
    if operation in ["-h", "--help"]:
        print("desktopini.py [options] [filename],\nwhere: options = -c | --copy | -r | --restore | -h | --help")
        exit();
    else:
        operation = sys.argv[1];

# which file to search for ?
if operation in ["-c", "--copy"]:
    filename = "Desktop.ini";
    print("Files named 'Desktop.ini' will be copied to 'myDesktop.ini'.")
elif operation in ["-r", "--restore"]:
    filename = "myDesktop.ini";
    print("Files named 'myDesktop.ini' will be copied to 'Desktop.ini' (hidden, system file) and their dir becomes a system dir.")
else:
    raise sys.exit("Unknown operation. Available operations: -c | --copy | -r | --restore")

# create | restore Desktop.ini
file_generator = locate(filename, "./");
for file in file_generator:
    flag = 1;
    print("Found file named: ", file)
    create_delete_dirlinks(file, operation)
