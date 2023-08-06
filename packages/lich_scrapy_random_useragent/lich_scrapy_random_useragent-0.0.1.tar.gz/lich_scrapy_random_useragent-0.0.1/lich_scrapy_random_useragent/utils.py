# -*- coding: utf-8 -*-
import os
import io
import json

def read(path):
    with io.open(path, encoding='utf-8', mode='rt') as fp:
        return json.loads(fp.read())

def bytes_to_text(s):
    if isinstance(s, bytes):
        return s.decode("utf-8")
    return s