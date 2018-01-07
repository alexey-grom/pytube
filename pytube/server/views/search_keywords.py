# -*- coding: utf-8 -*-
import logging

from aiohttp import web

from .base import PytubeMixin
from pytube.requests import create_get_content
from pytube.server.decorators import json_response
from pytube.server.decorators import timing
from pytube.youtube.search import search_keywords


logger = logging.getLogger(__name__)


class SearchKeywordsView(PytubeMixin, web.View):
    @json_response
    @timing
    async def get(self):
        query = self.request.query.get('query')
        if not query:
            raise web.HTTPBadRequest
        async with create_get_content(**self.opts) as get_content:
            return {
                'query': query,
                'keywords': await search_keywords(get_content, query),
            }
