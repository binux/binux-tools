#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<huangkuan@duokan.com>
#         http://binux.me
# Created on Mon 14 May 2012 04:40:15 PM CST

import sys
def info(type, value, tb):
    if hasattr(sys, 'ps1') or not (
            sys.stderr.isatty() and sys.stdin.isatty()
            ) or issubclass(type, SyntaxError):
        sys.__excepthook__(type, value, tb)
    else:
        import traceback, pdb
        traceback.print_exception(type, value, tb)
        print
        pdb.pm()
sys.excepthook = info

