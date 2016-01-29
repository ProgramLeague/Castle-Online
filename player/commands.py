#!/usr/bin/env python
#encoding=utf8

# File Name: commands.py
# Author: LSP
# Created Time: 2016年01月28日 星期四 14时20分42秒

from mutils.command import CommandHandlerBase
from mutils.autocomplete import AutoComplete

class HandlersManager(AutoComplete):

    def __init__(self):
        AutoComplete.__init__(self)
        self.initHandlers()

    def initHandlers(self):
        self.pushHandler(GoHandler())
        self.pushHandler(AttackHandler())

    def getHandler(self, name):
        if name in self._handlers:
            return self._handlers[name]

class GoHandler(CommandHandlerBase):
    """
    handle "go [direction]" commands
    """

    DIRECTS = ["left", "right", "forward", "back", "up", "down"]
    
    def __init__(self):
        CommandHandlerBase.__init__(self, "go")

    def handle(self, player, cmd):
        pass

    def complete(self, player, cmd):
        if len(cmd.args) == 1:
            ret = []
            tmpbuf = "".join(cmd.tmpbuf())
            for d in self.DIRECTS:
                if d.startswith(tmpbuf):
                    ret.append(d)
            return ret

class AttackHandler(CommandHandlerBase):
    """
    handle "attack [enemy]" commands
    """

    def __init__(self):
        CommandHandlerBase.__init__(self, "attack")

    def handle(self, player, cmd):
        pass

    def complete(self, player, cmd):
        pass
