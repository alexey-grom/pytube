# -*- coding: utf-8 -*-
import os
import re
from collections import defaultdict
from collections import OrderedDict
from datetime import datetime


DEFAULT_FORMAT = 'pytube-%y%m%d-%H%M%S-{config[args][title]}.{stream.format}'

FS_NTFS_CHRS = [chr(i) for i in range(0, 31)]
FS_CHRS = [
    '\"', '\#', '\$', '\%', '\'', '\*', '\/', '\:',
    '\;', '\<', '\>', '\?', '\\', '\^', '\|', '\~', '\\\\',
    # '\,', '\.',
]
FS_FILTER_PATTERN = re.compile('|'.join(FS_NTFS_CHRS + FS_CHRS), re.UNICODE)


def cmp_predicate(key, pattern):
    def cmp(stream):
        value = getattr(stream, key, None)
        if not value:
            return
        return type(value)(pattern) == value
    return cmp


def choose_stream(streams, **filters):
    streams = sorted(streams, key=lambda stream: stream.sort_key)
    for key, value in filters.items():
        if not value:
            continue
        streams = filter(cmp_predicate(key, value), streams)
    streams = list(streams)
    if not streams:
        return
    return streams[-1]


def format_filename(config, stream, fmt=None):
    fmt = fmt or DEFAULT_FORMAT
    filename = fmt.format(config=config, stream=stream)
    filename = datetime.now().strftime(filename)
    return filename


def safe_filename(filename, max_length=255):
    """Sanitize a string making it safe to use as a filename.

    This function was based off the limitations outlined here:
    https://en.wikipedia.org/wiki/Filename.

    :param str s:
        A string to make safe for use as a file name.
    :param int max_length:
        The maximum filename character length.
    :rtype: str
    :returns:
        A sanitized string.
    """
    # Characters in range 0-31 (0x00-0x1F) are not allowed in ntfs filenames.
    filename = FS_FILTER_PATTERN.sub('', filename)
    return filename[:max_length].rsplit(' ', 0)[0]


def human_size(size):
    if not size:
        return None
    size = int(size)
    suffix = ''
    for suffix in ['', 'K', 'M', 'G', 'T']:
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
