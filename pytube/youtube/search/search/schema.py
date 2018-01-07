# -*- coding: utf-8 -*-
from .filters import extract_canonical_url
from pytube.structure import filters
from pytube.structure import Schema as x


video_schema = x(
    ('videoRenderer', ),
    id='videoId',
    thumbnails=('thumbnail', 'thumbnails', ),
    title=('title', 'simpleText', ),
    description=x(
        filters.join('\n'),
        ('descriptionSnippet', 'runs', 'text',),
    ),
    published=('publishedTimeText', 'simpleText', ),
    length=('lengthText', 'simpleText', ),
    views_count=('viewCountText', 'simpleText', ),
    owner=x(
        ('ownerText', 'runs', ),
        text='text',
        id=('navigationEndpoint', 'browseEndpoint', 'browseId', ),
    ),
    channel_thumbnails=('channelThumbnail', 'thumbnails', ),
    richThumbnail=(
        'richThumbnail', 'movingThumbnailRenderer',
        'movingThumbnailDetails', 'thumbnails', ),
)

channel_schema = x(
    ('channelRenderer', ),
    id='channelId',
    canonical=x(
        extract_canonical_url,
        ('navigationEndpoint', 'browseEndpoint', 'canonicalBaseUrl'),
    ),
    title=('title', 'simpleText', ),
    thumbnails=('thumbnail', 'thumbnails', ),
    description=x(
        filters.join('\n'),
        ('descriptionSnippet', 'runs', 'text',),
    ),
    videos_count=x(
        filters.join('\n'),
        ('videoCountText', 'runs', 'text',),
    ),
    subscriber_count=x(
        filters.join('\n'),
        ('subscriberCountText', 'runs', 'text',),
    ),
)

playlist_schema = x(
    ('playlistRenderer', ),
    id='playlistId',
    title=('title', 'simpleText', ),
    videos_count=x(
        filters.type_cast(int),
        ('videoCount', ),
    ),
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
    continuations=(
        'continuations', 0, 'nextContinuationData',
        'continuation', ),
    items=x(
        filters.drop_empty_items,  #
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
    (
        'contents', 'twoColumnSearchResultsRenderer', 'primaryContents',
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
