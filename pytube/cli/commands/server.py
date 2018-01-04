# -*- coding: utf-8 -*-
from pytube.cli.decorators import command
from pytube.server import run_server
from pytube.utils import import_name


@command()
def server(arguments, **kwargs):
    """
    Usage:
      pytube [options] {command}
             [--host=<host>] [--port=<port>]
             [--setup-routes=<import-path>...]

    Options:
      --host=<host>                  [default: 0.0.0.0]
      --port=<port>                  [default: 8080]
      --setup-routes=<import-path>   [default: pytube.server.routes.install]

    """

    host = arguments.pop('--host')
    port = int(arguments.pop('--port'))

    def _setup_routes(app):
        for path in arguments.pop('--setup-routes'):
            setup_routes = import_name(path)
            assert callable(setup_routes)
            setup_routes(app)

    run_server(_setup_routes, host=host, port=port, **kwargs)
