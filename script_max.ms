/* -------- REPLACE HERE --------- */

theRootPath = "Q:\pathTo"
edt = #(
    DataPair find:"p:" replace:"q:\\",
    DataPair find:"\\\\data-server" replace:"q:\\"
)

/* ------------------------------ */

fn getFilesRecursive root pattern =(

    dir_array = GetDirectories (root+"/*")
    for d in dir_array do
    (
        join dir_array (GetDirectories (d+"/*"))
    )

    append dir_array (root + "/")		
    theFileList = #()
    for f in dir_array do
    (
        join theFileList (getFiles (f + pattern))
    )

    theFileList 
)

theRepathFileList = getFilesRecursive theRootPath "*.max"

for theMaxFile in theRepathFileList do 
(
    metaArray = getMAXFileAssetMetadata theMaxFile
    if metaArray != undefined 
    then
    (
        for x = 1 to metaArray.count do
        (
            fName = toLower (metaArray[x].filename)

            format "Asset: %\n" fName
            
            for el in edt do
            (
                if matchpattern fName pattern:(el.find +"*") ignorecase:false
                then 
                (
                    newFName = substituteString fName el.find el.replace
                    metaArray[x].filename = newFName
                    format "Replacing % \n   with % \n" fname newFName
                )
                else
                (
                    format "No Matching Path String\n"
                )
            )
        )
        setMAXFileAssetMetadata theMaxFile metaArray
    )

    else (format "File contains no Meta Data or is corrupt")
)