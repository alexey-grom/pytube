# -*- coding: utf-8 -*-
from time import time

from aiohttp import web


def context_middleware(**opts):
    context = {
        'started': time(),
        'opts': opts.copy(),
    }

    @web.middleware
    async def middleware(request, handler):
        request['context'] = context.copy()
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
