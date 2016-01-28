#!/usr/bin/env python
#encoding=utf8

# File Name: commands.py
# Author: LSP
# Created Time: 2016年01月28日 星期四 14时20分42秒

from mutils.command import CommandHandlerBase


class GoHandler(CommandHandlerBase):
    """
    handle "go [direction]" commands
    """

    DIRECTS = ["left", "right", "forward", "back", "up", "down"]
    
    def __init__(self):
        CommandHandlerBase.__init__("go")

    def handle(self, args):
        pass

    def complete(self, args):
        if len(args) == 1:
            ret = []
            for d in self.DIRECTS:
                if d.startswith(cmds[0]):
                    ret.append(d)
            return ret

        
