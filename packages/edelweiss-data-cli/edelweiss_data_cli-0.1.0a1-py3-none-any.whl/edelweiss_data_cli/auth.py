"""Usage: edelweiss authenticate [--refresh-token] [--token-dir=<dir>] [--scope=<scope>]...

Prints an access token for authenticating to the edelweiss API.

Options:
  -h --help          Show this screen
  --refresh-token    Print a refresh token instead of an access token
  --token-dir=<dir>  The directory in which to store refresh tokens
  --scope=<scope>    Any additional scopes to request from the authentication server

"""
from docopt import docopt

def run(api, argv):
    args = docopt(__doc__, argv=argv)

    api.authenticate(token_dir=args['--token-dir'], scopes=args['--scope'])

    if args['--refresh-token']:
        print(api.auth.refresh_token)
    else:
        print(api.auth.jwt)
