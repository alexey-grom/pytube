# -*- coding: utf-8 -*-
from aiohttp import web

from pytube.server import middlewares


def run_server(setup_routes, host=None, port=None, **context):
    app = web.Application(middlewares=[
        middlewares.context_middleware(**context),
        middlewares.timing_middleware(),
    ])
    setup_routes(app)
    web.run_app(app, host=host, port=port)
