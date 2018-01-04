# -*- coding: utf-8 -*-
from pytube.cli.decorators import command, redirect_output
from pytube.requests import create_get_content
from pytube.youtube.search import search_keywords


@command('search-keywords')
@redirect_output
async def search_keywords_command(arguments, **kwargs):
    """
    Usage:
      pytube [options] {command} <query>...
    """
    results = {}
    query = ' '.join(arguments.get('<query>'))
    async with create_get_content(**kwargs) as get_content:
        results[query] = await search_keywords(get_content, query)
    return results
