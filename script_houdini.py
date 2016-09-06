import hou
import argparse
import sys
import os

parser = argparse.ArgumentParser(description='Houdini Repath script')
parser.add_argument('--path', '-p', action='store', dest='path', help='Define path of root folder')
parser.add_argument('--backup', '-ba', action='store_true', default=False, dest='backup', help='Save file to name_edit.hip')
parser.add_argument('--recursive', '-r', action='store_true', default=False, dest='recursive', help='Recursive search hip file')
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
            if file.endswith('.hip'):
                files.append(os.path.join(root, file))
else:
    for file in [f for f in os.listdir(args.path) if f.endswith('.hip')]:
        files.append(os.path.join(args.path, file))
        
if not files:
    print 'Houdini file not found (.hip)'
    sys.exit()

for file in files:
    print '> Open file : {0}'.format(file)
    
    try:
        hou.hipFile.load(file_name=file, ignore_load_warnings=True)
    except:
        print 'Can\'t open this file.'
        continue
    
    for c in content:
        try:
            hou.hscript("opchange -i {0} {1}".format(c['s'], c['r']))
        except:
            print 'Can\'t replace {0} by {1}'.format(c['s'], c['r'])
    
    if args.backup:
        name, ext = os.path.splitext(file)
        hou.hipFile.save(file_name=name+'_edit'+ext)
    else:
        hou.hipFile.save()

sys.exit()
