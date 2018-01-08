# -*- coding: utf-8 -*-
from pytube.cli.decorators import command
from pytube.cli.decorators import redirect_output
from pytube.requests import create_get_content
from pytube.youtube.search import search


@command('search')
@redirect_output
async def search_command(arguments, **kwargs):
    """
    Usage:
      pytube [options] {command} [--type=<entities type>]
                                 [--sorting=<sorting alias>]
                                 [--limit=<pages count>]
                                 <query>...
    """
    query = ' '.join(arguments.get('<query>'))
    limit = int(arguments.pop('--limit', 0))
    sorting = arguments.pop('--sorting', None)
    type = arguments.pop('--type', None)

    results = []

    async with create_get_content(**kwargs) as get_content:
        paginator = search(get_content, query, sorting=sorting, type=type)
        count = 0
        async for data in paginator:
            results.append(data)
            count += 1
            if limit and count >= limit:
                break

    return results
