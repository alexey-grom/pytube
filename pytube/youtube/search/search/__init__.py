# -*- coding: utf-8 -*-
import logging
from urllib.parse import quote

from . import meta
from .schema import get_response_schema
from pytube import json
from pytube.youtube.provisioner import youtube_provisioner
from pytube.exceptions import DownloadingError


logger = logging.getLogger(__name__)


class search(object):
    def __init__(self, get_content, query, sorting=None, type=None, lang=None):
        self.get_content = youtube_provisioner(get_content, lang=lang)
        self.query = query
        self.lang = lang

        sorting = sorting or meta.BY_RELEVANCE
        type = type or meta.ALL
        assert sorting in meta.ORDERS
        assert type in meta.TYPES

        self.option = meta.OPTION_VALUES[sorting][type]

        self.continuations = None
        self.xsrf_token = None

        self._has_more = None

    @property
    def has_more(self):
        return self._has_more or self._has_more is None

    async def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.has_more:
            raise StopAsyncIteration

        params = {
            'search_query': quote(self.query),
            'sp': self.option,
            # 'hl': self.lang or 'en_US',
        }
        if self.xsrf_token:
            params['ctoken'] = self.continuations

        url = 'https://www.youtube.com/results'
        method = 'GET' if self.continuations is None else 'POST'

        logger.info('Download search url {}'.format(url))

        status_code, content = \
            await self.get_content(method=method, url=url, params=params)

        if status_code != 200:
            raise DownloadingError(status_code, url, 'search')

        data = json.loads(content)
        assert len(data) == 2

        schema = get_response_schema(not self.continuations)
        data = schema(data, dict(skip_empty=True))

        self.continuations = data['continuations']
        self.xsrf_token = data['xsrf_token']

        self._has_more = bool(self.continuations)

        items = data['items']

        return items
