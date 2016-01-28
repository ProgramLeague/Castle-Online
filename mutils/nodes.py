#!/usr/bin/env python
#encoding=utf8

# File Name: nodes.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 15时45分00秒

from twisted.internet import reactor
from twisted.spread import pb
from twisted.python import log

class RetryPBClientFactory(pb.PBClientFactory):

    def __init__(self, node, proxy):
        pb.PBClientFactory.__init__(self)
        self._node = node
        self._proxy = proxy
        self._retryDelay = 2
        self.connect()

    def connect(self):
        if self._node["type"] == "tcp":
            reactor.connectTCP(self._node["host"], self._node["port"], self)
        elif self._node["type"] == "unix":
            reactor.connectUNIX(self._node["addr"], self)
        else:
            log.err("Unknown connect type")
            
        self.getRootObject().addCallback(self._proxy.insert, self._node["name"])

    def clientConnectionFailed(self, connector, reason):
        log.err("Connect to " + self._node["name"].encode("utf-8") +
                " Failed, Retrying...")
        reactor.callLater(self._retryDelay, self.connect)
        self._retryDelay += 2

    def clientConnectionLost(self, connector, reason, reconnecting=0):
        log.err("Connect to " + self._node["name"].encode("utf-8") +
                " Lost, Retrying...")
        self._retryDelay = 2
        self._proxy.delete(self._node["name"])
        reactor.callLater(self._retryDelay, self.connect)


class NodeProxy(object):
    """
    PB proxy
    """

    def __init__(self, config):
        self._nodes = {}
        for node in config:
            factory = RetryPBClientFactory(node, self)

    def insert(self, obj, name):
        if not name in self._nodes:
            self._nodes[name] = obj

    def delete(self, name):
        if name in self._nodes:
            del self._nodes[name]

    def __getitem__(self, name):
        if name in self._nodes:
            return self._nodes[name]
        else:
            return None
