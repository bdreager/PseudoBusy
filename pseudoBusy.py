#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, platform, printer, randomPlusPlus

class PseudoBusy():
    def __init__(self, packaged=False):
        self.rand = randomPlusPlus.RandomPlusPlus()
        self.printer = printer.Printer(self.rand)
        if packaged:
            self.dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # since we're in a zip file, we have to move one level up
        else:
            self.dir = os.path.dirname(os.path.abspath(__file__))  # local directory

        self.slash = '\\' if platform.system() is 'Windows' else '/'  # this needs to be tested on windows
        depth = self.dir.count(self.slash)-2 # remove the -2 to start in /  but permission will be a problem then
        self.home = self.dir + ''.join((self.slash + "..") * depth)+self.slash

        # TODO use whitelist for selecting (txt, sh, py, rb, c, cpp, h, js, html, css, xml, etc.)
        # self.whitelist = [".txt", ".sh", ".py", ".rb", ".c", ".cpp", ".h", ".js", ".html", ".css", ".xml", ".ini", ".md", ".in", ".url", ".json", ".csv"]

    def run(self):
        # TODO search for files deeper on users filesystem
        while True:  # TODO make a stop case
            self.printer.reset()
            infile = None
            while not infile:
                infile = self.recurse_pick_file(self.home[:-1])  # NOTE the [:-1 is just for testing to remove the end "/"]

            # infile = self.loop_pick_file()
            self.printer.typing("Reading: "+infile+"\n\n")
            try:    # mainly for permission denied on windows
                with open(infile, "r") as ins:
                    for line in ins:
                        if not self.rand.int(0, 10):    # types a random string as a 'mistake'
                            num = self.rand.int(10, 25)
                            self.printer.typing(self.rand.string(num))
                            # if num < len(line)/2:
                            #    self.printer.backspace(num)
                            # else:
                            self.printer.backspace_delete(num)

                        self.printer.typing(line)
            except:
                pass

            print "\n\n"

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

#######################
#	Driver
#####################
if __name__ == '__main__':
    PseudoBusy().run()
