# -*- coding: utf-8 -*-
import logging

from aiohttp import web

from .base import PytubeMixin
from pytube.requests import create_get_content
from pytube.server.decorators import json_response
from pytube.server.decorators import timing
from pytube.youtube.feed import parse_feed


logger = logging.getLogger(__name__)


class FeedView(PytubeMixin, web.View):
    @json_response
    @timing
    async def get(self):
        id = self.request.query.get('id')
        if not id:
            raise web.HTTPBadRequest
        async with create_get_content(**self.opts) as get_content:
            return await parse_feed(get_content, id)
