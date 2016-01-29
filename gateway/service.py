#!/usr/bin/env python
#encoding=utf8

# File Name: service.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 10时48分25秒

from twisted.internet import reactor, protocol
from twisted.python import log

from gateway.session import Session
from gateway.telnet import TelnetService
from mutils.nodes import NodeProxy

import sys, time, json
import cPickle as pickle

WELCOME_MESSAGE = "欢迎来到Castle-Online\r\n\r\n"

class SessionProtocol(protocol.Protocol):

    SHELL = "\r\nCastle-%s-%d:%02d:%02d>> "

    def __init__(self, factory):
        self._telnet = TelnetService(self)
        self._session = Session(self)
        self._factory = factory
        self._locate = ""

    def connectionMade(self):
        self.transport.write(WELCOME_MESSAGE)
        self._session.handle("")

    def dataReceived(self, data):
        cmd = self._telnet.handle(data)
        if cmd:
            if self._session.logged():
                pbproxy = self._factory["player"]
                if pbproxy:
                    pbproxy.callRemote("handle", self._session._name,
                                       pickle.dumps(cmd)).\
                        addCallback(self._cmdResult)
                else:
                    self._protocol.transport.write("\r\n用戶服务器未启动!\r\n")
                    self._protocol.transport.loseConnection()

            else:
                self._session.handle(cmd)

    def _cmdResult(self, result):
        self.writeShell(result)

    def writeShell(self, data):
        if data:
            self.transport.write("\r\n")
            self.transport.write(str(data))

        lt = time.localtime()
        self.transport.write(SessionProtocol.SHELL %
                             (self._locate, lt.tm_hour, lt.tm_min, lt.tm_sec))

    def connectionLost(self, reason):
        self._session.logout()

class SessionFactory(protocol.Factory,
                     NodeProxy):

    def __init__(self, config):
        NodeProxy.__init__(self, config)

    def buildProtocol(self, addr):
        return SessionProtocol(self)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: %s config.json" % (sys.argv[0])
        sys.exit(1)
    config = json.load(open(sys.argv[1], 'r'))
    log.startLogging(sys.stdout)
    #log.startLogging(open(config["logfile"], 'w'))
    factory = SessionFactory(config["nodes"])
    reactor.listenTCP(config["port"], factory, interface = config["ip"])
    reactor.run()
