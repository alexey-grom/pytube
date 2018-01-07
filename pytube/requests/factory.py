# -*- coding: utf-8 -*-
import aiohttp

from . import middlewares as mwares
from . import utils


NULL = object()


def get_content_factory(client, successful_statuses=(200, ), middlewares=None):
    async def get_content(**kwargs):
        async with client.request(**kwargs) as response:
            status = response.status
            content = None
            if status in successful_statuses:
                content = await response.text()
            return status, content
    for middleware in middlewares or ():
        if not middleware:
            continue
        get_content = middleware(get_content)
    return get_content


class create_get_content:
    default_ttl = 60 * 60

    def __init__(self, proxy=None, proxy_auth=None,
                 cache_ttl=NULL, cache_backend=None, cache_endpoint=None,
                 cache_port=None, cache_database=None, cache_password=None,
                 **kwargs):
        if cache_ttl is NULL:
            cache_ttl = self.default_ttl
        elif cache_ttl:
            cache_ttl = int(cache_ttl)

        self.kwargs = utils.create_connector(proxy) or {}
        self.kwargs.update(kwargs)

        if not proxy:
            proxy = None
        self.proxy_auth = utils.create_proxy_auth(proxy, proxy_auth)

        self.middlewares = [
            mwares.user_agent_middleware(),
            mwares.request_defaults_middleware(proxy=proxy,
                                               proxy_auth=proxy_auth),
        ]
        if cache_ttl:
            cache = mwares.cached_request_middleware(
                cache_ttl=cache_ttl,
                cache_backend=cache_backend,
                cache_endpoint=cache_endpoint,
                cache_port=cache_port,
                cache_database=cache_database,
                cache_password=cache_password
            )
            self.middlewares.append(cache)

        self._client = None

    async def __aenter__(self):
        self._client = aiohttp.ClientSession(**self.kwargs)
        return get_content_factory(self._client, middlewares=self.middlewares)
        # TODO: fixit
        # async with aiohttp.ClientSession() as client:
        #     get_content = \
        #         get_content_factory(client, middlewares=self.middlewares)
        #     return get_content

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.close()
        self._client = None
