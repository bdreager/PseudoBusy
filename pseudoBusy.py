#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, string, platform, printer, randomPlusPlus

class PseudoBusy():
    def __init__(self):
        self.rand = randomPlusPlus.RandomPlutPlus()
        self.printer = printer.Printer(self.rand)
        self.compiled = True

    def run(self):
        # TODO search for files on users filesystem
        # TODO use whitelist for selecting (txt, sh, py, rb, c, cpp, h, js, html, etc.)
        while True:  # TODO make a stop case
            self.printer.reset()
            infile = self.pickFile();

            with open(infile, "r") as ins:
                for line in ins:
                    if self.rand.int(0, 10):
                        num = self.rand.int(10, 25)
                        self.printer.typing(self.rand.string(num))
                        if num <= len(line):
                            self.printer.backspace(num)
                        else:
                            self.printer.backspace_delete(num)

                    self.printer.typing(line)

            print "\n\n"

    def pickFile(self):
        if self.compiled:
            dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        else:
            dir = os.path.dirname(os.path.abspath(__file__))  # base directory

        if platform.system() is 'darwin':
            return self.rand.choice(dir)  # OSX doesn't like something I'm doing in rand.file, so use this instead
        else:
            full_file = None
        while full_file is None:
            dirs = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
            if len(dirs):
                newDir = self.rand.choice(dirs)
                file = self.rand.file(newDir)
                if not file is None:
                    full_file = dir + "/" + newDir + "/" + file

        return full_file

#######################
#	Driver
#####################
if __name__ == '__main__':
    main = PseudoBusy()
    main.compiled = False
    main.run()
