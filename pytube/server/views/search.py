# -*- coding: utf-8 -*-
from aiohttp import web

from .base import PytubeMixin
from pytube.requests import create_get_content
from pytube.server.decorators import json_response
from pytube.server.decorators import timing
from pytube.youtube.search import search


class SearchView(PytubeMixin, web.View):
    @json_response
    @timing
    async def get(self):
        query = self.request.query.get('query')
        if not query:
            raise web.HTTPBadRequest

        try:
            limit = self.request.query.get('limit', 0)
            limit = int(limit) or 30  # actual youtube's limit is 21
        except ValueError:
            raise web.HTTPBadRequest
        sorting = self.request.query.get('sorting')
        type = self.request.query.get('type')

        async with create_get_content(**self.opts) as get_content:
            try:
                paginator = \
                    search(get_content, query, sorting=sorting, type=type)
            except AssertionError:
                raise web.HTTPBadRequest

            results = []
            count = 0
            async for data in paginator:
                results.append(data)
                count += 1
                if limit and count >= limit:
                    break

            return {
                'query': query,
                'results': results,
            }
