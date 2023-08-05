"""Edelweiss Data CLI

A CLI tool for EdelweissData: Convenient publishing of scientific data with proper versioning, rich metadata support and a powerful API.

Usage:
    edelweiss [--url=URL] <command> [<args>...]

Options:
  -h --help     Show this screen
  --url=URL     The base edelweiss api url [default: https://api.edelweissdata.com]

The most commonly used commands are:
    authentiate  Generate access and refresh tokens
"""
from docopt import docopt
from edelweiss_data import API
import json

def main():

    args = docopt(__doc__, version="0.1.0", options_first=True)
    command = args['<command>']
    argv = [command] + args['<args>']

    api = API(args['--url'])

    if command == 'authenticate':
        from . import auth
        return auth.run(api, argv)
    else:
        raise "unknown command {}".format(command)

if __name__ == "__main__":
    main()
