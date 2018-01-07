# -*- coding: utf-8 -*-
from pytube.structure import EtreeSchema as x
from pytube.structure import filters
from pytube.structure import flags


author_schema = x(
    './author',
    name='./name/text()',
    uri='./uri/text()',
)

feed_schema = x(
    '.',
    id='./channelId/text()',
    title='.//title/text()',
    link='.//link/@href',
    author=author_schema,
    published='./published/text()',
    entries=x(
        flags.MULTIPLE,
        './entry',
        x(
            './group',
            x(
                './community',
                rating=x(
                    './starRating',
                    count=x(filters.int_cast, './@count'),
                    average=x(filters.float_cast, './@average'),
                    min=x(filters.int_cast, './@min'),
                    max=x(filters.int_cast, './@max'),
                ),
                views_count=x(filters.int_cast, './statistics/@views'),
            ),
            description='./description/text()',
            thumbnail=x(
                './thumbnail',
                url='./@url',
                width=x(filters.int_cast, './@width'),
                height=x(filters.int_cast, './@height'),
            ),
        ),
        id='./videoId/text()',
        channel_id='./channelId/text()',
        title='./title/text()',
        author=author_schema,
        published='./published/text()',
        updated='./updated/text()',
    ),
)
