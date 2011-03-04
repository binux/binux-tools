#!python
# coding: utf-8
'''
author: binux (17175297.hk@gmail.com)
'''

import scws_py
from scws_py import SCWS_XDICT_TXT, SCWS_XDICT_XDB, SCWS_XDICT_MEM
from scws_py import SCWS_MULTI_NONE, SCWS_MULTI_SHORT, SCWS_MULTI_DUALITY, SCWS_MULTI_ZMAIN, SCWS_MULTI_ZALL

def topword_repr(self):
    return '<top_word:%s\t/%s\t(%d)%f>' % (self.word, self.attr, self.times, self.weight)
scws_py.topword.__repr__ =  topword_repr

class scws(object):
    def __init__(self, dict="", rule="", charset="utf-8", 
          ignore=False, 
          multi=SCWS_MULTI_NONE,
          duality=False,
          debug=False):
        self._scws = scws_py.SCWS()
        if isinstance(dict, str):
            if self._scws.set_dict(dict, SCWS_XDICT_XDB) == -1:
              raise "error when add_dict"
        else:
          for each in dict:
              if isinstance(each, tuple):
                  if len(each) == 2:
                    if self._scws.add_dict(each[0], each[1]) == -1:
                      raise ("error when add_dict(%s, %d)" % (each[0], each[1]))
                  else:
                      raise "dict format error"
              elif isinstance(each, str):
                  if self._scws.add_dict(each, SCWS_XDICT_XDB) == -1:
                      raise ("error when add_dict(%s, %d)" % (each, SCWS_XDICT_XDB))

        if rule: self._scws.set_rule(rule)
        self._scws.set_charset(charset)
        self._scws.set_ignore(ignore)
        self._scws.set_multi(multi)
        self._scws.set_duality(duality)
        self._scws.set_debug(debug)

    def segmentation(self, text):
        class Word(object):
            word = ""
            off = 0
            idf = 0
            attr = ""
            def __repr__(self):
                return '<word:%s\t/%s\t%f>' % (self.word, self.attr, self.idf)

        if isinstance(text, unicode):
          text = text.encode("utf-8")
        self._scws.send_text(text, len(text))
        ret = self._scws.get_result()
        while ret:
            for each in ret:
                result = Word()
                result.word = text[each.off:each.off+each.len]
                result.off = each.off
                result.idf = each.idf
                result.attr = each.attr
                yield result
            ret = self._scws.get_result()
    
    def gettop(self, text, limit = 10, attr=""):
        if isinstance(text, unicode):
          text = text.encode("utf-8")
        self._scws.send_text(text, len(text))
        return self._scws.get_tops(limit, attr)
