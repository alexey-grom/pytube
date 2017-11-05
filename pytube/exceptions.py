# -*- coding: utf-8 -*-
"""Library specific exception definitions."""
import sys


class PytubeError(Exception):
    """Base pytube exception that all others inherent.

    This is done to not pollute the built-in exceptions, which *could* result
    in unintended errors being unexpectedly and incorrectly handled within
    implementers code.
    """


class ExtractError(PytubeError):
    """Data extraction based exception."""

    def __init__(self, msg, video_id=None):
        """Construct an instance of a :class:`ExtractError <ExtractError>`.

        :param str msg:
            User defined error message.
        :param str video_id:
            A YouTube video identifer.
        """
        if video_id is not None:
            msg = '{video_id}: {msg}'.format(video_id=video_id, msg=msg)

        super(ExtractError, self).__init__(msg)

        self.exc_info = sys.exc_info()
        self.video_id = video_id


class RegexMatchError(ExtractError):
    """Regex pattern did not return any matches."""


class AgeRestrictionError(ExtractError):
    """Content is age restricted."""


class DownloadingError(PytubeError):
    def __init__(self, status_code, url, content_type=None):
        self.status_code = status_code
        self.url = url
        self.content_type = content_type

        msg = 'Error occurred while downloading {}: ' \
              'status_code={}, url={}'.format(
                  content_type or 'unknown',
                  status_code, url,
              )

        super(DownloadingError, self).__init__(msg)
