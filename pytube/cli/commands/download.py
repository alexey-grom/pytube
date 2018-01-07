# -*- coding: utf-8 -*-
from subprocess import call

from pytube.cli.decorators import command
from pytube.requests import create_get_content
from pytube.utils import choose_stream
from pytube.utils import format_filename
from pytube.utils import safe_filename
from pytube.youtube.video import video_parser


@command()
async def download(arguments, **kwargs):
    """
    Usage:
      pytube [options] {command}
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
        async with create_get_content(**kwargs) as get_content:
            config, fmts = await video_parser(get_content, url)
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
