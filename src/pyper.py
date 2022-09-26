# pyper.py
"""
python scripting tool, patterned after perl command line
Provide python "one-line" script access, mimicking that of perl
Command line args found in perl will be applied to the pys script,
 e.g. -a,-p - loops over input lines, -e accepst script
 
"""
import sys
import argparse

from files_proc import FilesProc

class PyPer:
    
    def __init__(self, verbose = False):
        """ Setup argument collection
        :verbose: Print info about state default: False - no print
        """
        self.verbose = verbose
        parser = argparse.ArgumentParser()
        parser.add_argument('--py_verbose', dest='py_verbose', action='store_true')
        parser.add_argument('--py_recursive', dest='py_recursive', action='store_true')
        parser.add_argument('-a', dest='perl_opt_a', action='store_true')
        parser.add_argument('-n',  dest='perl_opt_n', action='store_true')
        parser.add_argument('-p',  dest='perl_opt_p', action='store_true')
        parser.add_argument('-e', dest='perl_opt_e', action='append')
        parser.add_argument('files', nargs='*', action='append')
        self.parser = parser
        self.next_line_std_in = None
        self.in_file = None
        self.in_files = []
        
    def parse_args(self, argv):
        """ parse arguments
        :argv: arguments default: use sys.argv
               if not a list use argv.split()
        """
        if self.verbose:
            print("\nargv:", argv)
        if argv is None:
            pargs = self.parser.parse_args()
        else:
            if not isinstance(argv, list):
                argv = argv.split()
            pargs = self.parser.parse_args(argv)
        self.argv = argv
        self.pargs = pargs
        if pargs.py_verbose:
            self.verbose = pargs.py_verbose
        if self.verbose:
            print("parse_args:", pargs)
        self.pargs = pargs
        self.next_line_init(verbose=self.verbose,
                            file_specs=pargs.files,
                            recursive=pargs.py_recursive)

    def next_line(self):
        """ Return next input line
            Acts like perl's <>
        """
        line = self.files_proc.next_line()
        return line

    def next_line_lineno(self):
        return self.files_proc.next_line_lineno()

    def next_line_filename(self):
        return self.files_proc.next_line_filename()
    
    def next_line_init(self, verbose=False, file_specs=None,
                       recursive=False):
        """ Setup for input form files or stdin
        """
        self.files_proc = FilesProc(verbose=verbose)
        self.files_proc.next_line_init(verbose=verbose,
                                       file_specs=file_specs,
                                       recursive=recursive)
        
    def run(self, argv=None):
        """ Parse and run program
        """
        ###if isinstance(argv,list):
        ###    argv = " ".join(argv)
        self.parse_args(argv)
        pgm = self.collect_pgm()
        if self.verbose:
            print("pgm:\n", pgm)
        self.exec_pgm(pgm)    
        
    def exec_pgm(self, pgm):
        """ Executed script (-e...) on files
        """
        import re
        
        global F 
        F = []
        
        global d_
        d_ = None

        def s(pat, rep, count=0):
            """ Replace in d_ all occurances of pat with rep
                Patterned after perl's s/pat/rep/g function
            """
            global d_ # (perl $_)
            global F    # (perl F)
            d_ = re.sub(pat, rep, d_, count)
 
        if self.pargs.perl_opt_n or self.pargs.perl_opt_p:
            while True:
                d_ = line = self.next_line()
                dARGV = self.next_line_filename()
                dd = self.next_line_lineno()
                if line is not None and len(line) > 0:
                    F = line.split()
                else:
                    d_ = ""
                    break
                exec(pgm)
                if self.pargs.perl_opt_p:
                    print(d_, end="")
        else:
            exec(pgm)

    def collect_pgm(self):
        pgm = """
global F
global dP
global d_
"""
        pgm += "".join(self.pargs.perl_opt_e)
        pgm_aug = ""
        sp_per_level = 4        # tab spacing
        depth = 0
        maxi = len(pgm)-1       # index of first of 2 chars
        skip_ch = False
        for i in range(len(pgm)):
            if skip_ch:
                skip_ch = False
                continue        # character already used
            ch1 = pgm[i]
            ch2 = pgm[i+1] if i < maxi else ""
            tok = ch1 + ch2 
            if tok == ';{':
                depth += 1  # start body
                pgm_aug += "\n" + depth*sp_per_level*" "
                skip_ch = True
            elif tok == ';}':
                depth -= 1  # end body
                pgm_aug += "\n" + depth*sp_per_level*" "
                skip_ch = True
            elif tok == ';|':
                pgm_aug += "\n" + depth*sp_per_level*" "
                skip_ch = True
            else:
                pgm_aug += ch1
                skip_ch = False
        return pgm_aug
    
def test_parsing(verbose=False):
    print("Exercising command line parsing")
    verbose = True
    pyp = PyPer(verbose=verbose)
    pyp.parse_args("-ane foo")
    pyp.parse_args("-a")
    pyp.parse_args("-a -p -e bar")
    pyp.parse_args("-ape foo")
    pyp.parse_args("-ape foo -e bar")
    pn = pyp.parse_args("-ape foo file1 file2 file3")
    pn = pyp.parse_args("-ape foo -e bar file1 file2 file3")


def test_files(verbose=False):
    print("Exercising file processing / programming")
    test_name = "test1.pyper" 
    with open(test_name,"w") as pout:
        print(
"""\
line 1  aaaa bbbb cccc
line 2  dddd eeee ffff
line 3  gggg hhhh iiii
""", file=pout, end="")
    test_name2 = "test2.pyper" 
    with open(test_name2,"w") as pout:
        print(
"""\
line 1  aaaa bbbb cccc
line 2  dddd eeee ffff
line 3  gggg hhhh iiii
""", file=pout, end="")
    pyp = PyPer(verbose=verbose)
    pyp.run(f"""-ane print(d_,end="") {test_name} {test_name2}""")

    pyp.run(f"""-ane print(d_,end="")"""
              f""" {test_name} {test_name2}""")

    pyp.run(f"""-ape d_=d_.replace("line","pfoobar")"""
              f""";print(d_,end="")"""
              f""" {test_name} {test_name2}""")
    
    pyp.run(['-ane', """d_=re.sub('[aeiou]{3}','xxx',d_)""",
              "-e", f""";print(d_,end="")""",
              test_name, test_name2])

    pyp.run(['-ape', """d_=re.sub('[aeiou]{3}','xxx',d_)""",
              test_name, test_name2])

    pyp.run(['-ape', """s('[aeiou]{3}','xxx')""",
              test_name, test_name2])

    pyp.run(['-ape','s("aa","bxb")', "test1.pyper"])
    pyp.run(['-e', 'for i in range(4):;{',
             '-e',       'for j in range(3):;{',
             '-e',           'print(i,j);}',
             ])
    pyp.run(['-ape', 'print(dARGV, dd,d_,end="")', "test1.pyper"])
    pyp.run(['-ane', 'print(dARGV, dd,d_,end="")', "test1.pyper", "test2.pyper"])

print("sys.argv:", sys.argv)
verbose=False
tests = "parsing, files"
#tests = "files"
if __name__ == '__main__':
    if len(sys.argv) == 1:
        if "parsing" in tests:
            test_parsing(verbose)
        if "files" in tests:
            test_files(verbose)
        exit(0)

    print("Cmd line run")
    pyper = PyPer()
    pyper.run()
    