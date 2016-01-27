#!/usr/bin/env python
#encoding=utf8

# File Name: service.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 10时48分25秒

from twisted.internet import reactor, protocol

from gateway.session import Session
from gateway.telnet import TelnetService

import time

WELCOME_MESSAGE = "欢迎来到Castle-Online\r\n\r\n"

class SessionProtocol(protocol.Protocol):

    SHELL = "\r\nCastle-%s-%d:%02d:%02d>> "

    def __init__(self):
        self._telnet = TelnetService(self)
        self._session = Session(self)

    def connectionMade(self):
        self.transport.write(WELCOME_MESSAGE)
        self._session.handle("")

    def dataReceived(self, data):
        cmd = self._telnet.handle(data)
        if cmd:
            if self._session.logged():
            
                self.writeShell()
            else:
                self._session.handle(cmd)


    def writeShell(self):
        lt = time.localtime()
        self.transport.write(SessionProtocol.SHELL %
                             ("demo", lt.tm_hour, lt.tm_min, lt.tm_sec))

    def connectionLost(self, reason):
        self._session.logout()

class SessionFactory(protocol.Factory):

    def buildProtocol(self, addr):
        return SessionProtocol()


if __name__ == '__main__':
    factory = SessionFactory()
    reactor.listenTCP(2333, factory)
    reactor.run()
