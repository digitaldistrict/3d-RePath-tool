import maya.standalone
maya.standalone.initialize("Python")

import argparse
import sys
import os
import maya.cmds as cmds

parser = argparse.ArgumentParser(description='Repath script')
parser.add_argument('--path', '-p', action='store', dest='path', help='Define path of root folder')
parser.add_argument('--backup', '-b', action='store_true', default=False, dest='backup', help='Save file to name_edit.mb')
parser.add_argument('--recursive', '-r', action='store_true', default=False, dest='recursive', help='Recursive search mb file')
parser.add_argument('content', nargs='+', help='First element is search, second is replace; example: C:/ Q:/, it will replace C:/ by Q:/')

args = parser.parse_args()

if not args.path or not args.content:
    print 'Path and content is required'
    sys.exit()

# convert search replace by {'s': search, 'r': replace}
content = [{'s': args.content[i], 'r': args.content[i+1]} for i in range(0, args.content.__len__(), 2)]
files = []

# search files
if args.recursive:
    for root, dirs, f in os.walk(args.path):
        for file in f:
            if file.endswith('.mb'):
                files.append(os.path.join(root, file))
else:
    for file in [f for f in os.listdir(args.path) if f.endswith('.mb')]:
        files.append(os.path.join(args.path, file))
        
if not files:
    print 'Maya file not found (.mb)'
    sys.exit()

for file in files:
    print '> Open file : {0}'.format(file)
    cmds.file(file, force=True, open=True)
    subdir = cmds.filePathEditor(query=True, listDirectories="")
    
    if subdir:
        for d in subdir:
            matching = [c for c in content if c['s'] in d]

            # find path to replace
            if matching:
                match = matching[0]
                print '>> Path to replace : {0}'.format(d)
                
                # get nodes
                nodes = cmds.filePathEditor(query=True, listFiles=d, withAttribute=True)
                nodes = [nodes[i] for i in range(1, nodes.__len__(), 2)]
                
                # repath them
                repath = d.replace(match['s'], match['r'])
                cmds.filePathEditor(*nodes, repath=repath, force=True)

        # rename current file
        if args.backup:
            name, ext = os.path.splitext(file)
            cmds.file(rename=name+'_edit'+ext)

        cmds.file(s=True,f=True)

sys.exit()