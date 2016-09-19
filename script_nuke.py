import argparse
import sys
import os
import subprocess
import time

from tempfile import mkstemp
from shutil import move

parser = argparse.ArgumentParser(description='Repath script')
parser.add_argument(
    '--path', '-p', 
    action='store', 
    dest='path', 
    help='Define path of root folder', 
    required=True)
parser.add_argument(
    '--backup', '-ba', 
    action='store_true', 
    default=False, 
    dest='backup', 
    help='Save file to name_edit.nk')
parser.add_argument(
    '--recursive', '-r', 
    action='store_true', 
    default=False, 
    dest='recursive', 
    help='Recursive search nk file')
parser.add_argument(
    '--exclude', '-e', 
    nargs='+', 
    default=[],
    help='Exclude folder for recursion')
parser.add_argument(
    '--content', '-c',
    nargs='+', 
    help='First element is search, second is replace; example: C:/ Q:/, it will replace C:/ by Q:/')

args = parser.parse_args()
args.path = args.path.replace('\\', '/')

def getSceneFile(args):
    files = []
    
    # search files
    if args.recursive:
        for root, dirs, f in os.walk(args.path):
            dirs[:] = [d for d in dirs if d not in args.exclude]
                
            for file in f:
                if file.endswith('.nk'):
                    el = root + '/' + file
                    el = el.replace('\\', '/')
                    files.append(el)
    else:
        for file in [f for f in os.listdir(args.path) if f.endswith('.nk')]:
            el = args.path + '/' + file
            el = el.replace('\\', '/')
            files.append(el)

    if not files:
        print 'Nuke file not found (.nk)'
        sys.exit()
        
    return files

def replace(file_path, content, backup=False):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                for el in content:
                    line = line.replace(el['s'], el['r'])
                new_file.write(line)
                
    os.close(fh)
    
    if not backup:
        os.remove(file_path)
        move(abs_path, file_path)
    else:
        name, ext = os.path.splitext(file_path)
        move(abs_path, name+'_edit'+ext)

print 'Search in progress...'

files = getSceneFile(args)

print '{0} files founded'.format(files.__len__())

# convert search replace by {'s': search, 'r': replace}
content = [
    {'s': args.content[i].replace('\\', '/'), 'r': args.content[i+1].replace('\\', '/')} 
    for i in range(0, args.content.__len__(), 2)
]
  
for f in files:
    replace(f, content, args.backup)
    
sys.exit()
