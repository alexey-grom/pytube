# -*- coding: utf-8 -*-
from .flags import flag


def split_args(args, item_test):
    flags, args = _iter_args(args, lambda item, _: isinstance(item, flag))
    filters, args = _iter_args(args, lambda item, _: callable(item))
    path, args = _iter_args(args, lambda _, index: index == 0)
    nested, args = _iter_args(args, lambda item, _: item_test(item))

    assert len(args) <= 0, 'Path should be single'
    assert not args, 'Nested elements contain items with unacceptable types'

    return flags, filters, path[0] if path else None, nested


def _iter_args(args, test):
    count = 0
    for index, item in enumerate(args):
        if not test(item, index):
            break
        count += 1
    return args[:count], args[count:]


def not_empty(value):
    if value is None:
        return False
    if isinstance(value, (list, tuple, dict)):
        return len(value) > 0
    return True


def is_empty(value):
    return not not_empty(value)
