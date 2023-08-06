#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.2"

__all__ = ('Container',)

from typing import Optional, Dict, Any


class Container:
    value: Optional[Dict[str, Any]]

    def __init__(self): self.value = None

    def __call__(self, value) -> None:
        self.value = value

    def __str__(self) -> str: return str(self.value)

    def __repr__(self) -> str: return str(self)


if __name__ == '__main__': pass
