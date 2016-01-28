#!/usr/bin/env python
#encoding=utf8

# File Name: dbproxy.py
# Author: LSP
# Created Time: 2016年01月27日 星期三 15时42分42秒

class Persistent(object):
    """
    持久化对象
    """
    TABLE = ""
    COLS = []

    def __init__(self, conn, **kw):
        self._attributes = {}
        self._conn = conn
        self._updates = {}
        #build sql conditions
        self._cond = ""
        self._values = []
        for k in kw:
            if not self._values:
                self._cond += k + " = ?"
            else:
                self._cond += " and " + k + " = ?"
            self._values.append(kw[k])

        self.load()

    def __getattr__(self, key):
        return self._attributes[key]

    def __setattr__(self, key, value):
        #warning: column's name can't startswith '_'!!!
        if key[0] == '_':
            object.__setattr__(self, key, value)
        else:
            self._attributes[key] = value
            self._updates[key] = True

    def inited(self):
        return bool(self._attributes)

    def load(self):
        query = "select %s from %s where %s" % (", ".join(self.COLS),
                                                self.TABLE, self._cond)
        cursor = self._conn.cursor()
        cursor.execute(query, self._values)
        result = cursor.fetchone()
        if result:
            i = 0
            while i < len(self.COLS):
                self._attributes[self.COLS[i]] = result[i].encode("utf-8")
                i += 1
        cursor.close()
        
    def flush(self):
        #update changed attributes only
        if not self._updates:
            return
            
        sets = ""
        values = []
        for k in self._updates:
            if not values:
                sets += k + " = ?"
            else:
                sets += ", " + k + " = ?"
            values.append(self._attributes[k])
        
        update = "update %s set %s where %s" % (self.TABLE, sets, self._cond)
        cursor = self._conn.cursor()
        cursor.execute(update, values + self._values)
        cursor.close()
        self._conn.commit()
        self._updates.clear()


if __name__ == '__main__':
    #just for test
    import sqlite3
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("create table test (id integer primary key, value text)")
    cursor.execute("insert into test (value) values('asdf')")
    cursor.execute("insert into test (value) values('qwer')")

    class Test(Persistent):
        TABLE = 'test'
        COLS = ['id', 'value']

    t = Test(conn, id=1)
    assert(t.value == "asdf")
    t.value = "zxcv"
    t.flush()
    nt = Test(conn, id=1)
    assert(nt.value == "zxcv")
