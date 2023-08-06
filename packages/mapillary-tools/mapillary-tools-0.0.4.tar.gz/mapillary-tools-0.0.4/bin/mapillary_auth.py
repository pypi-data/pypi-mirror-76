#!/usr/bin/env python

'''Get Mapillary authentication tokens and store them.

Asks for your Mapillary password and retrieves authentication tokens
from the Mapillary API and stores them in the configuration file.

Mapillary authentication tokens do not expire so you need to run this
only once.

'''

import getpass
import logging

import mapillary_tools as mt


def build_parser ():
    ''' Build the commandline parser. '''

    parser = mt.build_parser (__doc__)

    parser.add_argument (
        '-u', '--user_name', required = True,
        help='your username on Mapillary'
    )
    parser.add_argument (
        '-e', '--user_email', required = True,
        help='your email on Mapillary'
    )

    return parser


if __name__ == '__main__':
    args = build_parser ().parse_args ()
    mt.init_logging (args.verbose)

    password = getpass.getpass ('Please enter your Mapillary user password : ')

    try:
        mt.write_config_file (mt.get_auth_tokens (args.user_name, args.user_email, password))

    except mt.MapillaryError as e:
        logging.exception (e)
