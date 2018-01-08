# -*- coding: utf-8 -*-
from pytube.exceptions import DownloadingError
from pytube.youtube.provisioner import youtube_provisioner
from pytube import json
from . import meta
from .schema import about_schema, generic_schema


async def _about_tab(data):
    return about_schema(data)


tabs = {
    meta.ABOUT: _about_tab,
}


async def parse_channel(get_content, id, types=None):
    get_content = youtube_provisioner(get_content)

    types = types or {meta.ABOUT}

    result = {}

    base_url = 'https://www.youtube.com/user/{}'.format(id)
    if id.startswith('UC'):
        base_url = 'https://www.youtube.com/channel/{}'.format(id)

    generic = None

    for type in types:
        url = '{}/{}'.format(base_url, type)
        status_code, content = \
            await get_content(method='GET', url=url)
        if status_code != 200:
            raise DownloadingError(status_code, url, 'channel/{}'.format(type))

        data = json.loads(content)
        assert len(data) == 2

        if generic is None:
            generic = generic_schema(data)

        extractor = tabs[type]
        result[type] = await extractor(data)

    result['generic'] = generic

    return result
