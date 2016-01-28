#!/usr/bin/env python
#encoding=utf8

# File Name: command.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 15时42分37秒

from twisted.spread import pb

from mutils.autocomplete import AutoCompleteBase

import re

class Command(pb.Referenceable):

    def __init__(self, cmdstr):
        self.name = ""
        self.args = []
        cmds = re.split("[\s]+", cmdstr)
        if cmds:
            self.name = cmds[0]
            self.args = cmds[1:]


class CommandHandlerBase(AutoCompleteBase):

    def __init__(self, name):
        self.name = name

    def handle(self, args):
        pass

    def complete(self, args):
        pass
