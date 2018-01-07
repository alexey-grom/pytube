# encoding: utf-8


def extract_canonical_url(value, *args):
    if not value:
        return
    try:
        _, type, value = value.split('/', 2)
        if type == 'user':
            return value
    except ValueError:
        return
