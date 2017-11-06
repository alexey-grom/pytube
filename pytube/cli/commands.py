# -*- coding: utf-8 -*-
from subprocess import call

from pytube.cli.decorators import command
from pytube.cli.decorators import redirect_output
from pytube.player_config import player_config
from pytube.utils import choose_stream
from pytube.utils import format_filename
from pytube.utils import print_streams
from pytube.utils import safe_filename


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
      pytube [options] download
             [--output=<filename>]
             [--itag=<itag>]
             [--type=<type>]
             [--bitrate=<bitrate>]
             [--resolution=<resolution>]
             [--is-live]
             [--is-3d]
             [--fps=<fps>]
             [--quality=<quality>]
             [--format=<format>]
             [--video-codec=<video-codec>]
             [--audio-codec=<audio-codec>]
             <url>...
    """
    fmt = arguments.pop('--output', None)
    filters = {
        k.lstrip('--').replace('-', '_'): v
        for k, v in arguments.items()
        if k.startswith('--')
    }

    urls = arguments.get('<url>')
    for url in urls:
        async with player_config(url, **kwargs) as (config, fmts):
            stream = choose_stream(fmts, **filters)
            assert stream, 'Stream with required filters not found'

            filename = safe_filename(format_filename(config, stream), fmt)

            opts = ['-O', filename, stream.url]
            proxy = kwargs.get('proxy', None)
            if proxy:
                opts = ['-e', 'use_proxy=yes',
                        '-e', 'http_proxy={}'.format(proxy),
                        '-e', 'https_proxy={}'.format(proxy)] + \
                    opts
            call(['wget'] + opts)


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
