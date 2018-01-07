# -*- coding: utf-8 -*-
import logging

from aiohttp import web

from .base import PytubeMixin
from pytube.requests import create_get_content
from pytube.server.decorators import json_response
from pytube.server.decorators import timing
from pytube.youtube.video import video_parser


logger = logging.getLogger(__name__)


class VideoView(PytubeMixin, web.View):
    @json_response
    @timing
    async def get(self):
        url = self.request.query.get('url')
        if not url:
            raise web.HTTPBadRequest
        async with create_get_content(**self.opts) as get_content:
            config, fmts = await video_parser(get_content, url)
            return {
                'url': url,
                'player': config,
                'formats': fmts,
            }
