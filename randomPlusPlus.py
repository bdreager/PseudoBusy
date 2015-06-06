#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, platform, random

class RandomPlutPlus(random.Random):
    def __init__(self):
        random.Random.__init__(self)

    def file(self, dir):
        return self.safe_choice([f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))])

    def dir(self, dir):
        return self.safe_choice([d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))])

    def safe_choice(self, list):
        if not len(list):
            return None
        return self.choice(list)

    def ANSI_color(self):
         if not platform.system() is 'Windows':
            return '\033[9' + str(self.randint(0, 8)) + 'm'  # in the range \003[90m - \003[98m
         else:
            return ''  # don't work on windows, so don't bother

    def ANSI_annotation(self):  #this has a high chance of being butt ugly
         if not platform.system() is 'Windows':
            return '\033[' + str(self.randint(10, 99)) + 'm'  # in the range \003[10m - \003[99m
         else:
            return ''  # don't work on windows, so don't bother

    def unique_ANSI_color(self, list):
        length = len(list)
        if length:
            function = self.ANSI_color
            if length == 8: #ran out of colors, just find something to return
                function = self.ANSI_annotation

            selection = function()
            while any(selection in s for s in list):
                selection = function()

            return selection
        else:
            return self.ANSI_color()

    def int(self, min, max):
        return self.randint(min, max)