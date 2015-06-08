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

        # TODO use whitelist for selecting (txt, sh, py, rb, c, cpp, h, js, html, css, xml, etc.)
        #self.whitelist = [".txt", ".sh", ".py", ".rb", ".c", ".cpp", ".h", ".js", ".html", ".css", ".xml", ".ini", ".md", ".in", ".url"]

    def run(self):
        # TODO search for files deeper on users filesystem
        while True:  # TODO make a stop case
            self.printer.reset()
            infile = None
            while not infile:
                infile = self.recurse_pick_file(self.home[:-1])#NOTE the [:-1 is just for testing to remove the end "/"]

            #infile = self.loop_pick_file()
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

    def loop_pick_file(self):
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

    def recurse_pick_file(self, dir):
        file = None
        if self.rand.int(0, 10):
            new_dir = self.rand.dir(dir)
            try:
                file = self.recurse_pick_file(dir+"/"+new_dir) if new_dir else None
            except:
                pass
        if not file:
            new_file = self.rand.file(dir)
            file = dir + "/" + new_file if new_file else None
        if file:
            if not os.access(file, os.R_OK):
                file = None
            #elif not os.path.splitext(file) in self.whitelist:
            #    file = None

        return file

#######################
#	Driver
#####################
if __name__ == '__main__':
    PseudoBusy().run()
