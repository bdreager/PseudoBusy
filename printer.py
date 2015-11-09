#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time, platform

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

class Printer():
    MAX_TYPE_SPEED = 100 # measured in letters per second
    MIN_TYPE_SPEED = 10  # 100 wpm converted to lps
    TYPE_SPEED_CHANGE_AMT = 0.5
    TYPE_SPEED_DEFAULT = 10

    def __init__(self, new_rand):
        self.rand = new_rand
        self.reset()

    def reset(self):
        self.type_speed = self.TYPE_SPEED_DEFAULT # TODO make a setter for type_speed that sets type_wait
        self.type_wait = ((60.0/self.type_speed)/60.0)
        self.action = ACTION.DEFAULT

        self.color_list = []

        self.main_color = self.pick_color()
        self.quote_color = self.pick_color()
        self.digit_color = self.pick_color()
        self.math_color = self.pick_color()
        self.special_color = self.pick_color()
        self.random_color = self.pick_color()
        self.alpha_color = self.pick_color()

    def typing(self, string):
        for char in string:
            color = self.determine_color(char)
            sys.stdout.write('%s%s' % (color, char))
            sys.stdout.flush()

            self.typing_change()

            time.sleep(self.type_wait)

    def backspace(self, length):
        for _ in range(length):
            sys.stdout.write('\b')
            sys.stdout.flush()
            self.typing_change()
            time.sleep(self.type_wait)

    def backspace_delete(self, length):
           for _ in range(length):
            sys.stdout.write('\b \b')
            sys.stdout.flush()
            self.typing_change()
            time.sleep(self.type_wait)

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
        self.type_wait = ((60.0/self.type_speed)/60.0)    

    def accelerate_typing(self, roll):
        if roll:
            self.type_speed += self.TYPE_SPEED_CHANGE_AMT
            if self.type_speed > self.MAX_TYPE_SPEED:
                self.type_speed = self.MAX_TYPE_SPEED
        else:
            self.type_speed -= self.TYPE_SPEED_CHANGE_AMT
            if self.type_speed < self.MIN_TYPE_SPEED:
                self.type_speed = self.MIN_TYPE_SPEED

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
