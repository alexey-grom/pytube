# -*- coding: utf-8 -*-
"""Various helper functions implemented by pytube."""
import logging
import pprint
import re

from pytube.exceptions import RegexMatchError


logger = logging.getLogger(__name__)


def regex_search(pattern, string, groups=False, group=None, flags=0):
    """Shortcut method to search a string for a given pattern.

    :param str pattern:
        A regular expression pattern.
    :param str string:
        A target string to search.
    :param bool groups:
        Should the return value be ``.groups()``.
    :param int group:
        Index of group to return.
    :param int flags:
        Expression behavior modifiers.
    :rtype:
        str or tuple
    :returns:
        Substring pattern matches.
    """
    regex = re.compile(pattern, flags)
    results = regex.search(string)
    if not results:
        raise RegexMatchError(
            'regex pattern ({pattern}) had zero matches'
            .format(pattern=pattern),
        )
    else:
        logger.debug(
            'finished regex search: %s',
            pprint.pformat(
                {
                    'pattern': pattern,
                    'results': results.group(0),
                }, indent=2,
            ),
        )
        if groups:
            return results.groups()
        elif group is not None:
            return results.group(group)
        else:
            return results


def apply_mixin(dct, key, func, *args, **kwargs):
    r"""Apply in-place data mutation to a dictionary.

    :param dict dct:
        Dictionary to apply mixin function to.
    :param str key:
        Key within dictionary to apply mixin function to.
    :param callable func:
        Transform function to apply to ``dct[key]``.
    :param \*args:
        (optional) positional arguments that ``func`` takes.
    :param \*\*kwargs:
        (optional) keyword arguments that ``func`` takes.
    :rtype:
        None
    """
    dct[key] = func(dct[key], *args, **kwargs)
