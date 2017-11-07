# -*- coding: utf-8 -*-
import asyncio
import logging
from time import time

from aiohttp import web
from aiohttp.web_urldispatcher import AbstractView

from pytube.parser.player_config import player_config
from pytube.server.decorators import json_reponse


logger = logging.getLogger(__name__)


class PytubeMixin(AbstractView):
    @property
    def context(self):
        return self.request['context']


class HelloView(PytubeMixin, web.View):
    @json_reponse
    async def get(self):
        return {
            'context': self.context,
            'uptime': time() - self.context['started'],
        }


class SlowView(PytubeMixin, web.View):
    @json_reponse
    async def get(self):
        timeout = 1.0
        try:
            timeout = float(self.request.query.get('timeout'))
        except (TypeError, ValueError):
            pass
        await asyncio.sleep(timeout)
        return 'ok'


class ExtractView(PytubeMixin, web.View):
    @json_reponse
    async def get(self):
        url = self.request.query.get('url')
        async with player_config(url, **self.context) as (config, fmts):
            return {
                'url': url,
                'player': config,
                'formats': fmts,
            }
