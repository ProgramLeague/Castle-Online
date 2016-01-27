#!/usr/bin/env python
#encoding=utf8

# File Name: session.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 10时48分14秒

class Session(object):

    SESSION_STAT_INIT = 0
    SESSION_STAT_NAME = 1
    SESSION_STAT_PWD  = 2
    SESSION_STAT_DONE = 3
    
    def __init__(self, protocol):
        self._protocol = protocol
        self._stat = Session.SESSION_STAT_INIT
        self._name = ""
        self._pwd = ""

    def handle(self, cmd):
        if self._stat == Session.SESSION_STAT_INIT:
            self._protocol.transport.write("用户名:")
            self._stat = Session.SESSION_STAT_NAME
        elif self._stat == Session.SESSION_STAT_NAME:
            self._name = cmd
            self._protocol.transport.write("密码:")
            self._stat = Session.SESSION_STAT_PWD
            self._protocol._telnet.chmod()
        elif self._stat == Session.SESSION_STAT_PWD:
            self._pwd = cmd
            self.login()
        else:
            pass

    def login(self):
        def success():
            self._stat = Session.SESSION_STAT_DONE
            self._protocol.writeShell()
            self._protocol._telnet.enableEcho()
        success()

    def logout(self):
        pass

    def logged(self):
        return self._stat == Session.SESSION_STAT_DONE
        
