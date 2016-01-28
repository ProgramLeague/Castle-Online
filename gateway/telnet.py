#!/usr/bin/env python
#encoding=utf8

# File Name: telnet.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 10时41分37秒

from twisted.internet import reactor, protocol

IAC_DISABLE_ECHO_READLINE = "\xff\xfb\x01\xff\xfb\x03"

class TelnetService(object):
    """
    telnet服务
    """

    def __init__(self, protocol):
        self._protocol = protocol
        self._buflist = []
        self._echo = True
        self._readline = True

    def handle(self, data):
        #print repr(data)
        if data[0] == "\xff":
            #print "IAC"
            pass
        elif self._readline:
            return data.strip()
        elif data == "\r\n" or data == "\r\x00": #read-line
            buffer = "".join(self._buflist)
            self._buflist = []
            return buffer.strip()
        else:
            if self._echo:
                self._protocol.transport.write(data) #do echo
            self._buflist.append(data)
            return None

    def chmod(self):
        self._protocol.transport.write(IAC_DISABLE_ECHO_READLINE)
        self._echo = True
        self._readline = False

    def enableEcho(self):
        self._echo = True

    def disableEcho(self):
        self._echo = False
