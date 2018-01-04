# -*- coding: utf-8 -*-
from pytube.cli.decorators import command
from pytube.utils import print_streams
from pytube.requests import create_get_content
from pytube.youtube.video import video_parser


@command('list')
async def list_command(arguments, **kwargs):
    """
    Usage:
      pytube [options] {command} [--output=<filename>] <url>...
    """
    result = {}
    urls = arguments.get('<url>')

    for url in urls:
        async with create_get_content(**kwargs) as get_content:
            config, fmts = await video_parser(get_content, url)
            result[url] = sorted(fmts, key=lambda stream: stream.sort_key)

    for url, streams in result.items():
        print(url)
        print_streams(streams, ' ' * 2)
        print()
