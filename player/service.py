#!/usr/bin/env python
#encoding=utf8

# File Name: service.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 17时19分18秒

from twisted.internet import reactor
from twisted.spread import pb
from twisted.python import log

from player.players import PlayerManager
from mutils.nodes import NodeProxy
from mutils.command import Command

import sys, json
import cPickle as pickle

class PlayerService(pb.Root,
                    PlayerManager,
                    NodeProxy):

    LOGIN_NEED_USER = 0
    LOGIN_NEED_PWD = 1
    LOGIN_SUCCESS = 2

    def __init__(self, dbpath, config):
        PlayerManager.__init__(self, dbpath)
        NodeProxy.__init__(self, config)

    def remote_login(self, name, password):
        if self.getPlayer(name):
            return (self.LOGIN_NEED_USER, "不能重复登录")

        p = self.loginPlayer(name)
        if not p:
            return (self.LOGIN_NEED_USER, "用户不存在")

        if p.password != self.saltMD5(name, password):
            return (self.LOGIN_NEED_PWD, "密码错误")
        else:
            log.msg("用户", p.name, "(", p.nick, ")", "登录, 位置", p.locate)
            self.setPlayer(p)
            return (self.LOGIN_SUCCESS, "欢迎登录," + p.nick, p.locate)

    def remote_logout(self, name):
        p = self.getPlayer(name)
        if p:
            log.msg("用户", p.name, "(", p.nick, ")", "退出, 位置", p.locate)
            self.delPlayer(name)

    def remote_register(self, name, password):
        pass

    def remote_autocomplete(self, name, command):
        p = self.getPlayer(name)
        if p:
            cmd = pickle.loads(command)
            return self.complete(p, cmd)
        
    def remote_handle(self, name, command):
        p = self.getPlayer(name)
        if p:
            cmd = pickle.loads(command)
            hdr = self.getHandler(cmd.args[0])
            if hdr:
                return hdr.handle(p, cmd)
            else:
                return "未定义指令: " + cmd.args[0]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: %s config.json" % (sys.argv[0])
        sys.exit(1)
    config = json.load(open(sys.argv[1], 'r'))
    log.startLogging(sys.stdout)
    #log.startLogging(open(config["logfile"], 'w'))
    service = PlayerService(config["dbpath"], config["nodes"])
    reactor.listenTCP(config["port"], pb.PBServerFactory(service),
                      interface = config["ip"])
    reactor.run()
