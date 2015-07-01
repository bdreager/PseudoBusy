#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, platform, random, printer, randomPlusPlus

class PseudoBusy():
    MAX_PATIENCE = 6

    def __init__(self, packaged=False):
        self.rand = randomPlusPlus.RandomPlusPlus()
        self.printer = printer.Printer(self.rand)
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
            while not infile:
                try:
                    infile = self.recurse_pick_file(self.home[:-1])  # NOTE the [:-1 is just for testing to remove the end "/"]
                    with open(infile, 'r') as ins: ins.readline().decode('ascii')  # for catching junk we don't care to see
                except:
                    print self.message()
                    pass

            # infile = self.loop_pick_file()
            self.printer.typing("\nReading: "+infile+"\n")
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
                                print self.message()
                                break;
                        if not self.rand.int(0, 10):  # type a random string as a 'mistake'
                            num = self.rand.int(10, 25)
                            self.printer.typing(self.rand.string(num))
                            self.printer.backspace_delete(num)
                        self.printer.typing(line)

            except:  # mainly for permission denied on windows
                print self.message()
                pass

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
