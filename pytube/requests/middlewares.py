# -*- coding: utf-8 -*-

try:
    from pytube.cache import cached, create_cache
    cache_exists = True
except ImportError:
    cache_exists = False

from .utils import merge_defaults


UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
     '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'


def request_defaults_middleware(**defaults):
    def outer(get_content):
        async def wrapper(**kwargs):
            merge_defaults(kwargs, defaults)
            return await get_content(**kwargs)
        return wrapper
    return outer


def user_agent_middleware(user_agent=None):
    return request_defaults_middleware(headers={
        'User-Agent': user_agent or UA
    })


def cached_request_middleware(cache_ttl=None, cache_backend=None,
                              cache_endpoint=None, cache_port=None,
                              cache_database=None, cache_password=None):
    assert cache_exists, 'Install `aiocache`'

    def outer(get_content):
        cache = create_cache(cache_backend=cache_backend,
                             cache_endpoint=cache_endpoint,
                             cache_port=cache_port,
                             cache_database=cache_database,
                             cache_password=cache_password)
        return cached(cache, ttl=int(cache_ttl))(get_content)

    return outer
