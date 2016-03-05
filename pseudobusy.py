#!/usr/bin/env python
# -*- coding: utf-8 -*-

__program__ = 'PseudoBusy'
__version__ = '1.0.0'
__description__ = 'Terminal vomit'
__author__ = 'Brandon Dreager'
__author_email__ ='pseudobusy@subol.es'
__copyright__ = 'Copyright (c) 2016 Brandon Dreager'
__license__ = 'MIT'
__website__ = 'https://github.com/Regaerd/PseudoBusy'

import os
from printer import Printer, Random
from argparse import ArgumentParser

class PseudoBusy():
    MAX_PATIENCE = 6
    MIN_FILE_LENGTH = 1
    MAX_FILE_LENGTH = 5000
    MAX_FILE_SIZE = 100000000 # 100 MB
    MAX_CHARS_PER_LINE = 1000 # avoids heavily compressed files

    def __init__(self, args=None):
        self.args = args
        self.rand = Random()
        self.printer = Printer(shift_in_chance=25)
        self.target_dir = os.path.expanduser('~/')
        self.hide_target = True
        self.running = False

    def start(self):
        print (self.printer.CLEAR)
        self.running = True
        self.printer.write('Generating file list... ', speed=1)
        # TODO whitelist and blacklist
        self.files = [os.path.join(path, filename) for path, dirs, files in os.walk(self.target_dir) for filename in files]
        self.original_num_files = len(self.files)
        self.printer.write('Found {} files'.format(self.original_num_files))

        if self.args.reject_first:
            self.printer.write('\nChecking all files... ', speed=1)
            for i in xrange(self.original_num_files - 1, -1, -1):
                self.pick_file(i)
            self.printer.write('Rejected {} files'.format(self.original_num_files - len(self.files)))

        self.run()

    def run(self):
        while self.running:
            try:
                self.printer.reset()
                file, num_lines, size = self.pick_file()

                if self.args.typing_speed: self.printer.override_speed = self.args.typing_speed
                self.log(1, "Reading: "+file.replace(self.target_dir, '') if self.hide_target else file)
                self.log(2, "\nBytes:{}, Lines:{}, Rejects:{}\n".format(size,num_lines,self.original_num_files - len(self.files)))
                self.print_file(file)
            except KeyboardInterrupt:
                self.running = False

    def print_file(self, infile):
        try:
            with open(infile) as file:
                lines = file.readlines()

            patience = self.MAX_PATIENCE
            for line in lines:
                line = line.decode('ascii')  # hides garbage
                if line.strip():
                    patience = self.MAX_PATIENCE
                else:
                    patience -= 1
                    if patience <= 0:
                        break;
                if not self.rand.int(0, 10):  # type a random string as a 'mistake'
                    num = self.rand.int(10, 25)
                    self.printer.write(self.rand.string(num))
                    self.printer.backspace_delete(num)
                self.printer.write(line)
        except (Exception) as err:
            self.log(3, str(err)+'\n')

    def pick_file(self, index=None):
        file = num_lines = size =  None
        while not file:
            try:
                file = self.files[index] if index else self.rand.choice(self.files)
                size = os.path.getsize(file)
                if size >= self.MAX_FILE_SIZE: raise  Exception('File too large')
                if not os.access(file, os.R_OK): raise Exception('No read access')
                with open(file, 'r') as ins:
                    ins.readline().decode('ascii')  # for catching junk we don't care to see
                    num_lines = sum(1 for _ in ins) + 1

                if size / num_lines >= self.MAX_CHARS_PER_LINE: raise Exception('Too many characters per line')
                if num_lines <= self.MIN_FILE_LENGTH: raise Exception('Too few lines') # for empty and single line files
                if num_lines >= self.MAX_FILE_LENGTH: raise Exception('Too many lines') # for massive files (probably not code)
            except (Exception) as err:
                self.log(3, str(err)+'\n')
                self.files.remove(file) # we don't need to see rejects again
                file = None
                if index: break

        return (file, num_lines, size)

    def log(self, level, string):
        if (level <= self.args.verbose): self.printer.write(string)

def init_args():
    parser = ArgumentParser(prog=__program__, description=__description__)
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-v', '--verbose-level', type=int, default=1, choices=range(4),
                        help='set verbose output level (default: %(default)s)', dest='verbose')
    parser.add_argument('-s', '--typing-speed-override', type=float, default=0,
                        help='overrides typing speed', dest='typing_speed')
    parser.add_argument('-r', '--reject-first', action='store_true', default=False,
                        help='finds all rejects before starting', dest='reject_first')
    return parser.parse_args()

args = init_args()

def main():
    try:
        PseudoBusy(args=args).start()
    except: pass
    finally: print (Printer.CLEAR + Printer.RESET)

if __name__ == '__main__': main()

