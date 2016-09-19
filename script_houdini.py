import argparse
import sys
import os
import subprocess
import time

parser = argparse.ArgumentParser(description='Houdini Repath script')
parser.add_argument(
    '--path', '-p', 
    action='store', 
    dest='path', 
    help='Define path of root folder', 
    required=True)
parser.add_argument(
    '--houdini', '-hou', 
    action='store', 
    dest='houdini', 
    help='Define path of houdini by default : C:\\Program Files\\Side Effects Software\\', 
    default='C:\\Program Files\\Side Effects Software\\')
parser.add_argument(
    '--backup', '-ba', 
    action='store_true', 
    default=False, 
    dest='backup', 
    help='Save file to name_edit.hip')
parser.add_argument(
    '--recursive', '-r', 
    action='store_true', 
    default=False, 
    dest='recursive', 
    help='Recursive search hip file')
parser.add_argument(
    '--max', '-m',
    action='store',
    default=2,
    dest='max',
    type=int,
    help='Maximum Houdini instance in parallel')
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
                if file.endswith('.hip'):
                    files.append(os.path.join(root, file))
    else:
        for file in [f for f in os.listdir(args.path) if f.endswith('.hip')]:
            files.append(os.path.join(args.path, file))

    if not files:
        print 'Houdini file not found (.hip)'
        sys.exit()
        
    return files

def getHoudiniVersion(args):
    dirs = os.listdir(args.houdini)
    listHoudini = {}
    
    for d in dirs:
        if os.path.isfile(os.path.join(args.houdini, d, 'bin', 'hython.exe')):
            listHoudini[d.split(' ')[1].strip()] = os.path.join(args.houdini, d)
    
    if not listHoudini:
        print 'Houdini folder not found, use --houdini'
        sys.exit()
        
    return listHoudini

def getFileVersion(file):
    with open(file, "rb") as f:
        word = ''
        waitVersion = False
        byte = f.read(1)
        
        while byte != "":
            if byte != ' ':
                word += byte
            else:
                if waitVersion and word != '=':
                    return word.split("'")[1]

                if word == '_HIP_SAVEVERSION':
                    waitVersion = True

                word = ''

            byte = f.read(1)
            
    return False

def selectHoudiniVersion(listHoudini, version):
    find = False
    
    for key in listHoudini:
        if key == version:
            return listHoudini[key]
    
    if not find:
        sepVer = version.split('.')
        for key in listHoudini:
            sepDir = key.split('.')
            
            if sepDir[0] == sepVer[0] and sepDir[1] == sepVer[1]:
                return listHoudini[key]
            
    return False
    

print 'Search in progress...'

files = getSceneFile(args)
listHoudini = getHoudiniVersion(args)

print '{0} files founded'.format(files.__len__())

# convert search replace by {'s': search, 'r': replace}
content = [
    {'s': args.content[i].replace('\\', '/'), 'r': args.content[i+1].replace('\\', '/')} 
    for i in range(0, args.content.__len__(), 2)
]

currentNum = 0 # current file pos
Processes = [] # instance in progress

def startScript(file):
    file = file.replace('\\', '/')
    version = getFileVersion(file)
    
    if not version:
        print 'Can\'t find version of {0}'.format(file)
        return False
    
    houdini = selectHoudiniVersion(listHoudini, version)
    
    if not houdini:
        print 'Not find version Houdini {0}'.format(version)
        return False
        
    houdini = os.path.join(houdini, 'bin', 'hython.exe')
    
    return subprocess.Popen([houdini, '-c', """
import hou
import os
import sys

file = "{f}"
content = {c}
backup = {b}
print '> Open file : {{0}}'.format(file)

try:
    hou.hipFile.load(file_name=file, ignore_load_warnings=True)
except:
    print 'Cant open this file.'
    sys.exit()

for c in content:
    try:
        hou.hscript("opchange -i {{0}} {{1}}".format(c['s'], c['r']))
    except:
        print 'Cant replace {{0}} by {{1}}'.format(c['s'], c['r'])

if backup:
    name, ext = os.path.splitext(file)
    hou.hipFile.save(file_name=name+'_edit'+ext)
else:
    hou.hipFile.save()
    
sys.exit()
""".format(f=file, c=content, b=args.backup)])

def startNew():
    global currentNum
    global Processes
    
    if currentNum < len(files):
        proc = startScript(files[currentNum])
        currentNum += 1
        if proc:
            Processes.append(proc)

def checkRunning():
    global currentNum
    global Processes
    
    # remove ended processes
    for p in range(len(Processes)-1,-1,-1):
        if Processes[p].poll() is not None: 
            del Processes[p]
    
    while (len(Processes) < args.max) and (currentNum < len(files)):
      startNew()

checkRunning()
while (len(Processes) > 0):
    time.sleep(0.1)
    checkRunning() 

sys.exit()
