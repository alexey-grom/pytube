# -*- coding: utf-8 -*-
from time import time

from aiohttp import web


def context_middleware(**context):
    data = context.copy()
    data['started'] = time()

    @web.middleware
    async def middleware(request, handler):
        request['context'] = data.copy()
        return await handler(request)

    return middleware


def timing_middleware():
    @web.middleware
    async def middleware(request, handler):
        started = time()
        response = await handler(request)
        response.headers['X-Elapsed'] = '{:.5f}'.format(time() - started)
        return response
    return middleware
