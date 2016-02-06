#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, string, sys, time, platform, random

class TYPE:
    UNDEFINED = 0
    ALPHA = 1
    QUOTE = 2
    DIGIT = 3
    MATH = 4
    SPECIAL = 5

class ACTION:
    DEFAULT = 0
    QUOTE = 1
    RANDOM = 2

class Printer(object):
    MAX_TYPE_SPEED = 100 # measured in letters per second ~1200wpm -> 100lps
    MIN_TYPE_SPEED = 10  # 120wpm converted to lps
    TYPE_SPEED_CHANGE_AMT = 0.5
    TYPE_SPEED_DEFAULT = 10

    CLEAR = '\033[2J\033[;H'
    RESET = '\033[0m'

    SHIFT_IN = "\016"
    SHIFT_OUT = "\017"

    def __init__(self, shift_in_chance=0):
        self.rand = Random()
        self._type_speed = None
        self.type_delay = None
        self.override_speed = 0

        self.shift_in_chance = shift_in_chance
        if self.shift_in_chance < 0: self.shift_in_chance = 0
        if self.shift_in_chance > 100: self.shift_in_chance = 100

        self.reset()

    @property
    def type_speed(self): return self._type_speed
    @type_speed.setter
    def type_speed(self, value):
        self._type_speed = value

        if self._type_speed > self.MAX_TYPE_SPEED: self._type_speed = self.MAX_TYPE_SPEED
        elif self._type_speed < self.MIN_TYPE_SPEED: self._type_speed = self.MIN_TYPE_SPEED

        if self.override_speed is not 0:
            self._type_speed += self.override_speed

        self.type_delay = ((60.0/self.type_speed)/60.0)

    def reset(self):
        if self.shift_in_chance and self.rand.int(1, 100) <= self.shift_in_chance:
            print self.SHIFT_IN
        else:
            print self.SHIFT_OUT

        self.override_speed = 0
        self.type_speed = self.TYPE_SPEED_DEFAULT
        self.action = ACTION.DEFAULT

        self.color_list = []

        self.main_color = self.pick_color()
        self.quote_color = self.pick_color()
        self.digit_color = self.pick_color()
        self.math_color = self.pick_color()
        self.special_color = self.pick_color()
        self.random_color = self.pick_color()
        self.alpha_color = self.pick_color()

    def write(self, string, speed=None):
        if speed: self.override_speed = speed
        for char in string:
            color = self.determine_color(char)
            sys.stdout.write('%s%s' % (color, char))
            sys.stdout.flush()

            self.typing_change()

            time.sleep(self.type_delay)

    def backspace(self, length):
        for _ in range(length):
            sys.stdout.write('\b')
            sys.stdout.flush()
            self.typing_change()
            time.sleep(self.type_delay)

    def backspace_delete(self, length):
           for _ in range(length):
            sys.stdout.write('\b \b')
            sys.stdout.flush()
            self.typing_change()
            time.sleep(self.type_delay)

    def pick_color(self):
        new_color = ''
        if not platform.system() is 'Windows':  # don't work on windows, so don't bother
            new_color = self.rand.unique_ansi_color(self.color_list)

        self.color_list.append(new_color)
        return new_color

    def typing_change(self):
        if not self.rand.int(0, 1000):
            self.type_speed = self.MAX_TYPE_SPEED if self.rand.int(0, 1) else self.MIN_TYPE_SPEED
        else:
            self.accelerate_typing(self.rand.int(0, 1))

    def accelerate_typing(self, roll):
        if roll:
            self.type_speed += self.TYPE_SPEED_CHANGE_AMT
        else:
            self.type_speed -= self.TYPE_SPEED_CHANGE_AMT

    def determine_color(self, char):
        char_type = self.determine_type(char)

        if self.action == ACTION.RANDOM:
            if char_type == TYPE.ALPHA:
                return self.random_color
            else:
                self.action = ACTION.DEFAULT
                # return self.main_color
        if self.action == ACTION.QUOTE:
            if char_type == TYPE.QUOTE:
                self.action = ACTION.DEFAULT
            return self.quote_color
        elif char_type == TYPE.QUOTE:
            self.action = ACTION.QUOTE
            return self.quote_color
        elif char_type == TYPE.ALPHA:
            return self.alpha_color
        elif char_type == TYPE.DIGIT:
            return self.digit_color
        elif char_type == TYPE.MATH:
            return self.math_color
        elif char_type == TYPE.SPECIAL:
            return self.special_color
        elif self.action == ACTION.DEFAULT:
            if char == " " and not self.rand.int(0, 10):
                self.action = ACTION.RANDOM
                return self.random_color
            return self.main_color

    @staticmethod
    def determine_type(char):
        # TODO Detect curly brackets,
        if char.isalpha() or char == "-" or char == "_":
            return TYPE.ALPHA
        elif char == '\"': # or char == '\'': //can't use single quote until I can detect apostrophe
            return TYPE.QUOTE
        elif char.isdigit():
            return TYPE.DIGIT
        elif char == '+' or char == '=' or char == '>' or char == '<' or char == '.' or char == '/' or char == '*':
            return TYPE.MATH
        elif char == '?' or char == '&' or char == '|' or char == '%' or char == '!' or char == ':' or char == '\\':
            return TYPE.SPECIAL
        else:
            return TYPE.UNDEFINED

class Random(random.Random):
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
        return '\033[9' + str(self.randint(0, 9)) + 'm'  # in the range \003[90m - \003[98m

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