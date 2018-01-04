# -*- coding: utf-8 -*-

import re
from urllib.parse import urlencode

from pytube.exceptions import DownloadingError


re_keyword = re.compile('\["([^"]+)",')


async def search_keywords(get_content, query, lang=None):
    params = {
        'client': 'youtube',
        'q': query,
        'hl': lang or 'en_US',
    }
    url = 'https://clients1.google.com/complete/search?' + urlencode(params)
    status_code, content = await get_content(method='GET', url=url)
    if status_code != 200:
        raise DownloadingError(status_code, url, 'keywords')
    return tuple(set(re_keyword.findall(content)))
