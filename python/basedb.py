#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2010-12-28

@author: binux
'''

import logging
import datetime
import itertools
import MySQLdb

logger = logging.getLogger("default")

def sqlify(obj): 
    r"""
    converts `obj` to its proper SQL version

        >>> sqlify(None)
        'NULL'
        >>> sqlify(True)
        "'t'"
        >>> sqlify(3)
        '3'
    """
    # because `1 == True and hash(1) == hash(True)`
    # we have to do this the hard way...

    if obj is None:
        return 'NULL'
    elif obj is True:
        return "'t'"
    elif obj is False:
        return "'f'"
    elif datetime and isinstance(obj, datetime.datetime):
        return "'%s'" % MySQLdb.escape_string(str(obj.isoformat()))
    elif isinstance(obj, basestring):
        if isinstance(obj, unicode): obj = obj.encode('utf8')
        return "'%s'" % MySQLdb.escape_string(str(obj))
    else:
        return str(obj)
    
def safestr(obj, encoding='utf-8'):
    r"""
    Converts any given object to utf-8 encoded string. 
    
        >>> safestr('hello')
        'hello'
        >>> safestr(u'\u1234')
        '\xe1\x88\xb4'
        >>> safestr(2)
        '2'
    """
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    elif isinstance(obj, str):
        return obj
    elif hasattr(obj, 'next') and hasattr(obj, '__iter__'): # iterator
        return itertools.imap(safestr, obj)
    else:
        return str(obj)

class BaseDB(object):
    '''
    BaseDB

    dbcur should be overwirte
    '''
    dbcur = None
    autocommit = True

    def _execute(self, sql_query):
        self.dbcur.execute(sql_query)
    
    def _select(self, tablename, what="*", where="", limit=None):
        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where: sql_query += " WHERE %s" % where
        if limit: sql_query += " LIMIT %d" % limit
        logger.debug("<sql: %s>" % sql_query)

        self.dbcur.execute(sql_query)
        if limit == 1:
            return self.dbcur.fetchone()
        else:
            return self.dbcur.fetchall()
 
    def _replace(self, tablename, **values):
        q = lambda x: "(" + x + ")"
        if values:
            _keys = ", ".join(values.keys())
            _values = ", ".join([sqlify(v) for v in values.values()])
            sql_query = "REPLACE INTO %s " % tablename + q(_keys) + " VALUES " + q(_values)
        else:
            sql_query = "REPLACE INTO %s DEFAULT VALUES" % tablename
        logger.debug("<sql: %s>" % sql_query)
        
        self.dbcur.execute(sql_query)
        lastrowid = self.dbcur.lastrowid
        if self.autocommit: 
            self._execute("COMMIT;")
        return lastrowid

    def _insert(self, tablename, **values):
        q = lambda x: "(" + x + ")"
        if values:
            _keys = ", ".join(values.keys())
            _values = ", ".join([sqlify(v) for v in values.values()])
            sql_query = "INSERT INTO %s " % tablename + q(_keys) + " VALUES " + q(_values)
        else:
            sql_query = "INSERT INTO %s DEFAULT VALUES" % tablename
        logger.debug("<sql: %s>" % sql_query)
        
        self.dbcur.execute(sql_query)
        lastrowid = self.dbcur.lastrowid
        if self.autocommit: 
            self._execute("COMMIT;")
        return lastrowid
    
    def _update(self, tablename, where, **values):
        _key_values = ", ".join([k + " = " + sqlify(v) for k, v in values.items()]) 
        sql_query = "UPDATE %s SET %s WHERE %s" % (tablename, _key_values, where)
        logger.debug("<sql: %s>" % sql_query)
        
        ret = self.dbcur.execute(sql_query)
        if self.autocommit: 
            self._execute("COMMIT;")
        return ret
    
    def _delete(self, tablename, where):
        sql_query = "DELETE FROM %s" % tablename
        if where: sql_query += " WHERE %s" % where
        logger.debug("<sql: %s>" % sql_query)

        ret = self.dbcur.execute(sql_query)
        if self.autocommit: 
            self._execute("COMMIT;")
        return ret

class IterDB:
    """
    for traverse

    iter should be overwrite
    """
    dbcur = None
    iter = None
    def get_each(self, where=""):
        for group in self.get_group():
            for args in group:
                yield args

    def get_group(self, where=""):
        return self.iter

    class iterator(object):
        '''
        fetch list from mysql
        '''
    
        def __init__(self, db, table, what, where="", offset_order="id", cache=5000, start_id=0):
            '''
            Constructor
            '''
            self.dbcur = db.cursor()

            self.cur_id = start_id
            self.cache = cache
            self.table = table
            self.what = what
            self.where = where
            self.offset_order = offset_order
            self.offset = 0

        def __iter__(self):
            return self
        
        def next(self):
            self.sql = "SELECT %s FROM %s" % (self.what, self.table)
            self.sql += " WHERE `%s` > %s" % (self.offset_order, self.cur_id)
            if self.where: self.sql += " AND %s" % self.where
            self.sql += " ORDER BY `%s` LIMIT %d" % (self.offset_order, self.cache)
            print self.sql
            data_len = self.dbcur.execute(self.sql)
            if not data_len:
                raise StopIteration

            print "offset: %d, start_id: %s" % (self.offset, self.cur_id)
            row = self.dbcur.fetchall()
            self.cur_id = max(row, key=lambda x: x[0])[0]
            self.offset += self.cache
            return row
        
