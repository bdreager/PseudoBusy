#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from printer import Printer, Random
from argparse import ArgumentParser

__program__ = 'PseudoBusy'
__version__ = '0.8.0'
__description__ = 'Terminal vomit'

class PseudoBusy():
    MAX_PATIENCE = 6
    MIN_FILE_LENGTH = 1
    MAX_FILE_LENGTH = 5000

    def __init__(self, args=None):
        self.args = args
        self.rand = Random()
        self.printer = Printer(shift_in_chance=25)
        self.target_dir = os.path.expanduser('~/')
        self.hide_target = True
        self.running = False

    def start(self):
        self.running = True
        self.printer.write('Generating file list... ', speed=1)
        # TODO whitelist and blacklist
        self.files = [os.path.join(path, filename) for path, dirs, files in os.walk(self.target_dir) for filename in files]
        self.original_num_files = len(self.files)
        self.printer.write('Found {} files'.format(self.original_num_files))
        self.run()

    def run(self):
        while self.running:
            self.printer.reset()
            infile, num_lines = self.pick_file()

            if self.args.typing_speed: self.printer.override_speed = self.args.typing_speed
            self.verbose("Reading: "+infile.replace(self.target_dir, '') if self.hide_target else infile)
            self.verbose("\nLines: {}\n".format(num_lines))
            self.verbose("Rejects: {}\n".format(self.original_num_files - len(self.files)))
            self.print_file(infile)

    def print_file(self, infile):
        try:
            with open(infile, "r") as ins:
                patience = self.MAX_PATIENCE
                for line in ins:
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
        except: pass

    def pick_file(self):
        file = num_lines = None
        while not file:
            try:
                file = self.rand.choice(self.files)
                if not os.access(file, os.R_OK): raise Exception('No read access')

                with open(file, 'r') as ins: ins.readline().decode('ascii')  # for catching junk we don't care to see
                num_lines = self.bufcount(file)
                if num_lines <= self.MIN_FILE_LENGTH: raise Exception('File too small') # for empty and single line files
                if num_lines >= self.MAX_FILE_LENGTH: raise Exception('File too large') # for massive files (probably not code)
            except Exception, err:
                self.verbose(str(err)+'\n')
                self.files.remove(file) # we don't need to see rejects again
                file = None

        return (file, num_lines)

    def verbose(self, string):
        if self.args.verbose: self.printer.write(string)

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

def init_args():
    parser = ArgumentParser(prog=__program__, description=__description__)
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='turn on verbose output', dest='verbose')
    parser.add_argument('-s', '--typing-speed-override', type=float, default=0,
                        help='overrides typing speed', dest='typing_speed')

    return parser.parse_args()

if __name__ == '__main__':
    args = init_args()
    try:
        print Printer.CLEAR
        PseudoBusy(args=args).start()
    except Exception, e:
        print Printer.RESET
        print Printer.CLEAR
        print e
        pass
