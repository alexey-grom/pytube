# -*- coding: utf-8 -*-
from pytube.cli.decorators import command
from pytube.cli.decorators import redirect_output
from pytube.requests import create_get_content
from pytube.youtube.video import video_parser


@command()
@redirect_output
async def dump_player_config(arguments, **kwargs):
    """
    Usage:
      pytube [options] {command} [--output=<filename>] <url>...

    """
    result = {}
    urls = arguments.get('<url>')
    for url in urls:
        async with create_get_content(**kwargs) as get_content:
            config, _ = await video_parser(get_content, url)
            result[url] = config
    return result
