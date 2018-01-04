# -*- coding: utf-8 -*-
from pytube.cli.decorators import command, redirect_output
from pytube.requests import create_get_content


@command('try-request')
@redirect_output
async def try_request(arguments, **kwargs):
    """
    Usage:
      pytube [options] {command} [<url>]
    """
    url = arguments.get('<url>') or 'https://httpbin.org/anything'
    async with create_get_content(**kwargs) as get_content:
        return await get_content(method='GET', url=url)
