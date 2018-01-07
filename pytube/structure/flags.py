# -*- coding: utf-8 -*-


class flag:
    __slots__ = 'name',

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Flag[{}]'.format(self.name)
    __repr__ = __str__


DEBUG = flag('debug')
STRICT = flag('strict')
# SKIP_EMPTY = flag('skip empty')
KEEP_EMPTY = flag('keep empty')
