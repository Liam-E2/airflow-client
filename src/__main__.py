import argparse
import sys
from traceback import format_exc
import logging

from .config import *

parser = argparse.ArgumentParser()
parser.set_defaults(cmd=lambda args: print("No arguments supplied; pass -h/--help for available arguments"))
subparsers = parser.add_subparsers()

configure = subparsers.add_parser("configure", help="Opens config file in default text editor")
configure.set_defaults(cmd=edit_config)

if __name__ == '__main__':
    args = parser.parse_args()
    try:
        args.cmd(args)
    except Exception as e:
        logging.error(format_exc())
        sys.exit(1)

    sys.exit(0)
