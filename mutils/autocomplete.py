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

    def complete(self, cmds):
        pass


class AutoComplete(AutoCompleteBase):

    def __init__(self):
        self._handlers = {}

    def pushHandler(self, handler):
        self._handlers[handler.name] = handler

    def complete(self, cmds):
        if len(cmds) == 1:
            ret = []
            for k in self._handlers:
                if k.startswith(cmds[0]):
                    ret.append(k)
            return ret
        else:
            if cmds[0] in self._handlers:
                return self._handlers[cmds[0]].complete(cmds[1:])
