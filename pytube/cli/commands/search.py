# -*- coding: utf-8 -*-
from pytube.cli.decorators import command, redirect_output
from pytube.requests import create_get_content
from pytube.youtube.search import search


@command('search')
@redirect_output
async def search_command(arguments, **kwargs):
    """
    Usage:
      pytube [options] {command} [--limit=<count>] <query>...
    """
    results = {}
    limit = int(arguments.pop('--limit', 0))
    query = ' '.join(arguments.get('<query>'))
    results[query] = []
    async with create_get_content(**kwargs) as get_content:
        paginator = search(get_content, query)
        count = 0
        while True:
            data = await paginator.next()
            results[query].append(data)
            if not paginator.has_more:
                break
            count += 1
            if limit and count >= limit:
                break
    return results
