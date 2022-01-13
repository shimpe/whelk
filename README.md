# whelk
tool to extract schelp files from supercollider documents

# usage:

## Get an overview of commmand line options
```
python3 whelk.py -h 
```
## Process single file 

The schelp file will have the same name as the .sc or .scd file you pass to -i
```
python3 whelk -i path/to/Classes/SomeFile.sc -o path/to/HelpSource/Classes/
```

## Process entire folder of files via wildcards

The schelp files will have the same name as the .sc or .scd file it was extracted from, but with extension .schelp

```
python3 whelk.py -i "path/to/Classes/*.sc" -o path/to/HelpSource/Classes/
```
