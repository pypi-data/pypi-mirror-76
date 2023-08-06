#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.3"

__all__ = ('API',)

from api_bridge.methods import Method
from api_bridge.container import Container
from api_bridge.url import valid_url
from api_bridge.exceptions import APIException, ValidationException

from requests import request, Response
from operator import gt

from typing import Optional, Union, Callable, Dict, Any


class API:
    url: str
    method: Method
    result_filter: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]
    callback: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]
    validate: Optional[Callable[[Dict[str, Any]], bool]]
    post_data: Optional[Dict[str, Any]]

    response: Optional[Response]

    def __init__(self,
                 url: str,
                 method: Method = Method.GET,
                 result_filter: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
                 validate: Optional[Callable[[Dict[str, Any]], bool]] = None,
                 post_data: Optional[Dict[str, Any]] = None
                 ):
        self.url = url
        if not valid_url(url): pass
        self.method = method
        self.response = None
        self.result_filter = result_filter
        self.validate = validate
        self.post_data = post_data

    def __bool__(self) -> bool: return self.response is not None and self.response.ok

    def __repr__(self) -> str: pass

    def __str__(self) -> str: pass

    def __gt__(self, other) -> Union['API', Container]:
        self.request()
        other(self.result_filter(self.json()) if self.result_filter else self.json())
        return other

    def __rshift__(self, other) -> Union['API', Container]: return self > other

    def __call__(self, filter_data=None):
        if filter_data is not None:
            self.url = self.url.format(**filter_data)
        self.request()

    def json(self):
        if self.response is not None: return self.response.json()
        else: raise APIException('Request not done yet!')

    def request(self) -> None:
        try: self.response = request(method=str(self.method), url=self.url, data=self.post_data or dict())
        except Exception as exc: raise APIException(f'{self.method}-request for {self.url} failed [{exc}]!')
        else:
            if not self.response.ok or (self.validate is not None and not self.validate(self.json())):
                raise ValidationException(f'Response code from "{self.url}" was not ok or validation '
                                   f'"{self.validate.__name__ if self.validate is not None else None}" failed!')

    @staticmethod
    def chain(*apis) -> Container:
        current: API = apis[0]
        for api in apis[1:]:
            current = gt(current, api)
        return current > Container()


if __name__ == '__main__': pass
