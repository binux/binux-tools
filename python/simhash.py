#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2010-11-30

@author: binux
'''

import hashlib

class simhash():
    '''
    simhash
    '''


    def __init__(self, tokens=[]):
        '''
        Constructor
        '''
        self.hash_algorithm = hashlib.md5
        self.hashbits = self.hash_algorithm().digest_size * 8
        self.hash = self.simhash(tokens)
        
    def __str__(self):
        return "{0:x}".format(self.hash)
    
    def __long__(self):
        return long(self.hash)
    
    def __float__(self):
        return float(self.hash)
    
    def simhash(self, tokens):
        v = [0] * self.hashbits
        
        for t, w in [(self._string_hash(x[0]), x[1]) for x in tokens]:
            bitmask = 0
            
            for i in range(self.hashbits):
                bitmask = 1 << i
                if t & bitmask:
                    v[i] += w
                else:
                    v[i] -= w
            
        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] > 0:
                fingerprint += 1 << i
                    
        return fingerprint
        
    def _string_hash(self, v):
        return int(self.hash_algorithm(v).hexdigest(), 16)
        
if __name__ == "__main__":
    t = (("天龙八部", 12345),
         ("天龙八部", 0),
         ("天龙八部", -1),
         ("天龙八部", 1),
         ("天龙八部", 0.1),
         ("天龙八部", 0.5),
         ("天龙八部", 321543.465647),
         ("", 1),
         ("123124", 1),
         ("asdfab", 1),
         ("aaa", 1),
         ("a", 1),
         ("bbb", 1),
         )
    
    print simhash(t)
        
