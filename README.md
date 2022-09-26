# pyper
Python program to provide some of the features available via perl command line operation.  pyper.py executes on a Microsoft Windows command line.  My hope is to provide much of the convenience of the perl command line operation while supporting the use of most of the python language.  It seams that the most serious difficulty in using python as a command line vehicle is that python uses indentation as the grouping construct.  I addressed this by finding character sequences which might be used to do this on one line.  My current choices are ";{" to start a statement group, ";}" to complete a statement group, and ";|" to force a statement separation (see below).  Note my target is command line "one-liners" only.  More complex coding should use a program file.

#### Currently supported are perl command line options: (-a, -n, -p, -e).
#### Supported variables are:
```
d_ == perl $_
dd == perl $.
dARGV == perl $ARGV
```
#### Scripts are standard python with the following additions:
#### ;{ - Start conditional body : converted to newline plus indentation
#### ;} - complete conditional body : converted to newline with one less indentation
#### ;| - forces new statement line : converted to newline with current indentation
##### ;| was added because statements such as ```rp=re.search(...);if rp: print(rp.group(1), '==>', d_)``` would not compile under python.

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
