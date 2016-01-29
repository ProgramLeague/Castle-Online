#!/usr/bin/env python
#encoding=utf8

# File Name: command.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 15时42分37秒

from mutils.autocomplete import AutoCompleteBase

import re

class Command(object):

    def __init__(self):
        self.args = []
        self._tmpbuf = []

    def append(self, char):
        self._tmpbuf.append(char)

    def pop(self):
        if self._tmpbuf:
            self._tmpbuf.pop()
        else:
            if self.args:
                arg = self.args.pop()
                self._tmpbuf = [i for i in arg]

    def finish(self):
        if self._tmpbuf:
            self.args.append("".join(self._tmpbuf))
            self._tmpbuf = []

    def empty(self):
        return not bool(self.args) and not bool(self._tmpbuf)

    def tmpbuf(self):
        return self._tmpbuf

    def tmpbufEmpty(self):
        return not bool(self._tmpbuf)

    def tmpbufSize(self):
        return len(self._tmpbuf)

    def __str__(self):
        ret = ""
        if self.args:
            ret += " ".join(self.args) + " "
        ret += "".join(self._tmpbuf)
        return ret


class CommandHandlerBase(AutoCompleteBase):

    def __init__(self, name):
        self.name = name

    def handle(self, player, cmd):
        pass

    def complete(self, player, cmd):
        pass
