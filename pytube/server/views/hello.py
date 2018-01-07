# -*- coding: utf-8 -*-
import logging
from time import time

from aiohttp import web

from .base import PytubeMixin
from pytube.server.decorators import json_response
from pytube.server.decorators import timing


logger = logging.getLogger(__name__)


class HelloView(PytubeMixin, web.View):
    @json_response
    @timing
    async def get(self):
        return {
            'context': self.context,
            'uptime': time() - self.context['started'],
        }
