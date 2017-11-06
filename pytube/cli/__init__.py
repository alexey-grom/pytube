# -*- coding: utf-8 -*-
"""
Usage:
  pytube [--proxy=<proxy>] [--proxy-auth=<username:password>]
         [--cache-backend=<backend>] [--cache-endpoint=<endpoint>]
         [--cache-port=<port>] [--cache-database=<database>]
         [--cache-password=<password>]
         [-v|-vv|-vvv]
         <command> [<args>...]
  pytube -h

Options:
  -h --help
  -v|-vv|-vvv
  --output=<filename>
  --proxy=<proxy>
  --proxy-auth=<username:password>
  --cache-backend=<backend>
  --cache-endpoint=<endpoint>
  --cache-port=<port>
  --cache-database=<database>
  --cache-password=<password>

Commands:
  list
  download
  dump-player-config
  dump-streams
  server

"""
import asyncio
from logging import basicConfig
from logging import DEBUG
from logging import INFO
from logging import WARNING

from docopt import docopt

from . import commands


def get_command_by_name(name):
    clean = name.replace('-', '_')
    names = [clean, '{}_command'.format(clean)]
    for clean in names:
        command = getattr(commands, clean, None)
        if command and getattr(command, 'is_command', None):
            command.name = name
            return command


def run_command(command, *args, **opts):
    argv = (command.name, ) + args
    arguments = docopt(command.__doc__, argv=argv)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(command(arguments, **opts))


def collect_opts(arguments):
    return dict(
        cache_backend=arguments.get('--cache-backend'),
        cache_endpoint=arguments.get('--cache-endpoint'),
        cache_port=arguments.get('--cache-port'),
        cache_database=arguments.get('--cache-database'),
        cache_password=arguments.get('--cache-password'),
        proxy=arguments.get('--proxy'),
        proxy_auth=arguments.get('--proxy-auth'),
        output=arguments.pop('--output', None),
    )


def main():
    arguments = docopt(__doc__, options_first=True)

    command = get_command_by_name(arguments.pop('<command>'))
    assert command, 'Unknown command'

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
    run_command(command, *args, **opts)


if __name__ == '__main__':
    main()
