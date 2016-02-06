#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from printer import Printer, Random

class PseudoBusy():
    MAX_PATIENCE = 6
    MIN_FILE_LENGTH = 1
    MAX_FILE_LENGTH = 5000

    def __init__(self):
        self.rand = Random()
        self.printer = Printer(shift_in_chance=25)
        self.target_dir = os.path.expanduser('~/')
        self.hide_target = True
        self.running = False

    def start(self):
        self.running = True
        self.printer.write('Generating file list... ', speed=50)
        # TODO whitelist and blacklist
        self.files = [os.path.join(path, filename) for path, dirs, files in os.walk(self.target_dir) for filename in files]
        self.original_num_files = len(self.files)
        self.printer.write('Found {} files'.format(self.original_num_files))
        self.run()

    def run(self):
        while self.running:
            self.printer.reset()
            infile, num_lines = self.pick_file()

            #self.printer.override_speed = 1000 # NOTE just for testing
            self.printer.write("Reading: "+infile.replace(self.target_dir, '') if self.hide_target else infile)
            self.printer.write("\nLines: {}| Rejects: {} \n".format(num_lines, self.original_num_files - len(self.files)))
            self.print_file(infile)

    def print_file(self, infile):
        try:
            with open(infile, "r") as ins:
                patience = self.MAX_PATIENCE
                for line in ins:
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
                # TODO print err if verbose
                self.files.remove(file) # we don't need to see rejects again
                file = None

        return (file, num_lines)

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
    except Exception, e:
        print Printer.RESET
        print Printer.CLEAR
        print e
        pass
