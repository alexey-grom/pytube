# -*- coding: utf-8 -*-
import json as _json
from functools import partial
from json import JSONEncoder

# try:
#     import ujson as _json
# except ImportError:
#     import json as _json

from pytube.youtube.video.streams import Stream


class _Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Stream):
            return {**o.raw_data, **o.overrides}
        return super().default(o)


dump = partial(_json.dump, cls=_Encoder)
dumps = partial(_json.dumps, cls=_Encoder)
loads = _json.loads


# dump = _json.dump
# dumps = _json.dumps


def indent_dumps(*args, **kwargs):
    kwargs.setdefault('indent', 1)
    return dumps(*args, **kwargs)
