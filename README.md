# pyper
Python program to provide some of the features available via perl command line operation
### The following is an MS Windows executable example of some similar perl and pyper.py command lines:
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
