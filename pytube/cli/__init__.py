# -*- coding: utf-8 -*-
"""
Usage:
  pytube [--proxy=<proxy>] [--proxy-auth=<username:password>]
         [--cache-backend=<backend>] [--cache-endpoint=<endpoint>]
         [--cache-port=<port>] [--cache-database=<database>]
         [--cache-password=<password>]
         [--cache-ttl=<ttl>]
         [-v|-vv|-vvv]
         <command> [<args>...]
  pytube -h

Options:
  -h --help
  -v|-vv|-vvv
  --proxy=<proxy>
  --proxy-auth=<username:password>
  --cache-backend=<backend>
  --cache-endpoint=<endpoint>
  --cache-port=<port>
  --cache-database=<database>
  --cache-password=<password>

Commands:
{}

"""
import asyncio
from logging import basicConfig
from logging import DEBUG
from logging import INFO
from logging import WARNING

from docopt import docopt

from . import commands  # noqa
from .decorators import commands_register


def run_command(command_name, command, *args, **opts):
    argv = (command_name, ) + args
    arguments = docopt(
        command.__doc__.format(command=command_name),
        argv=argv,
    )

    result = command(arguments, **opts)
    if not asyncio.iscoroutine(result):
        return

    loop = asyncio.get_event_loop()
    loop.run_until_complete(result)


def collect_opts(arguments):
    opts = dict(
        cache_backend=arguments.get('--cache-backend'),
        cache_endpoint=arguments.get('--cache-endpoint'),
        cache_port=arguments.get('--cache-port'),
        cache_database=arguments.get('--cache-database'),
        cache_password=arguments.get('--cache-password'),
        proxy=arguments.get('--proxy'),
        proxy_auth=arguments.get('--proxy-auth'),
    )
    ttl = arguments.get('--cache-ttl')
    if ttl is not None:
        opts['cache_ttl'] = ttl
    return opts


def main():
    commands_list = '\n'.join(commands_register.keys())
    arguments = docopt(__doc__.format(commands_list), options_first=True)

    command_name = arguments.pop('<command>')
    assert command_name in commands_register, 'Unknown command'
    command = commands_register[command_name]

    verbosity = arguments.get('-v')
    if verbosity:
        level = {
            1: WARNING,
            2: INFO,
            3: DEBUG,
        }[verbosity]
        basicConfig(level=level)

    args = arguments.pop('<args>')
    opts = collect_opts(arguments)
    run_command(command_name, command, *args, **opts)


if __name__ == '__main__':
    main()
