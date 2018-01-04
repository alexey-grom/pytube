# -*- coding: utf-8 -*-
import sys
from functools import wraps

from pytube.json import dump


commands_register = {}


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


def command(name=None):
    def wrapper(func):
        command_name = name or func.__name__.replace('_', '-')
        assert command_name not in commands_register
        commands_register[command_name] = func
        return func
    return wrapper
