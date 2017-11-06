# -*- coding: utf-8 -*-
import sys
from functools import wraps
try:
    from ujson import dump
except ImportError:
    from json import dump


def redirect_output(func):
    @wraps(func)
    async def wrapper(arguments, **kwargs):
        output = arguments.pop('--output', None)
        if not output:
            output = sys.stdout
        else:
            output = open(output, 'w')
        try:
            dump(await func(arguments, **kwargs), output)
        finally:
            output.close()
    return wrapper


def command(func):
    func.is_command = True
    return func
