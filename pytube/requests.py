# -*- coding: utf-8 -*-
from aiohttp import BasicAuth

try:
    from pytube.cache import cached, create_cache
    cache_exists = True
except ImportError:
    cache_exists = False


UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
     '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'


def get_content_factory(client, successful_statuses=(200, ), middlewares=None):
    async def get_content(**kwargs):
        async with client.request(**kwargs) as response:
            status = response.status
            content = None
            if status in successful_statuses:
                content = await response.text()
            return status, content
    for middleware in middlewares or ():
        get_content = middleware(get_content)
    return get_content


def request_defaults_middleware(**defaults):
    def outer(get_content):
        async def wrapper(**kwargs):
            _merge_defaults(kwargs, defaults)
            return await get_content(**kwargs)
        return wrapper
    return outer


def user_agent_middleware(user_agent=None):
    return request_defaults_middleware(headers={
        'User-Agent': user_agent or UA
    })


def request_proxy_middleware(proxy=None, proxy_auth=None):
    proxy_auth = _prepare_proxy_auth(proxy_auth)
    return request_defaults_middleware(proxy=proxy, proxy_auth=proxy_auth)


def cached_request_middleware(cache_ttl=None, cache_backend=None,
                              cache_endpoint=None, cache_port=None,
                              cache_db=None, cache_password=None):
    assert cache_exists, 'Install `aiocache`'

    def outer(get_content):
        cache = create_cache(cache_backend=cache_backend,
                             cache_endpoint=cache_endpoint,
                             cache_port=cache_port,
                             cache_db=cache_db,
                             cache_password=cache_password)
        return cached(cache, ttl=int(cache_ttl))(get_content)

    return outer


def _merge_defaults(dest, src):
    for k, v in src.items():
        if isinstance(v, dict):
            dest.setdefault(k, {})
            _merge_defaults(dest[k], v)
            continue
        dest.setdefault(k, v)


def _prepare_proxy_auth(proxy_auth):
    if not proxy_auth:
        return
    return BasicAuth(*proxy_auth.split(':', 1))
