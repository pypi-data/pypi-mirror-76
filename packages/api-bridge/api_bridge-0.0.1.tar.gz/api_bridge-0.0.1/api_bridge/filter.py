#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.1"

__all__ = ('Filter',)

from operator import getitem
from typing import Dict, Any


class Filter:
    out: Dict[str, Any]

    def __init__(self, **out: str):
        self.out = out

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if self.out is None: return dict()
        output = dict()
        for name, value, in self.out.items():
            subs = value.split()
            item = getitem(data, subs[0])
            for sub in subs[1:]:
                item = getitem(item, sub)
            output[name] = item
        return output


if __name__ == '__main__': pass
