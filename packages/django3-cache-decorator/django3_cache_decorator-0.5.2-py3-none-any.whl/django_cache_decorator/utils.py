# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

import hashlib

def cache_get_key(*args, **kwargs):
    serialise = []
    for arg in args:
        serialise.append(str(arg))
    for key,arg in kwargs.items():
        serialise.append(str(key))
        serialise.append(str(arg))

    full_str = "".join(serialise)
    key = hashlib.md5(full_str.encode('utf-8')).hexdigest()
    return key
