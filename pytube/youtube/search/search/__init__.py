# -*- coding: utf-8 -*-
import logging
from urllib.parse import quote
from urllib.parse import urlencode

from pytube.exceptions import DownloadingError
from pytube import json
from .meta import *
from .schema import get_response_schema


logger = logging.getLogger(__name__)


class search(object):
    def __init__(self, get_content, query, sorting=None, type=None, lang=None):
        self.get_content = get_content
        self.query = query
        self.lang = lang

        sorting = sorting or BY_RELEVANCE
        type = type or ALL
        assert sorting in ORDERS
        assert type in TYPES

        self.option = OPTION_VALUES[sorting][type]

        self.continuations = None
        self.xsrf_token = None

        self._has_more = None

    @property
    def has_more(self):
        return self._has_more or self._has_more is None

    async def next(self):
        if not self.has_more:
            return

        headers = {
            'X-YouTube-Client-Name': '1',
            'X-YouTube-Client-Version': '2.20171218',
        }

        params = {
            'search_query': quote(self.query),
            'hl': self.lang or 'en_US',
            'pbj': '1',
            'sp': self.option,
        }
        if self.xsrf_token:
            params['ctoken'] = self.continuations

        url = 'https://www.youtube.com/results?' + urlencode(params)
        method = 'GET' if self.continuations is None else 'POST'

        logger.info('Download search url {}'.format(url))

        status_code, content = \
            await self.get_content(method=method, url=url, headers=headers)

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
