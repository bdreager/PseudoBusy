#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: http://stackoverflow.com/questions/3657103/python-print-not-functioning-correctly-after-using-curses

import os, platform
from printer import Printer, Random

class PseudoBusy():
    MAX_PATIENCE = 6
    MIN_FILE_LENGTH = 1
    MAX_FILE_LENGTH = 5000

    def __init__(self):
        self.rand = Random()
        self.printer = Printer(shift_in_chance=25)
        self.dir = os.path.expanduser('~/')
        self.slash = '\\' if platform.system() is 'Windows' else '/'  # this needs to be tested on windows
        self.running = False

    def start(self):
        self.running = True
        self.run()

    def run(self):
        # TODO search for files deeper on users filesystem

        while self.running:
            self.printer.reset()
            infile = None
            num_lines = 0
            # TODO search in a background thread. Maintain small backlog (10?) of files to print
            while not infile:
                try:
                    infile = self.recurse_pick_file(self.dir)
                    with open(infile, 'r') as ins: ins.readline().decode('ascii')  # for catching junk we don't care to see
                    num_lines = self.bufcount(infile)
                    if num_lines <= self.MIN_FILE_LENGTH: raise Exception('File too small') # for empty and single line files
                    if num_lines >= self.MAX_FILE_LENGTH: raise Exception('File too large') # for massive files (probably not code)
                except Exception, err:
                    infile = None

            self.printer.override_speed = 1000
            self.printer.typing("Reading: "+infile.replace(self.dir, ''))
            self.printer.typing("\nLines: "+str(num_lines)+"\n")
            self.print_file(infile)

    def print_file(self, infile):
        try:
            with open(infile, "r") as ins:
                patience = self.MAX_PATIENCE
                for line in ins:
                    line = line.decode('ascii')  # for catching junk we don't care to see
                    if line.strip():
                        patience = self.MAX_PATIENCE
                    else:
                        patience -= 1
                        if patience <= 0:
                            break;
                    if not self.rand.int(0, 10):  # type a random string as a 'mistake'
                        num = self.rand.int(10, 25)
                        self.printer.typing(self.rand.string(num))
                        self.printer.backspace_delete(num)
                    self.printer.typing(line)
        except: pass

    def recurse_pick_file(self, directory):
        found_file = None
        if self.rand.int(0, 10):
            new_dir = self.rand.dir(directory)
            try:
                found_file = self.recurse_pick_file(directory + self.slash + new_dir) if new_dir else None
            except:
                pass
        if not found_file:
            new_file = self.rand.file(directory)
            found_file = directory  + self.slash + new_file if new_file else None
        if found_file:
            if not os.access(found_file, os.R_OK):
                found_file = None
            # elif not os.path.splitext(file) in self.whitelist:
            #    file = None

        found_file = found_file.replace(self.slash+self.slash, self.slash) # quick fix
        return found_file

    @staticmethod
    def bufcount(filename):
        f = open(filename)
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.read

        buf = read_f(buf_size)
        while buf:
            lines += buf.count('\n')
            buf = read_f(buf_size)

        return lines

if __name__ == '__main__':
    try:
        print Printer.CLEAR
        PseudoBusy().start()
    except:
        print Printer.RESET
        print Printer.CLEAR
