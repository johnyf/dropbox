#!/usr/bin/env python
#
# 2012-2014 (BSD) Ioannis Filippidis
"""
create/delete junctions based on "dirlink" files
(win, mac, linux)
"""
import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger()

import sys
import os
import subprocess
import argparse
import shlex
import fnmatch
import platform

def locate(pattern, root=os.curdir):
    """Recursively find files under given directory matching pattern.
    """
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

def create_delete_dirlinks_darwin(dirlink, args):
    fid = open(dirlink, 'r')
    igot = fid.readlines()
    fid.close()
    
    path = dirlink.replace('dirlink', '')
    path = path.replace('\\', '/')
    logger.debug('current dirlink file in: ' + str(path))
    
    n = 0;
    for line in igot:
        n = n +1
        logger.debug('Line No.' + str(n))
        
        line = line.replace('\\', '/')
        if line.find('target') > -1:
            target = line.replace('target = ', '')
            logger.debug('The target is: ' + target)
        elif line.find('link') > -1:
            junction = line.replace('link = ', '')
            logger.debug('The Link is: ' + junction)
            
            #junction = path + junction
            #target = path + target
            
            target = os.path.expandvars(target)
            
            if args.create:
                args = shlex.split('ln -s ' + target + ' ' + junction);
            elif args.delete:
                args = shlex.split('rm -f -v ' + junction);
            else:
                raise sys.exit(
                    'Unknown operation. '
                    'Available operations: '
                    '-c | --create | -d | --delete'
                )
            
            logger.debug(args)
            subprocess.call(args)

def create_delete_dirlinks_windows(dirlink, args):
    fid = open(dirlink, 'r')
    igot = fid.readlines()
    fid.close()
    
    path = dirlink.replace('dirlink', '')
    path = path.replace('\\', '\\\\')
    logger.info('current dirlink file in: ' + path)
    
    n = 0;
    for line in igot:
        n = n +1
        logger.debug('Line No.' + str(n))
        
        line = line.replace('\\', '\\\\')
        if line.find('target') > -1:
            target = line.replace('target = ', '')
            logger.info('The target is: ' + target)
        elif line.find('link') > -1:
            junction = line.replace('link = ', '')
            logger.info('The Link is :' + junction)
            
            junction = path +junction
            target = path +target
            
            if args.create:
                args = shlex.split('ln1 --junction ' + junction +
                                   ' ' + target)
            elif args.delete:
                args = shlex.split('junction -d ' + junction)
            else:
                raise sys.exit(
                    'Unknown operation. '
                    'Available operations: '
                    '-c | --create | -d | --delete'
                )
            
            subprocess.call(args)

if __name__ == '__main__':
    desc = (
        'locate() is used in case of exporting only to a PDF '
        '(w/o latex export). '
        'Only in that case \includegraphics{} is still '
        'able to find the PDF without a path. '
        'If latex export is used, '
        'then the produced .pdf_tex should be used, '
        'with an \input{} command in latex and '
        'a relative path is mandatory for '
        'the \input{} command to work.'
    )
    
    parser = argparse.ArgumentParser(description=desc)
    
    g = parser.add_mutually_exclusive_group()
    
    g.add_argument('-c', '--create', help='add symbolic links',
                    action='store_true')
    g.add_argument('-d', '--delete', help='erase symbolic links',
                    action='store_true')
    
    parser.add_argument('-f', '--filename', help='filename',
                        default='dirlink')
    parser.add_argument('-v', '--verbose', help='increase output verbosity',
                    action='store_true')
    
    args = parser.parse_args()
    
    # no args ?
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    filename = args.filename
    logger.debug('instruction in filename = ' + str(filename))
    
    # create or delete junctions
    file_generator = locate(filename, './')
    osname = platform.system()
    for f in file_generator:
        flag = 1
        logger.debug('Found file named: ' + str(f))
        
        if osname == 'Darwin':
            create_delete_dirlinks_darwin(f, args)
        else:
            create_delete_dirlinks_windows(f, args)
