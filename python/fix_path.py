#!/usr/bin/env python
# encoding: utf-8

import os
import sys

_fixpath = os.path.join(os.path.dirname(__file__), '..')
if _fixpath not in sys.path:
    sys.path.insert(1, _fixpath)
