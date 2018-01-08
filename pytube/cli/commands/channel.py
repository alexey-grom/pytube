# -*- coding: utf-8 -*-
from pytube.cli.decorators import command
from pytube.cli.decorators import redirect_output
from pytube.requests import create_get_content
from pytube.youtube.channel import parse_channel


@command('channel')
@redirect_output
async def channel_command(arguments, **kwargs):
    """
    Usage:
      pytube [options] {command} <id>...
    """
    ids = arguments.pop('<id>', None)
    result = {}

    async with create_get_content(**kwargs) as get_content:
        for id in ids:
            result[id] = await parse_channel(get_content, id)

    return result
