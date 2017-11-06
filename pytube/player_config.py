# -*- coding: utf-8 -*-
import aiohttp

from . import parser
from . import requests


NULL = object()


class player_config:
    def __init__(self, url, with_formats=True, proxy=None, proxy_auth=None,
                 cache_ttl=NULL, cache_backend=None, cache_endpoint=None,
                 cache_port=None, cache_db=None, cache_password=None,
                 **kwargs):
        self.url = url
        self.with_formats = with_formats

        if cache_ttl is NULL:
            cache_ttl = 60 * 60
        elif cache_ttl:
            cache_ttl = int(cache_ttl)

        self.middlewares = (
            requests.user_agent_middleware(),
            requests.request_defaults_middleware(proxy=proxy,
                                                 proxy_auth=proxy_auth),
            requests.cached_request_middleware(cache_ttl=cache_ttl,
                                               cache_backend=cache_backend,
                                               cache_endpoint=cache_endpoint,
                                               cache_port=cache_port,
                                               cache_db=cache_db,
                                               cache_password=cache_password),
        )

    async def __aenter__(self):
        async with aiohttp.ClientSession() as client:
            get_content = requests. \
                get_content_factory(client, middlewares=self.middlewares)
            return await parser.\
                player_config_parser(get_content, self.url,
                                     with_formats=self.with_formats)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
