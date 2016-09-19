# 3d-RePath-tool
Search and replace asset in 3D software (Maya, 3dsMax, Houdini, Nuke).

## 3dsMax

- Autodesk 3dsMax 2010+
- script find here http://www.scriptspot.com/3ds-max/scripts/batch-asset-re-path-tool
- No open file required, but 3dsMax need to be launched

### How To Use
- Drag&Drop script into 3dsMax
- Search your "Root Folder..." where search .max files
- "Collect/Refresh Asset Paths" for find files and list unique path
- Double click an path or write what you need to find
- Fill the value "Replace" 
- Start "RePath" for submit, but pay attention to manually backup your file

### How To Verify

- Max Application Menu > References > Asset Tracking

### No GUI script

- script_max.ms replace path at line 3, and edit DataPair for right replace.
```
/* you're path */
theRootPath = "Q:\pathTo" 

/* add or remove line for multiple replace (search is case sensitive) */
edt = #(
    DataPair find:"p:" replace:"q:\\",
    DataPair find:"\\\\data-server" replace:"q:\\"
)
```
- Open 3dsMax open script editor, paste content of script_max.ms and evaluate them

## Maya

- Python 2.7
- Autodesk Maya 2016 SP4+
- use script_maya.py

### How To Use

- Start command 
```
python script_maya.py -h
```

### Set Maya Folder

- Find your Maya directory (by default C:\Program Files\Autodesk\Maya2016\)
- If Maya isn't here, add -ma --maya flag with right folder

### How To Verify

- Windows > General Editors > File Path Editor

### Example

```
python script_maya.py -p "C:\mayaScene" -r -c "C:\oldprojet" "C:\mayaScene" "D:\object" "C:\mayaScene\object"
```
Search into C:\mayaScene recursively maya scene, open them, search C:\oldproject or D:\object path, if it found them, then replace by C:\mayaScene or C:\mayaScene\object.

## Houdini

- Python 2.7
- use script_houdini.py

### How To Use

- start command
```
python script_houdini.py -h
```

### Set Houdini Folder

- Find your Houdini directory (by default C:\Program Files\Side Effects Software\)
- If Houdini isn't here, add -h --houdini flag with right folder

### How To Verify

- Render > Pre-Flight Scene...

### Example

```
python script_houdini.py -p "C:\houdini" -r -c "C:\oldprojet" "C:\houdini" "D:\object" "C:\houdini\object"
```
Search into C:\houdini recursively houdini scene, open them, replace all occurences C:\oldproject by C:\houdini and D:\object by C:\houdini\object.
It will open right version of Houdini for open and save your file.

## Nuke

- Python 2.7
- use script_nuke.py

### How To Use

- start command
```
python script_nuke.py -h
```

### Example

```
python script_nuke.py -p "C:\nuke" -r -c "//data-server" "Q:" "P:" "Q:"
```
Search into C:\nuke recursively nuke scene, open them, replace all occurences //data-server by Q: and P: by Q:.

## Arguments for Python script

| Short   | Long        | Description                                                                                         |
|---------|-------------|-----------------------------------------------------------------------------------------------------|
| -p      | --path      | Define path of root folder                                                                          |
| -ba     | --backup    | Save file to name_edit.ext                                                                          |
| -r      | --recursive | Recursive search scene file                                                                         |
| -e      | --exclude   | Eclude folder by name; example: -e backup back_save, it will ignore "backup" folder and "back_save" |
| -h      | --houdini   | Houdini folder                                                                                      |
| -ma     | --maya      | Maya folder                                                                                         |
| -m      | --max       | Maximum instance in parallel (Maya and Houdini)                                                     |
| -c      | --content   | First element is search, second is replace; example: -c C:/ Q:/, it will replace C:/ by Q:/         |
