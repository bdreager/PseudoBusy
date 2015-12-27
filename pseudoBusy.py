#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, platform, random, printer, randomPlusPlus

class PseudoBusy():
    MAX_PATIENCE = 6
    LENGTH_MIN = 1
    LENGTH_MAX = 5000

    def __init__(self, packaged=False):
        self.rand = randomPlusPlus.RandomPlusPlus()
        self.printer = printer.Printer(self.rand, shift_in_chance=25)
        if packaged:
            self.dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # since we're in a zip file, we have to move one level up
            self.message = Response.generic
        else:
            self.dir = os.path.dirname(os.path.abspath(__file__))  # local directory
            self.message = Response.random

        self.slash = '\\' if platform.system() is 'Windows' else '/'  # this needs to be tested on windows
        depth = self.dir.count(self.slash)-2  # remove the -2 to start in /  but permission will be a problem then
        self.home = self.dir + ''.join((self.slash + "..") * depth)+self.slash

    def run(self):
        # TODO search for files deeper on users filesystem
        while True:  # TODO make a stop case
            self.printer.reset()
            infile = None
            num_lines = 0
            # TODO search in a background thread. Maintain small backlog (10?) of files to print
            while not infile:
                try:
                    infile = self.recurse_pick_file(self.home[:-1])  # NOTE the [:-1] is just for testing to remove the end "/"
                    with open(infile, 'r') as ins: ins.readline().decode('ascii')  # for catching junk we don't care to see
                    num_lines = self.bufcount(infile)
                    if num_lines <= self.LENGTH_MIN: raise Exception('File too small') # for empty and single line files
                    if num_lines >= self.LENGTH_MAX: raise Exception('File too large') # for massive files (probably not code)
                except Exception, err:
                    self.printer.override_speed = 1000
                    self.printer.typing(str(err) + '\n')
                    #self.printer.typing(self.message())
                    self.printer.override_speed = 0
                    infile = None

            self.printer.typing("Reading: "+infile+"\n")
            self.printer.typing("Lines: "+str(num_lines)+"\n")
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
                            self.printer.typing(self.message())
                            break;
                    if not self.rand.int(0, 10):  # type a random string as a 'mistake'
                        num = self.rand.int(10, 25)
                        self.printer.typing(self.rand.string(num))
                        self.printer.backspace_delete(num)
                    self.printer.typing(line)

        except:  # mainly for permission denied on windows
            self.printer.typing(self.message())

    def loop_pick_file(self):
        if platform.system() is 'darwin':
            return self.rand.choice(self.dir)  # OSX doesn't like something I'm doing in pick_file, so use this instead
        else:
            full_file = None

        while full_file is None:
            dirs = [d for d in os.listdir(self.home) if os.path.isdir(os.path.join(self.home, d))]
            if len(dirs):
                full_dir = self.home+self.rand.choice(dirs)
                found_file = self.rand.file(full_dir)
                if found_file is not None:
                    full_file = full_dir + self.slash + found_file

        return full_file

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
            found_file = directory + self.slash + new_file if new_file else None
        if found_file:
            if not os.access(found_file, os.R_OK):
                found_file = None
            # elif not os.path.splitext(file) in self.whitelist:
            #    file = None

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

# simple, static, random response generator
class Response:
    Errors = []
    with open("errors.txt", "r") as ins:
        for line in ins:
            Errors.append(line)

    @classmethod
    def random(cls):
        return "Error: "+cls.Errors[random.randint(0, len(cls.Errors)-1)]

    @staticmethod
    def generic():
        return "Error"

#######################
#	Driver
#####################
if __name__ == '__main__':
    PseudoBusy().run()
