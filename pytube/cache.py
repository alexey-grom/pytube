# -*- coding: utf-8 -*-
import functools
from functools import lru_cache

from aiocache import cached as _cached
from aiocache import caches
from aiocache.base import BaseCache


CACHE_BACKEND_BY_ALIAS = {
    'dummy': 'pytube.cache.DummyCache',
    'memory': 'aiocache.SimpleMemoryCache',
    'memcached': 'aiocache.MemcachedCache',
    'redis': 'aiocache.RedisCache',
}


@lru_cache(None)
def create_cache(cache_backend=None, cache_endpoint=None, cache_port=None,
                 cache_database=None, cache_password=None):
    opts = {
        'cache': CACHE_BACKEND_BY_ALIAS[cache_backend or 'dummy'],
        'endpoint': cache_endpoint,
        'port': cache_port,
        'db': cache_database,
        'password': cache_password,
    }
    opts = {
        k: v
        for k, v in opts.items()
        if v
    }
    return caches.create(**opts)


class DummyCache(BaseCache):
    async def _add(self, key, value, ttl, _conn=None):
        return

    async def _get(self, key, encoding, _conn=None):
        return

    async def _multi_get(self, keys, encoding, _conn=None):
        return

    async def _set(self, key, value, ttl, _cas_token=None, _conn=None):
        return

    async def _multi_set(self, pairs, ttl, _conn=None):
        return

    async def _delete(self, key, _conn=None):
        return

    async def _exists(self, key, _conn=None):
        return

    async def _increment(self, key, delta, _conn=None):
        return

    async def _expire(self, key, ttl, _conn=None):
        return

    async def _clear(self, namespace, _conn=None):
        return

    async def _raw(self, command, *args, **kwargs):
        return

    async def _close(self, *args, **kwargs):
        pass


class cached(_cached):
    def __init__(self, cache, ttl=None):
        super(cached, self).__init__(ttl=ttl)
        self.cache = cache

    def __call__(self, f):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            return await self.decorator(f, *args, **kwargs)
        return wrapper
