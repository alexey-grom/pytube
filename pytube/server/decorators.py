# -*- coding: utf-8 -*-
from time import time

from aiohttp import web

from pytube import json


def json_response(func):
    async def wrapper(self, *args, **kwargs):
        dumps_func = json.dumps
        if 'indent' in self.request.query:
            dumps_func = json.indent_dumps
        return web.json_response(await func(self, *args, **kwargs),
                                 dumps=dumps_func)
    return wrapper


def timing(func):
    async def wrapper(self, *args, **kwargs):
        started = time()
        result = await func(self, *args, **kwargs)
        result['elapsed'] = time() - started
        return result
    return wrapper
