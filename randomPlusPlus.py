#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, string, random

class RandomPlusPlus(random.Random):
    def __init__(self):
        random.Random.__init__(self)

    def file(self, directory):
        return self.safe_choice([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

    def dir(self, directory):
        return self.safe_choice([d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))])

    def safe_choice(self, color_list):
        if not len(color_list):
            return None
        return self.choice(color_list)

    def ansi_color(self):
        return '\033[9' + str(self.randint(0, 8)) + 'm'  # in the range \003[90m - \003[98m

    def ansi_annotation(self):  # this has a high chance of being butt ugly
        return '\033[' + str(self.randint(10, 99)) + 'm'  # in the range \003[10m - \003[99m

    def unique_ansi_color(self, color_list):
        length = len(color_list)
        if length:
            function = self.ansi_color
            if length == 8:  # ran out of colors, just find something to return
                function = self.ansi_annotation

            selection = function()
            while any(selection in s for s in color_list):
                selection = function()

            return selection
        else:
            return self.ansi_color()

    def int(self, min_index, max_index):
        return self.randint(min_index, max_index)

    def string(self, length):
        return ''.join(self.choice(string.digits + string.ascii_letters) for i in range(length))
