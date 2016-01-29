#!/usr/bin/env python
#encoding=utf8

# File Name: players.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 21时03分38秒

from mutils.dbproxy import Persistent
from player.commands import HandlersManager

import sqlite3, os, hashlib

class Player(Persistent):
    
    TABLE = "t_player"
    COLS = ["name", "password", "nick", "locate"] #...

    def handle(self, command):
        pass



class PlayerManager(HandlersManager):

    def __init__(self, dbpath):
        HandlersManager.__init__(self)
        if os.path.exists(dbpath):
            self._conn = sqlite3.connect(dbpath)
        else:
            self._conn = sqlite3.connect(dbpath)
            self._initDB(self._conn)
            
        self._players = {}

    def getPlayer(self, name):
        if name in self._players:
            return self._players[name]

    def setPlayer(self, player):
        self._players[player.name] = player

    def delPlayer(self, name):
        if name in self._players:
            self._players[name].flush()
            del self._players[name]
            return True
        else:
            return False

    def loginPlayer(self, pname):
        player = Player(self._conn, name=pname)
        if player.inited():
            return player
        else:
            return False

    SALT1 = "bsfwskzb"
    SALT2 = "ncwai,x#"
        
    def saltMD5(self, user, password):
        first = hashlib.md5(user + self.SALT1 + password).hexdigest()
        return hashlib.md5(first[:16] + self.SALT2 + first[17:]).hexdigest()

    def _initDB(self, conn):
        conn.execute("CREATE TABLE t_player (name varchar(32) primary key" +
                     ", password char(32), nick varchar(32), locate text)")
        conn.execute("INSERT INTO t_player VALUES('admin', '" +
                     self.saltMD5("admin", "123456") + "', '主角', 'Default')")
        conn.commit()
