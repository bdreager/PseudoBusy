#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, platform, printer, randomPlusPlus

class PseudoBusy():
    def __init__(self, packaged=False):
        self.rand = randomPlusPlus.RandomPlutPlus()
        self.printer = printer.Printer(self.rand)
        if packaged:
            self.dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #since we're in a zip file, we have to move one level up
        else:
            self.dir = os.path.dirname(os.path.abspath(__file__))  #local directory

        slash = '\\' if platform.system() is 'Windows' else '/' #this needs to be tested on windows
        depth = self.dir.count(slash)-2 #remove the -2 to start in /  but permission will be a problem then
        self.home = self.dir +''.join("/.." * depth)+"/"

    def run(self):
        # TODO search for files deeper on users filesystem
        # TODO use whitelist for selecting (txt, sh, py, rb, c, cpp, h, js, html, css, etc.)
        while True:  # TODO make a stop case
            self.printer.reset()
            infile = self.pick_file()
            self.printer.typing("Reading: "+infile+"\n\n")
            with open(infile, "r") as ins:
                for line in ins:
                    if not self.rand.int(0, 10):    #types a random string as a 'mistake'
                        num = self.rand.int(10, 25)
                        self.printer.typing(self.rand.string(num))
                        #if num < len(line)/2:
                        #    self.printer.backspace(num)
                        #else:
                        self.printer.backspace_delete(num)

                    self.printer.typing(line)

            print "\n\n"

    def pick_file(self):
        if platform.system() is 'darwin':
            return self.rand.choice(self.dir)  # OSX doesn't like something I'm doing in pick_file, so use this instead
        else:
            full_file = None

        while full_file is None:
            dirs = [d for d in os.listdir(self.home) if os.path.isdir(os.path.join(self.home, d))]
            if len(dirs):
                full_dir = self.home+self.rand.choice(dirs)
                file = self.rand.file(full_dir)
                if not file is None:
                    full_file = full_dir + "/" + file

        return full_file

#######################
#	Driver
#####################
if __name__ == '__main__':
    PseudoBusy().run()
