# -*- coding: utf-8 -*-
import logging
from urllib.parse import quote
from urllib.parse import urlencode

from pytube.exceptions import DownloadingError
from pytube import json
from pytube.structure import Schema as x
from pytube.structure import filters
from pytube.structure import flags


logger = logging.getLogger(__name__)

ALL = ''
VIDEOS = 'videos'
CHANNELS = 'channels'
PLAYLISTS = 'playlists'
MOVIES = 'movies'
SHOWS = 'shows'

TYPE_KEYS = {
    VIDEOS: 'EgIQAQ%3D%3D',
    CHANNELS: 'EgIQAg%3D%3D',
    PLAYLISTS: 'EgIQAw%3D%3D',
    MOVIES: 'EgIQBA%3D%3D',
    SHOWS: 'EgIQBQ%3D%3D',
}


class search(object):
    def __init__(self, get_content, query, lang=None):
        self.get_content = get_content
        self.query = query
        self.lang = lang

        self.continuations = None
        self.xsrf_token = None

        self._has_more = None

    @property
    def has_more(self):
        return self._has_more or self._has_more is None

    async def next(self):
        if not self.has_more:
            return

        headers = {
            'X-YouTube-Client-Name': '1',
            'X-YouTube-Client-Version': '2.20171218',
        }

        params = {
            'search_query': quote(self.query),
            'hl': self.lang or 'en_US',
            'pbj': '1',
            # 'spf': 'navigate',
        }
        if self.xsrf_token:
            params['ctoken'] = self.continuations

        url = 'https://www.youtube.com/results?' + urlencode(params)
        method = 'GET' if self.continuations is None else 'POST'

        logger.info('Download search url {}'.format(url))

        status_code, content = \
            await self.get_content(method=method, url=url, headers=headers)

        if status_code != 200:
            raise DownloadingError(status_code, url, 'search')

        data = json.loads(content)
        assert len(data) == 2

        schema = get_response_schema(not self.continuations)
        data = schema(data, dict(skip_empty=True))

        self.continuations = data['continuations']
        self.xsrf_token = data['xsrf_token']

        self._has_more = bool(self.continuations)

        items = data['items']

        # import pdb; pdb.set_trace()

        return items


video_schema = x(
    flags.SKIP_EMPTY,
    ('videoRenderer', ),
    id='videoId',
    thumbnails=('thumbnail', 'thumbnails', ),
    title=('title', 'simpleText', ),
    description=x(filters.join('\n'),
                  ('descriptionSnippet', 'runs', 'text',)),
    published=('publishedTimeText', 'simpleText', ),
    length=('lengthText', 'simpleText', ),
    views_count=('viewCountText', 'simpleText', ),
    owner=x(
        ('ownerText', 'runs', ),
        text='text',
        id=('navigationEndpoint', 'browseEndpoint', 'browseId', ),
    ),
    channel_thumbnails=('channelThumbnail', 'thumbnails', ),
    richThumbnail=('richThumbnail', 'movingThumbnailRenderer',
                   'movingThumbnailDetails', 'thumbnails', ),
)

channel_schema = x(
    flags.SKIP_EMPTY,
    ('channelRenderer', ),
    id='channelId',
    title=('title', 'simpleText', ),
    thumbnails=('thumbnail', 'thumbnails', ),
    description=x(filters.join('\n'),
                  ('descriptionSnippet', 'runs', 'text',)),
    videos_count=x(filters.join('\n'),
                   ('videoCountText', 'runs', 'text',)),
    subscriber_count=x(filters.join('\n'),
                       ('subscriberCountText', 'runs', 'text',)),
)

playlist_schema = x(
    flags.SKIP_EMPTY,
    ('playlistRenderer', ),
    id='playlistId',
    title=('title', 'simpleText', ),
    videos_count=x(filters.type_cast(int),
                   ('videoCount', )),
    videos=x(
        ('videos', 'childVideoRenderer', ),
        id='videoId',
        title=('title', 'simpleText', ),
        length=('lengthText', 'simpleText', ),
    ),
    owner=x(
        ('longBylineText', 'runs', ),
        id=('navigationEndpoint', 'browseEndpoint', 'browseId', ),
        title='text',
    ),
    thumbnails=('thumbnails', 'thumbnails', ),
)

contents_schema = x(
    continuations=('continuations', 0, 'nextContinuationData',
                   'continuation', ),
    items=x(
        # filters.drop_empty_items,
        ('contents', ),
        x(
            filters.drop_null_values,
            # lambda result, original: result if result else {'raw': original},
            video=video_schema,
            channel=channel_schema,
            playlist=playlist_schema,
        ),
    ),
)

first_page = x(
    ('contents', 'twoColumnSearchResultsRenderer', 'primaryContents',
     'sectionListRenderer', 'contents', 0, 'itemSectionRenderer', ),
    contents_schema,
)

another_page = x(
    ('continuationContents', 'itemSectionContinuation', ),
    contents_schema,
)


def get_response_schema(is_first_page):
    return x(
        (1, ),
        x(
            ('response', ),
            first_page if is_first_page else another_page,
            estimated_results=('estimatedResults', ),
        ),
        xsrf_token=('xsrf_token', ),
    )
