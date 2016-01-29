#!/usr/bin/env python
#encoding=utf8

# File Name: autocomplete.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 21时37分11秒



class AutoCompleteBase(object):
    """
    auto-complete for client shell
    """

    def __init__(self):
        pass

    def complete(self, player, cmds):
        pass


class AutoComplete(AutoCompleteBase):

    def __init__(self):
        self._handlers = {}

    def pushHandler(self, handler):
        self._handlers[handler.name] = handler

    def complete(self, player, cmd):
        if len(cmd.args) == 0:
            ret = []
            tmpbuf = "".join(cmd.tmpbuf())
            for k in self._handlers:
                if k.startswith(tmpbuf):
                    ret.append(k)
            return ret
        else:
            if cmd.args[0] in self._handlers:
                return self._handlers[cmd.args[0]].complete(player, cmd)
