#!/usr/bin/env python
#encoding=utf8

# File Name: session.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 10时48分14秒

from player.service import PlayerService

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
        self._loginRetry = 2

    def handle(self, cmd):
        if self._stat == Session.SESSION_STAT_INIT:
            self._protocol._telnet.chmod()
            self._protocol.transport.write("用户名:")
            self._stat = Session.SESSION_STAT_NAME
        elif self._stat == Session.SESSION_STAT_NAME:
            self._name = cmd
            self._protocol.transport.write("\r\n密码:")
            self._protocol._telnet.disableEcho()
            self._stat = Session.SESSION_STAT_PWD
        elif self._stat == Session.SESSION_STAT_PWD:
            self._pwd = cmd
            self.login()
        else:
            pass

    def login(self):
        pbproxy = self._protocol._factory["player"]
        if pbproxy:
            pbproxy.callRemote("login", self._name, self._pwd).\
                addCallback(self._login_cb)
        else:
            self._protocol.transport.write("\r\n用戶服务器未启动!\r\n")
            self._protocol.transport.loseConnection()

    def _login_cb(self, result):
        if result[0] == PlayerService.LOGIN_SUCCESS:
            self._stat = Session.SESSION_STAT_DONE
            self._protocol._locate = result[2]
            self._protocol.writeShell(result[1])
            self._protocol._telnet.enableEcho()
        elif result[0] == PlayerService.LOGIN_NEED_PWD:
            if self._loginRetry:
                self._loginRetry -= 1
                self._protocol.transport.write(result[1])
                self._protocol.transport.write("\r\n密码:")
            else:
                self._protocol.transport.write(result[1])
                self._protocol.transport.write("\r\n")
                self._protocol.transport.loseConnection()
        else:
            self._stat = Session.SESSION_STAT_NAME
            self._protocol.transport.write(result[1])
            self._protocol.transport.write("\r\n用户名:")
            self._protocol._telnet.enableEcho()
        
    def logout(self):
        pass

    def logged(self):
        return self._stat == Session.SESSION_STAT_DONE
        
