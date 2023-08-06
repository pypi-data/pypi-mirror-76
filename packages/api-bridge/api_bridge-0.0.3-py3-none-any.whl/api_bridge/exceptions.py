#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.3"

__all__ = ('APIException', 'ValidationException',)


class APIException(Exception): pass


class ValidationException(APIException): pass


if __name__ == '__main__': pass
