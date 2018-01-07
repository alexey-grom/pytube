# -*- coding: utf-8 -*-
from urllib.parse import urlencode

from lxml.etree import fromstring

from .schema import feed_schema
from pytube.exceptions import DownloadingError
from pytube.utils import remove_namespaces


async def parse_feed(get_content, id):
    key = 'user'
    if id.startswith('PL'):
        key = 'playlist_id'
    elif id.startswith('UC'):
        key = 'channel_id'

    params = {
        key: id,
    }
    url = 'https://www.youtube.com/feeds/videos.xml?' + urlencode(params)

    status_code, content = await get_content(method='GET', url=url)
    if status_code != 200:
        raise DownloadingError(status_code, url, 'feed')

    tree = fromstring(content.encode())
    remove_namespaces(tree)
    return feed_schema(tree)
