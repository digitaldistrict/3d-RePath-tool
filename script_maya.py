import argparse
import sys
import os
import subprocess
import time

parser = argparse.ArgumentParser(description='Repath script')
parser.add_argument(
    '--path', '-p', 
    action='store', 
    dest='path', 
    help='Define path of root folder', 
    required=True)
parser.add_argument(
    '--maya', '-ma', 
    action='store', 
    dest='maya', 
    help='Define path of maya by default : C:\\Program Files\\Autodesk\\Maya2016\\', 
    default='C:\\Program Files\\Autodesk\\Maya2016\\')
parser.add_argument(
    '--backup', '-ba', 
    action='store_true', 
    default=False, 
    dest='backup', 
    help='Save file to name_edit.mb')
parser.add_argument(
    '--recursive', '-r', 
    action='store_true', 
    default=False, 
    dest='recursive', 
    help='Recursive search mb file')
parser.add_argument(
    '--max', '-m',
    action='store',
    default=2,
    dest='max',
    type=int,
    help='Maximum Maya instance in parallel')
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
                if file.endswith('.mb'):
                    el = root + '/' + file
                    el = el.replace('\\', '/')
                    files.append(el)
    else:
        for file in [f for f in os.listdir(args.path) if f.endswith('.mb')]:
            el = args.path + '/' + file
            el = el.replace('\\', '/')
            files.append(el)

    if not files:
        print 'Houdini file not found (.mb)'
        sys.exit()
        
    return files

files = getSceneFile(args)

# convert search replace by {'s': search, 'r': replace}
content = [
    {'s': args.content[i].replace('\\', '/'), 'r': args.content[i+1].replace('\\', '/')} 
    for i in range(0, args.content.__len__(), 2)
]

currentNum = 0 # current file pos
Processes = [] # instance in progress
procfiles = [] # file of instance

if not args.maya or not os.path.isfile(os.path.join(args.maya, 'bin', 'mayapy.exe')):
    print 'Maya folder not found, use --maya'
    sys.exit()

args.maya = os.path.join(args.maya, 'bin', 'mayapy.exe')
    
def startScript(file):
    
    print '> Open file : {0}'.format(file)
    
    with open(os.devnull, 'w') as devnull:
        return subprocess.Popen([args.maya, '-c', """
import maya.standalone
maya.standalone.initialize("Python")

import maya.cmds as cmds  
import sys
import os

file = "{f}"
content = {c}
backup = {b}
#print '> Open file : {{0}}'.format(file)

try:
    cmds.file(file, force=True, open=True, ignoreVersion=True)
except:
    print 'Cant open this file.'
    cmds.quit()
    sys.exit()

# disable reference
refs = cmds.file(q=True, r=True)
refsName = []

for ref in refs:
    namespace = cmds.referenceQuery(ref, referenceNode=True)
    refsName.append(namespace)
    cmds.file(unloadReference=namespace)

subdir = cmds.filePathEditor(query=True, listDirectories="")

if subdir:
    for d in subdir:
        matching = [c for c in content if c['s'] in d]

        # find path to replace
        if matching:
            match = matching[0]
            print '>> Path to replace : {{0}}'.format(d)

            # get nodes
            try:
                nodes = cmds.filePathEditor(query=True, listFiles=d, withAttribute=True)
                nodes = [nodes[i] for i in range(1, nodes.__len__(), 2)]
            except:
                print 'Cant find node path'
                cmds.quit()
                sys.exit()

            # repath them
            repath = d.replace(match['s'], match['r'])

            try:
                cmds.filePathEditor(*nodes, repath=repath, force=True)
            except:
                print 'Cant replace path by {{0}}'.format(repath)
                cmds.quit()
                sys.exit()

    # try to enable reference
    for namespace in refsName:
        try:
            cmds.file(loadReference=namespace)
        except:
            pass

    # rename current file
    if backup:
        name, ext = os.path.splitext(file)
        cmds.file(rename=name+'_edit'+ext)

    try:
        cmds.file(s=True,f=True)
    except:
        pass
    
cmds.quit()
sys.exit()
""".format(f=file, c=content, b=args.backup)], stderr=devnull, stdout=devnull)

def startNew():
    global currentNum
    global Processes
    global procfiles
    
    if currentNum < len(files):
        proc = startScript(files[currentNum])
        if proc:
            Processes.append(proc)
            procfiles.append(files[currentNum])
            
        currentNum += 1

def checkRunning():
    global currentNum
    global Processes
    global procfiles
    
    # remove ended processes
    for p in range(len(Processes)-1,-1,-1):
        if Processes[p].poll() is not None: 
            if Processes[p].poll() == 1:
                print 'Maya crashes for file {0}'.format(procfiles[p])
                
            del Processes[p]
            del procfiles[p]
    
    while (len(Processes) < args.max) and (currentNum < len(files)):
      startNew()

checkRunning()
while (len(Processes) > 0):
    time.sleep(0.1)
    checkRunning() 

sys.exit()
