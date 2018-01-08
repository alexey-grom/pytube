# encoding: utf-8
from urllib.parse import urlencode


def youtube_provisioner(get_content, lang=None):
    async def wrapper(**kwargs):
        url = kwargs.pop('url')
        params = {
            'pbj': '1',
        }
        params.update(kwargs.pop('params', None) or {})
        if params:
            # todo: currently it's presume that url has no query
            url = '{}?{}'.format(url, urlencode(params))
        headers = {
            'X-YouTube-Client-Name': '1',
            'X-YouTube-Client-Version': '2.20171218',
            'Accept-Language': lang or 'en_US',
        }
        headers.update(kwargs.pop('headers', None) or {})
        return await get_content(url=url, headers=headers, **kwargs)
    return wrapper
