# -*- coding: utf-8 -*-
from pytube.cli.decorators import command
from pytube.cli.decorators import redirect_output
from pytube.player_config import player_config
from pytube.utils import print_streams


@command
async def list_command(arguments, **kwargs):
    """
    Usage:
      pytube [options] list [--output=<filename>] <url>...
    """
    result = {}
    urls = arguments.get('<url>')

    for url in urls:
        async with player_config(url, **kwargs) as (config, fmts):
            result[url] = fmts
            result[url] = sorted(fmts, key=lambda stream: stream.sort_key)

    for url, streams in result.items():
        print(url)
        print_streams(streams, ' ' * 2)
        print()


@redirect_output
@command
async def dump_streams(arguments, **kwargs):
    """
    Usage:
      pytube [options] dump-streams [--output=<filename>] <url>...
    """
    result = {}
    urls = arguments.get('<url>')
    for url in urls:
        async with player_config(url, **kwargs) as (config, fmts):
            result[url] = [
                fmt.raw_data
                for fmt in fmts
            ]
    return result


@redirect_output
@command
async def dump_player_config(arguments, **kwargs):
    """
    Usage:
      pytube [options] dump-player-config [--output=<filename>] <url>...

    """
    result = {}
    urls = arguments.get('<url>')
    for url in urls:
        async with player_config(url, **kwargs) as (config, fmts):
            result[url] = config
    return result


@command
async def download(arguments, **kwargs):
    """
    Usage:
      pytube [options] download [--output=<filename>] <url>...
    """
    raise NotImplementedError


@command
async def server(arguments, **kwargs):
    """
    Usage:
      pytube [options] server [--host=<host>] [--port=<port>]

    Options:
      --host=<host>         [default:0.0.0.0]
      --port=<port>         [default:8080]

    """
    raise NotImplementedError
