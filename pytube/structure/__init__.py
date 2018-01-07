# encoding: utf-8

from logging import getLogger

from .utils import split_args
from .flags import DEBUG, STRICT, SKIP_EMPTY
from . import native
from . import filters


logger = getLogger('structure')


class Item(object):
    __slots__ = 'path',

    null_value = native.NULL
    allowed_key_types = (int, str, )

    def __init__(self, path):
        self.path = self.check_path(path)

    def __call__(self, data, flags=()):
        return self.apply(data, self.path, flags)

    def apply(self, data, path, flags=()):
        value = self._extract(data, path, flags)
        return self._check_strict(value, STRICT in flags)

    def _extract(self, data, path, flags):
        return native.walk(data, *path, default=self.null_value)

    def _check_strict(self, value, is_strict):
        if not value:
            return value
        if isinstance(value, (list, tuple)):
            return [
                self._check_strict(item, is_strict)
                for item in value
            ]
        if value is self.null_value:
            if is_strict:
                raise KeyError
            return
        return value

    @classmethod
    def check_path(cls, path):
        if isinstance(path, cls.allowed_key_types):
            return (path, )

        if isinstance(path, (list, tuple)):
            valid = all([
                isinstance(part, cls.allowed_key_types)
                for part in path
            ])
            if valid:
                return path
        raise RuntimeError('Bad path: {}'.format(path))

    def __str__(self):
        return 'Item<{}>'.format(str(self.path))
    __repr__ = __str__


class Schema(object):
    __slots__ = \
        'flags', \
        'filters', \
        'path', \
        'nested', \
        'named',

    item_class = Item

    def __init__(self, *nested, **named):
        self.flags, self.filters, self.path, self.nested = \
            split_args(nested, self.item_test)
        self.named = named

    def __call__(self, data, flags=()):
        pass_flags = set(flags) | set(self.flags)
        if self.path:
            data = self.item_class(self.path)(data, pass_flags)
        result = self.apply(data, pass_flags)
        for func in self.filters:
            result = func(result, data)
        return result

    def apply(self, data, flags=()):
        flags = set(flags) | set(self.flags)

        if not data and SKIP_EMPTY in flags:
            return data

        if isinstance(data, (list, tuple)):
            return [
                self.apply(item, flags)
                for item in data
            ]

        if not self.nested and not self.named:
            result = data

        elif self.nested and not self.named:
            result = self._apply_as_array(data, flags)

        else:
            result = self._apply_as_dict(data, flags)

        return result

    def _apply_as_array(self, data, flags):
        result = []
        for item in self.nested:
            result.append(item(data, flags - {DEBUG}))
        if len(self.nested) == 1:
            result = result[0]
        return result

    def _apply_as_dict(self, data, flags):
        result = {}

        for item in self.nested:
            result.update(item(data, flags - {DEBUG}))

        for name, item in self.named.items():
            if not self.item_test(item):
                item = self.item_class(item)
            result[name] = item(data, flags - {DEBUG})

        return result

    @classmethod
    def item_test(cls, item):
        return item and isinstance(item, (cls.item_class, cls))
