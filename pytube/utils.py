# -*- coding: utf-8 -*-
import os
from collections import defaultdict
from collections import OrderedDict


def human_size(size):
    if not size:
        return None
    size = int(size)
    for suffix in ['b', 'K', 'M', 'G', 'T']:
        if size < 1024:
            break
        size, _ = divmod(size, 1024)
    return '{}{}b'.format(size, suffix)


def get_maximal_width():
    _, columns = os.popen('stty size', 'r').read().split()
    return int(columns)


def format_column(prop, value, width=None):
    if not value:
        result = ''
    else:
        result = '{}={}'.format(prop, value)
    return result + (' ' * max([0,  (width or 0) - len(result)]))


def get_printable_columns(streams, prefix, spacing, all_columns):
    max_width = get_maximal_width()

    widths = defaultdict(int)

    for prop in all_columns:
        widths[prop] = max([
            len(format_column(prop, getattr(stream, prop)))
            for stream in streams
        ])

    widths = {
        column: width
        for column, width in widths.items()
        if width
    }

    columns_count = 0
    accum = len(prefix)
    for index, (prop, width) in enumerate(widths.items()):
        accum += (spacing if (index and width) else 0) + width
        if accum > max_width:
            break
        columns_count += 1

    return OrderedDict([
        (column, widths.get(column, 0))
        for column in all_columns[:columns_count]
    ])


def print_streams(streams, prefix=None, spacing=2):
    prefix = prefix or ''

    columns = get_printable_columns(
        streams, prefix, spacing, [
            'itag',
            'type',
            'format',
            'hclen',
            'format',
            'video_codec',
            'audio_codec',
            'resolution',
            'bitrate',
            'is_live',
            'is_3d',
            'abr',
            'quality',
            'quality_label',
            'size',
            'fps',
        ],
    )

    for stream in streams:
        print(prefix + (' ' * spacing).join([
            format_column(column, getattr(stream, column), width)
            for column, width in columns.items()
        ]))
