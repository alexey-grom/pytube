# -*- coding: utf-8 -*-
from aiohttp import web

from pytube import json


def json_reponse(func):
    async def wrapper(self, *args, **kwargs):
        dumps_func = json.dumps
        if 'indent' in self.request.query:
            dumps_func = json.indent_dumps
        return web.json_response(await func(self, *args, **kwargs),
                                 dumps=dumps_func)
    return wrapper
