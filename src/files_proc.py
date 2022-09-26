#files_proc.py    24Sep2022  crs, Author
"""
Process files, facilitating traverse files, lines
Initially supporting pyper.py processing command line
files specifications as done by perl in a Linux/unix 
style in a Windows shell Environment 
"""
import sys
import argparse
import glob 
from Lib.pickle import TRUE

class FilesProc:
    def __init__(self, verbose=False, recursive=False):
        """ Setup file processing 
        :verbose: show processing default: false 
        :recursive: look recursively in folders default:False 
        """
        self.verbose = verbose
        self.recursive = recursive
        self._next_line_lineno = 0
        
    def get_files(self, verbose=False, file_specs=None, recursive=False):
        """ get files specified
        :verbose: show process default: no change in 
        :file_specs: file specification
            None - use sys.argv files
            str - use argv.split()
            list - use list
        :recursive: search recursively for files default:False
                If True overrides __init__
        """
        if verbose:
            self.verbose = verbose
        if recursive:
            self.recursive = recursive
        if file_specs is None:
            parser = argparse.ArgumentParser()
            parser.add_argument('--verbose', dest='verbose', action='store_true')
            parser.add_argument('file_specs', nargs='*', action='append')
            pargs = parser.parse_args()
            """ Hack to produce [,,,] instead if [[,,,]]
            """
            if pargs.file_specs is not None:
                if isinstance(pargs.file_specs, list) and len(pargs.file_specs)==1:
                    pargs.file_specs = pargs.file_specs[0]
                file_specs = pargs.file_specs
            if pargs.verbose:
                self.verbose = pargs.verbose
            if self.verbose:
                print("parse_args:", pargs)
        else:
            if isinstance(file_specs, str):
                file_specs = file_specs.split()
            else:
                if not isinstance(file_specs,list):
                    file_specs = list(file_specs)
                else:
                    # A HACK to overcome [[]] served up by argparse *
                    if len(file_specs)==1 and isinstance(file_specs[0],list):
                        file_specs = file_specs[0]
            if self.verbose:
                print("file_specs:", file_specs)
        all_files = []
        for file_spec in file_specs:
            arg_files = glob.glob(file_spec, recursive=self.recursive)
            all_files += arg_files
        return all_files

    def next_line_init(self, verbose=False, file_specs=None, recursive=False):
        """ Setup line by line processing, using get_line
        """
        files = self.get_files(verbose=verbose, file_specs=file_specs,
                               recursive = recursive)
        
        next_line_stdin = True if len(files) == 0 else False
        self.next_line_stdin = next_line_stdin
        self.in_file_name = "-"

        self._next_line_lineno = 0
        self.in_files = files
        self.in_file = None     # Current open input file ptr
        
        
    def next_line(self):
        """ Return next line, including newline, from file list
            EOF returns ""
            sets self.file_name on each new file
            Acts like perl's <>
        """
        if self.next_line_stdin:
            inp = sys.stdin.readline()
        else:
            inp = None
            while len(self.in_files)>0 or self.in_file is not None:
                if self.in_file is None:
                    if len(self.in_files) > 0:
                        self.in_file_name = self.in_files.pop(0)
                        self.in_file = open(self.in_file_name)
                        self._next_line_lineno = 0
                        continue        # Use new file
                    else:
                        inp = None 
                        break       # No input left
                else:                    
                    inp = self.in_file.readline()
                    if len(inp) == 0:
                        if self.verbose:
                            print(self.in_file_name, "EOF")
                        self.in_file.close()
                        self.in_file = None     # Flag used
                        inp = None
                        continue                # Check for file
                    else:
                        self._next_line_lineno += 1
                    break           # use line
        return inp

    def next_line_lineno(self):
        """ get lineno of current file
        """
        return self._next_line_lineno

    def next_line_filename(self):
        """ Get current file name
        """
        return self.in_file_name
    
if __name__ == '__main__':
    verbose = True
    def test_spec_files(fspec, recursive=False):
        """ Exercise file specification
        :fspec: file spec strint, list
        :recursive: search folders recursively
        """
        fp = FilesProc(verbose=verbose, recursive=recursive)
        files = fp.get_files(file_specs=fspec)
        print(f"fspec:{fspec} {len(files)} files")
        for file in files:
            print(f"    {file}")
    
    tests = "basic, recursive"
    tests = "recursive"
    if "basic" in tests:
        test_spec_files("*.py")
        test_spec_files("*.*")
        test_spec_files("../../*.*")
        test_spec_files("../../*.*")
        test_spec_files("../../*proj/src/*.py")
        test_spec_files("../../r*proj/src/*")
    if "recursive" in tests:
        test_spec_files("pyper_test/*.*", recursive=True)
        test_spec_files("pyper_test/*.txt", recursive=True)
        test_spec_files(r"pyper_test\*.txt", recursive=True)
                    