#!/usr/bin/env python
#encoding=utf8

# File Name: telnet.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 10时41分37秒

from twisted.internet import reactor, protocol

from mutils.command import Command

import cPickle as pickle

IAC_DISABLE_ECHO_READLINE = "\xff\xfb\x01\xff\xfb\x03"

class TelnetService(object):
    """
    telnet服务
    """

    def __init__(self, protocol):
        self._protocol = protocol
        self._cmd = Command()
        self._space = True
        self._echo = True
        self._autocomplete = False
        self._inAC = False
        self._handlers = {}
        self._handlers["\xff"] = self.handleIAC
        self._handlers[" "] = self.handleSpace
        self._handlers["\r"] = self.handleEnter
        self._handlers["\n"] = self.handleEnter
        self._handlers["\t"] = self.handleTab
        self._handlers["\x7f"] = self.handleBackspace

    def handle(self, data):
        print repr(data)
        #in auto-complete processing, never deal with any other input
        if self._inAC:
            return None
            
        if data[0] in self._handlers:
            return self._handlers[data[0]](data)
        else:
            return self.handleChar(data)

    def chmod(self):
        self._protocol.transport.write(IAC_DISABLE_ECHO_READLINE)
        self.enableEcho()

    def enableEcho(self):
        self._echo = True

    def disableEcho(self):
        self._echo = False

    def enableSpace(self):
        self._space = True

    def disableSpace(self):
        self._space = False

    def enableAC(self):
        self._autocomplete = True

    def disableAC(self):
        self._autocomplete = False

    def handleIAC(self, data):
        pass #do nothing...

    def handleSpace(self, data):
        if self._space:
            self.handleChar(data)
        else:
            if not self._cmd.tmpbufEmpty():
                self._cmd.finish()
                self._protocol.transport.write(" ")

    def handleEnter(self, data):
        if not self._cmd.empty():
            self._cmd.finish()
            ret = self._cmd
            self._cmd = Command()
            return ret

    def handleBackspace(self, data):
        if not self._cmd.empty():
            self._cmd.pop()
            if self._echo:
                self._protocol.transport.write("\x08 \x08")

    def handleTab(self, data):
        if self._autocomplete:
            self._inAC = True
            pbproxy = self._protocol._factory["player"]
            if pbproxy:
                pbproxy.callRemote("autocomplete",
                                   self._protocol._session._name,
                                   pickle.dumps(self._cmd)).\
                    addCallback(self.handleTab_cb)
            else:
                self._protocol.transport.write("\r\n用戶服务器未启动!\r\n")
                self._protocol.transport.loseConnection()

    def handleTab_cb(self, result):
        self._inAC = False
        if not result:
            return

        if len(result) == 1:
            offset = self._cmd.tmpbufSize()
            self._protocol.transport.write(result[0][offset:] + " ")
            self._cmd.args.append(result[0])
            self._cmd._tmpbuf = []
        else:
            self._protocol.writeShell(" ".join(result))
            self._protocol.transport.write(str(self._cmd))

    def handleChar(self, data):
        self._cmd.append(data)
        if self._echo:
            self._protocol.transport.write(data)
