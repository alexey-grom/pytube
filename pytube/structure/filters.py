# -*- coding: utf-8 -*-


def join(separator):
    def inner(data, *args):
        return separator.join(data or [])
    return inner


def default(value):
    def inner(data, *args):
        return data or value
    return inner


def type_cast(target, strict=False):
    def inner(data, *args):
        if data is None:
            return None
        try:
            return target(data)
        except (ValueError, TypeError):
            if not strict:
                return None
            raise
    return inner


int_cast = type_cast(int)
float_cast = type_cast(float)


def drop_null_values(item, *args):
    if not isinstance(item, dict):
        return item
    return {
        k: v
        for k, v in item.items()
        if v is not None
    }


def drop_empty_items(items, *args):
    if not isinstance(items, (tuple, list)):
        return items
    return [
        item
        for item in items
        if item
    ]
