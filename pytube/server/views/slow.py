# -*- coding: utf-8 -*-
import asyncio
import logging

from aiohttp import web

from pytube.server.decorators import json_response, timing
from .base import PytubeMixin


logger = logging.getLogger(__name__)


class SlowView(PytubeMixin, web.View):
    @json_response
    @timing
    async def get(self):
        timeout = 1.0
        try:
            timeout = float(self.request.query.get('timeout'))
        except (TypeError, ValueError):
            pass
        await asyncio.sleep(timeout)
        return 'ok'
