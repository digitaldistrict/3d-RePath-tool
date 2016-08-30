# Maya-RePath-tool
Search and replace asset in Maya scene.

## Getting start

- Autodesk Maya 2016 SP4+
- Find your Maya directory (by default C:\Program Files\Autodesk\Maya2016\bin)
- Start command 
```
pathToMaya\bin\mayapy.exe script.py -h
```

## Arguments

| Short   | Long        | Description                                                                              |
|---------|-------------|------------------------------------------------------------------------------------------|
| -p      | --path      | Define path of root folder                                                               |
| -b      | --backup    | Save file to name_edit.mb                                                                |
| -r      | --recursive | Recursive search maya file                                                               |
| content |             | First element is search, second is replace; example: C:/ Q:/, it will replace C:/ by Q:/ |

## Example

```
pathToMaya\bin\mayapy.exe script.py -p 'C:/mayaScene/' -r -b 'C:/oldprojet/' 'C:/mayaScene/' 'D:/object' 'C:/mayaScene/object'
```
In C:/mayaScene search recursively maya scene, open their, search C:/oldproject or D:/object path, if them found replace by C:/mayaScene or C:/mayaScene/object.