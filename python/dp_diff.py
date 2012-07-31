#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<17175297.hk@gmail.com>
#         http://binux.me
# Created on Mon 16 Jul 2012 11:57:34 AM CST

import sys
from difflib import SequenceMatcher

MIN_INT = -sys.maxint
MAX_INT = sys.maxint

class DP_diff:
    """a diff function base on Advanced Dynamic Programming

    >>> from pprint import pprint
    >>> s = DP_diff("GAATTCAGTTA", "GGATCGA")
    >>> pprint(s._matrix)
    [[0, -2, -4, -6, -8, -10, -12, -14, -16, -18, -20, -22],
     [-2, 2.0, 0.0, -2.0, -4.0, -6.0, -8.0, -10.0, -12.0, -14.0, -16.0, -18.0],
     [-4, 0.0, 1.0, -1.0, -3.0, -5.0, -7.0, -9.0, -8.0, -10.0, -12.0, -14.0],
     [-6, -2.0, 2.0, 3.0, 1.0, -1.0, -3.0, -5.0, -7.0, -9.0, -11.0, -10.0],
     [-8, -4.0, 0.0, 1.0, 5.0, 3.0, 1.0, -1.0, -3.0, -5.0, -7.0, -9.0],
     [-10, -6.0, -2.0, -1.0, 3.0, 4.0, 5.0, 3.0, 1.0, -1.0, -3.0, -5.0],
     [-12, -8.0, -4.0, -3.0, 1.0, 2.0, 3.0, 4.0, 5.0, 3.0, 1.0, -1.0],
     [-14, -10.0, -6.0, -2.0, -1.0, 0.0, 1.0, 5.0, 3.0, 4.0, 2.0, 3.0]]
    >>> s.get_opcodes()
    [('equal', 0, 1, 0, 1), ('replace', 1, 2, 1, 2), ('equal', 2, 3, 2, 3), ('delete', 3, 4, 3, 3), ('equal', 4, 6, 3, 5), ('delete', 6, 7, 5, 5), ('equal', 7, 8, 5, 6), ('delete', 8, 10, 6, 6), ('equal', 10, 11, 6, 7)]
    >>> DP_diff("", "AABBCC").get_opcodes()
    [('insert', 0, 0, 0, 6)]
    >>> DP_diff("AABBCC", "").get_opcodes()
    [('delete', 0, 6, 0, 0)]
    """
    def __init__(self,
            a, b,
            isjunk=None,
            compare_func=None,
            pool=None,
            delete_w=-2,
            insert_w=-2,
            replace_w=-1,
            equal_w=2,
            min_similar=0.8,
            skip_offset=0):
        self.options = {}
        self.options['isjunk'] = isjunk
        if compare_func:
            self.options['compare_func'] = compare_func
        else:
            self.options['compare_func'] = CachedSeqComparer()
        self.options['pool'] = pool
        self.options['delete_w'] = delete_w
        self.options['insert_w'] = insert_w
        self.options['replace_w'] = replace_w
        self.options['equal_w'] = equal_w
        self.options['min_similar'] = min_similar
        self.options['skip_offset'] = skip_offset

        self.set_seq(a, b)

    def set_seq(self, a, b):
        self.a = a
        self.b = b
        self._build_matrix()

    def get_opcodes(self):
        m = self._matrix
        o = self._opt
        result = []
        a2, b2 = i, j = len(m)-1, len(m[0])-1
        while o[i][j]:
            opt = o[i][j]
            if opt == "equal" or o[i][j] == "replace":
                while(o[i][j] == opt):
                    i, j = i-1, j-1
            elif opt == "insert":
                while(o[i][j] == opt):
                    i, j = i-1, j
            elif opt == "delete":
                while(o[i][j] == opt):
                    i, j = i, j-1
            else:
                break
            result.append( (opt, j, b2, i, a2) )
            a2, b2 = i, j
        result.reverse()
        return result

    def score(self):
        return self._matrix[-1][-1]

    def ratio(self):
        return self.score()

    def _build_matrix(self):
        if len(self.a) > 10 and len(self.b) > 10 and self.options['pool']:
            self._matrix, self._opt = self.options['pool'].apply(build_matrix, (self.a, self.b, self.options))
        else:
            self._matrix, self._opt = build_matrix(self.a, self.b, self.options)

def build_matrix(a, b, options):
    m = [[MIN_INT for col in xrange(len(a)+1)] for row in xrange(len(b)+1)]
    o = [["null_opt" for col in xrange(len(a)+1)] for row in xrange(len(b)+1)]
    for j in xrange(1, len(a)+1):
        m[0][j] = j*options['delete_w']
        o[0][j] = "delete"
    for i in xrange(1, len(b)+1):
        m[i][0] = i*options['insert_w']
        o[i][0] = "insert"
    m[0][0] = 0

    pre_offset = 0
    equal_step = 0
    start_offset = 0
    skip_offset = options['skip_offset']
    _similar = options['compare_func']
    isjunk = options['isjunk']
    for i in xrange(1, len(b)+1):
        first_match = MAX_INT 
        for j in xrange(1, len(a)+1):
            if skip_offset and (j < start_offset or first_match+skip_offset < j):
                score = MIN_INT
                a1 = MIN_INT
            else:
                similar_ratio = _similar(a[j-1], b[i-1], isjunk=isjunk)
                if similar_ratio < options['min_similar']:
                    score = options['replace_w']
                else:
                    score = similar_ratio*options['equal_w']
                a1 = m[i-1][j-1]+score
            a2 = m[i-1][j]+options['insert_w']
            a3 = m[i][j-1]+options['delete_w']
            m[i][j] = max(a1, a2, a3)
            if m[i][j] == a1 and score > 0:
                if first_match == MAX_INT and skip_offset:
                    first_match = j
                    if pre_offset + 1 == j:
                        equal_step += 1
                        if equal_step >= skip_offset:
                            start_offset = j - skip_offset
                    else:
                        equal_step = 0
                    pre_offset = j
                o[i][j] = "equal"
            elif m[i][j] == a1 and score < 0:
                o[i][j] = "replace"
            elif m[i][j] == a2:
                o[i][j] = "insert" # go down
            elif m[i][j] == a3:
                o[i][j] = "delete" # go right

    return m, o

class CachedSeqComparer:
    def __init__(self):
        self.cache = None

    def __call__(self, a, b, isjunk=None):
        s = None
        if self.cache:
            if self.cache.b == b:
                s = self.cache.set_seq1(a)
            elif self.cache.b == a:
                s = self.cache.set_seq1(b)
            elif self.cache.a == a:
                a, b = b, a
            #elif self.cache.a == b:
                #pass
        if not s:
            self.cache = s = SequenceMatcher(isjunk, a, b)

        ratio = s.quick_ratio()
        if a in b or b in a:
            ratio = (1-(1-ratio)/2)

        return ratio

if __name__ == "__main__":
    import doctest
    doctest.testmod()
