# -*- coding: utf-8 -*-
from . import filters  # noqa
from . import native
from .flags import DEBUG
from .flags import KEEP_EMPTY
from .flags import MULTIPLE
from .flags import STRICT
from .utils import is_empty
from .utils import split_args


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
        if is_empty(value):
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


class Schema(object):
    __slots__ = \
        'flags', \
        'filters', \
        'path', \
        'nested', \
        'named',

    item_class = Item
    non_inherited_flags = {DEBUG, MULTIPLE}

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

        if is_empty(data) and KEEP_EMPTY not in flags:
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
            result.append(item(data, flags - self.non_inherited_flags))
        if len(self.nested) == 1:
            result = result[0]
        return result

    def _apply_as_dict(self, data, flags):
        result = {}

        for item in self.nested:
            result.update(item(data, flags - self.non_inherited_flags))

        for name, item in self.named.items():
            if not self.item_test(item):
                item = self.item_class(item)
            result[name] = item(data, flags - self.non_inherited_flags)

        return result

    @classmethod
    def item_test(cls, item):
        return item and isinstance(item, (cls.item_class, cls))


class EtreeItem(Item):
    allowed_key_types = (str, )
    null_value = None

    def _extract(self, data, path, flags):
        multiple = MULTIPLE in flags
        result = data.xpath(path)
        if not result:
            return [] if multiple else None
        return result if multiple else result[0]

    @classmethod
    def check_path(cls, path):
        if isinstance(path, cls.allowed_key_types):
            return path
        raise RuntimeError('Bad path: {}'.format(path))


class EtreeSchema(Schema):
    item_class = EtreeItem
