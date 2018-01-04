# encoding: utf-8


NULL = object()


def _is_array(value):
    return value and isinstance(value, (list, tuple))


def _is_dict(value):
    return value and isinstance(value, dict)


def _has(value, key):
    if not value:
        return
    if _is_dict(value):
        return key in value
    if _is_array(value) and isinstance(key, int):
        return len(value) > key
    return


def _is_collection(value):
    return value and (_is_dict(value) or _is_array(value))


def _is_prime(value):
    return not _is_collection(value)


def walk(value, *keys, default=None):
    ref = value

    for index, key in enumerate(keys):
        if _is_prime(ref):
            ref = NULL
            break

        if _has(ref, key):
            ref = ref[key]
            continue

        if _is_array(ref) and keys[index:]:
            ref = [
                walk(item, *keys[index:], default=default)
                for item in ref
            ]
            break

        ref = NULL
        break

    return default if ref is NULL else ref
