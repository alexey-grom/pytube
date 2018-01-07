# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import aiosocks
from aiohttp import BasicAuth
from aiosocks.connector import ProxyClientRequest
from aiosocks.connector import ProxyConnector


def create_proxy_auth(proxy, proxy_auth):
    if not proxy_auth:
        return

    parsed = urlparse(proxy)

    if parsed.scheme == 'socks4':
        return aiosocks.Socks4Auth(*proxy_auth.split(':'))

    elif parsed.scheme == 'socks5':
        return aiosocks.Socks5Auth(*proxy_auth.split(':'))

    return BasicAuth(*proxy_auth.split(':', 1))


def create_connector(proxy=None):
    if not proxy:
        return
    return dict(
        connector=ProxyConnector(remote_resolve=True),
        request_class=ProxyClientRequest,
    )


def merge_defaults(dest, src):
    for k, v in src.items():
        if isinstance(v, dict):
            dest.setdefault(k, {})
            merge_defaults(dest[k], v)
            continue
        dest.setdefault(k, v)
