#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, platform, printer, randomPlusPlus

class PseudoBusy():
    def __init__(self):
        self.rand = randomPlusPlus.RandomPlutPlus()
        self.printer = printer.Printer(self.rand)

    def run(self):
        # TODO search for files on users filesystem
        # TODO use whitelist for selecting (txt, sh, py, rb, c, cpp, h, js, html, etc.)
        while True:  # TODO make a stop case
            self.printer.reset()
            infile = self.pickFile();

            with open(infile, "r") as ins:
                for line in ins:
                    self.printer.typing(line)
                    # TODO fake errors when typing, backspace over error, retype

            print "\n\n"

    def pickFile(self):
        #dir = os.path.dirname(os.path.abspath(__file__))  # base directory
        dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if platform.system() is 'darwin':
            return self.rand.choice(dir)  # OSX doesn't like something I'm doing in pickFile, so use this instead
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

# #######################
# #	Driver
# #####################
# if __name__ == '__main__':
#     main = PseudoBusy()
#     main.run()