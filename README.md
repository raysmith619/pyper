# pyper
### PROTOTYPE - UNTESTED - FOR DEMO or DISCUSSION PURPOSES ONLY
pyper.py is a Python program to facilitate perl-like "one-liner" command support.  
    pyper.py provides many of the useful features available via perl command line operation while retaining the utility of the python language.  pyper.py executes on a Microsoft Windows command line.  Most of the difficulty in using python as a command line vehicle is that python uses indentation as the statement grouping construct.  This has been addressed by using several short character sequence tokens to group statements, while remaining on one line.  The current choices are ";{" to start a statement group and ";}" to complete a statement group.  The token ";|" is available, to force a statement separation.  This appears to be necessary in a few cases where the "on-line" separator ";" does not work (see below).  My target goal is only supporting command line "one-liners".  More complex coding should use a program file.

#### Currently supported are perl command line options: (-a, -n, -p, -e).
- -a - split input line by whitespace into array F
- -e - python script to be executed, multiple -e scripts are seamlessly joined as one script
- -n - script is interpreted as the body of a loop over each line of all files
- -p - loop as in "-n" but input line, possibly modified, is printed

#### Supported variables are:
- d_ - (== perl $_) input line, including newline
- dd - (== perl $.) current file's line number
- dARGV (== perl $ARGV) current file name

#### Scripts are standard python with the following additions:
- ;{ - Start conditional body : converted to newline plus indentation
- ;} - complete conditional body : converted to newline with one less indentation
- ;| - forces new statement line : converted to newline with current indentation  
The token ";|" was added because statements such as ```rp=re.search(...);if rp: print(rp.group(1), '==>', d_)``` would not compile under python.

#### The following is an MS Windows executable example of some similar perl and pyper.py command lines:
```
REM Finding print statements, using -n option
REM C:\Users\raysm\workspace\python\pyper\src>

REM perl: (Note that I could not find a way to escape ">")
perl -ane "if (/print(\([^)]*\))/) {print(\"$1 ==- $_\n\")}" pyper.py

REM pyper:
pyper.py --py_verbose -ane "rp=re.search(r'print([^)]*\))',d_);|if rp: print(rp.group(1), '==>', d_)" pyper.py

REM Double loops

REM perl
perl -e "for ($i=1; $i<4;$i++) {for ($j=1; $j<5;$j++) {$p=$i*$j;print \" i: $i j: $j $\\n\"}}"

REM pyper:
REM pyper.py -e "for i in range(1,4):;{for j in range(1,5):;{print('i:',i,'j:',j,i*j);};}"
```
##### Notes
- Because of MS Windows/DOS command line limitations plus perl's interpretation of single quotes we used double quotes(") to enclose -e scripts and backslash escaped double quotes (\
