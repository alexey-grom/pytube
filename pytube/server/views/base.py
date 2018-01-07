# -*- coding: utf-8 -*-
import logging

from aiohttp.web_urldispatcher import AbstractView


logger = logging.getLogger(__name__)


class PytubeMixin(AbstractView):
    @property
    def context(self):
        return self.request['context']

    @property
    def opts(self):
        return self.context['opts']
