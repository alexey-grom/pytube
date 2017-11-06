# -*- coding: utf-8 -*-
import logging

from pytube.parser import extract
from pytube.parser.itags import get_format_profile
from pytube.utils import human_size

logger = logging.getLogger(__name__)


class RawProperty:
    def __init__(self, name, default=None, convert=None):
        self.name = name
        self.default = default
        self.convert = convert

    def __get__(self, instance, owner):
        if self.name in instance.overrides:
            return instance.overrides[self.name]

        value = instance.raw_data.get(self.name, self.default)
        if self.convert:
            value = self.convert(value)
        return value

    def __set__(self, instance, value):
        instance.overrides[self.name] = value


class Stream:
    def __init__(self, raw):
        self._raw = raw
        self._overrides = {}

        # Additional information about the stream format, such as resolution,
        # frame rate, and whether the stream is live (HLS) or 3D.
        self._overrides.update(get_format_profile(self.itag))
        # self.fmt_profile = get_format_profile(self.itag)

        self.mime_type, self.codecs = extract.mime_type_codec(self.type)
        self.type, self.format = self.mime_type.split('/', 1)

        # ['vp8', 'vorbis'] -> video_codec: vp8, audio_codec: vorbis. DASH
        # streams return NoneType for audio/video depending.
        self.video_codec, self.audio_codec = self.parse_codecs()

    url = RawProperty('url')

    itag = RawProperty('itag')
    type = RawProperty('type', '')
    bitrate = RawProperty('bitrate')
    clen = RawProperty('clen', 0, int)
    hclen = RawProperty('clen', 0, lambda value: human_size(value) or '?')

    resolution = RawProperty('resolution', None)
    abr = RawProperty('abr', None)
    is_live = RawProperty('is_live', None)
    is_3d = RawProperty('is_3d', None)
    fps = RawProperty('fps', None)
    size = RawProperty('size')
    quality = RawProperty('quality')
    quality_label = RawProperty('quality_label')

    index = RawProperty('index')
    init = RawProperty('init')
    lmt = RawProperty('lmt')
    projection_type = RawProperty('projection_type')

    @property
    def is_adaptive(self):
        """Whether the stream is DASH."""
        # if codecs has two elements (e.g.: ['vp8', 'vorbis']): 2 % 2 = 0
        # if codecs has one element (e.g.: ['vp8']) 1 % 2 = 1
        return len(self.codecs) % 2

    @property
    def is_progressive(self):
        return not self.is_adaptive

    @property
    def includes_audio_track(self):
        if self.is_progressive:
            return True
        return self.type == 'audio'

    @property
    def includes_video_track(self):
        if self.is_progressive:
            return True
        return self.type == 'video'

    def parse_codecs(self):
        """Get the video/audio codecs from list of codecs.

        Parse a variable length sized list of codecs and returns a
        consitant two element tuple, with the video codec as the first element
        and audio as the second. Returns None if one is not available
        (adaptive only).

        :rtype: tuple
        :returns:
            A two element tuple with audio and video codecs.

        """
        video = None
        audio = None
        if not self.is_adaptive:
            video, audio = self.codecs
        elif self.includes_video_track:
            video = self.codecs[0]
        elif self.includes_audio_track:
            audio = self.codecs[0]
        return video, audio

    @property
    def raw_data(self):
        return self._raw

    @property
    def overrides(self):
        return self._overrides

    @property
    def sort_key(self):
        return self.type, self.clen
