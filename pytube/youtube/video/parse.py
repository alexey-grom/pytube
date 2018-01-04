# -*- coding: utf-8 -*-
import json
import logging
from urllib.parse import parse_qsl

try:
    import aiohttp
    aiohttp_exists = True
except ImportError:
    aiohttp_exists = False

from pytube.youtube.video import mixins, extract, streams
from pytube.exceptions import AgeRestrictionError, DownloadingError
from pytube.youtube.video.helpers import apply_mixin
from pytube.requests import get_content_factory


logger = logging.getLogger(__name__)


async def get_player_config(video_url, with_formats=True):
    assert aiohttp_exists, 'Install `aiohttp`'

    async with aiohttp.ClientSession() as client:
        get_content = get_content_factory(client)
        return await video_parser(get_content, video_url, with_formats)


async def video_parser(get_content, video_url, with_formats=True):
    # video_id part of /watch?v=<video_id>
    video_id = extract.video_id(video_url)

    # https://www.youtube.com/watch?v=<video_id>
    watch_url = extract.watch_url(video_id)

    logger.info('Download watch url {}'.format(video_url))
    status_code, watch_html = \
        await get_content(method='GET', url=watch_url)
    if status_code != 200:
        raise DownloadingError(status_code, watch_url, 'js')

    if extract.is_age_restricted(watch_html):
        raise AgeRestrictionError('Content is age restricted')

    logger.info('Extract player config')
    player_config = extract.get_ytplayer_config(watch_html)

    logger.info('Extract player args')
    formats = None

    if with_formats:
        logger.info('Extract js url')
        js_url = extract.js_url(watch_html)

        logger.info('Extract vid info url')
        vid_info_url = extract.video_info_url(video_id=video_id,
                                              watch_url=watch_url,
                                              watch_html=watch_html)

        formats = await player_formats_parser(get_content, js_url,
                                              vid_info_url, player_config)

    return player_config, formats


async def player_formats_parser(get_content, js_url, vid_info_url,
                                player_config):
    config_args = player_config['args']

    logger.info('Download js {}'.format(js_url))
    status_code, js = await get_content(method='GET', url=js_url)
    if status_code != 200:
        raise DownloadingError(status_code, js_url, 'js')

    logger.info('Download vid info {}'.format(vid_info_url))
    status_code, vid_info = \
        await get_content(method='GET', url=vid_info_url)
    if status_code != 200:
        raise DownloadingError(status_code, vid_info_url, 'vid info')

    vid_info = {k: v for k, v in parse_qsl(vid_info)}

    # https://github.com/nficano/pytube/issues/165
    stream_maps = ['url_encoded_fmt_stream_map']
    if 'adaptive_fmts' in config_args:
        stream_maps.append('adaptive_fmts')

    fmt_streams = []

    # unscramble the progressive and adaptive stream manifests.
    for fmt in stream_maps:
        mixins.apply_descrambler(vid_info, fmt)
        mixins.apply_descrambler(config_args, fmt)

        # apply the signature to the download url.
        mixins.apply_signature(config_args, fmt, js)

        # build instances of :class:`Stream <Stream>`
        stream_manifest = config_args[fmt]
        for stream in stream_manifest:
            video = streams.Stream(raw=stream)
            fmt_streams.append(video)

    # load the player_response object (contains subtitle information)
    apply_mixin(config_args, 'player_response', json.loads)

    return fmt_streams
