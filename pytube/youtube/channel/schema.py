# -*- coding: utf-8 -*-
from pytube.structure import Schema as x
from pytube.structure import filters
from pytube.structure import flags


about_schema = x(
    (1, 'response', 'contents', 'twoColumnBrowseResultsRenderer', ),
    x(
        filters.drop_empty_items,
        filters.pop_first,
        ('tabs', ),
        x(
            ('tabRenderer', 'content', 'sectionListRenderer', 'contents', 0,
             'itemSectionRenderer', 'contents', 0,
             'channelAboutFullMetadataRenderer', ),
            title=('title', 'simpleText', ),
            description=('description', 'simpleText', ),
            joined_date=x(
                filters.join(' '),
                ('joinedDateText', 'runs', 'text', ),
            ),
            subscribers_count=x(
                filters.join(' '),
                ('subscriberCountText', 'runs', 'text', ),
            ),
            views_count=x(
                filters.join(' '),
                ('viewCountText', 'runs', 'text', ),
            ),
        ),
    ),
    related_channels=x(
        ('secondaryContents', 'browseSecondaryContentsRenderer',
         'contents', 'verticalChannelSectionRenderer', ),
        title='title',
        items=x(
            ('items', ),
            x(
                'miniChannelRenderer',
                channel_id='channelId',
                title=x(
                    filters.join(' '),
                    ('title', 'runs', 'text', ),
                ),
                videos_count=x(
                    filters.join(' '),
                    ('videoCountText', 'runs', 'text', ),
                ),
                subscribers_count=('subscriberCountText', 'simpleText', ),
                thumbnails=('thumbnail', 'thumbnails', )
            ),
        ),
    ),
)

generic_schema = x(
    filters.merge_dicts,
    (1, 'response', ),
    x(
        ('microformat', 'microformatDataRenderer', ),
        # title='title',
        # description='description',  # it's trimmed
        tags='tags',
        thumbnails=('thumbnail', 'thumbnails', )
    ),
    x(
        ('metadata', 'channelMetadataRenderer', ),
        # available_countries='availableCountryCodes',
        title='title',
        description='description',
        # owner_urls='ownerUrls',
        external_id='externalId',
        rss_url='rssUrl',
        avatar=('avatar', 'thumbnails', ),
        is_family_safe='isFamilySafe',
        is_paid_channel='isPaidChannel',
    ),
)
