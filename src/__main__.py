import argparse
import sys
from traceback import format_exc
import logging

from .config import *

parser = argparse.ArgumentParser()
parser.set_defaults(
    cmd=lambda args: print("No arguments supplied; pass -h/--help for available arguments"),
    conf=get_config()
    )
subparsers = parser.add_subparsers()

configure = subparsers.add_parser("configure", help="Opens config file in default text editor")
configure.set_defaults(cmd=edit_config)

list_objects = subparsers.add_parser("list", help="List objects; supported object types:")
list_objects.add_argument("-d", "--dag", help="List DAGs", action="store_true")
list_objects.add_argument("-f", "--filter", help="Regex pattern to match on dag_id")


if __name__ == '__main__':
    args = parser.parse_args()
    try:
        args.cmd(args)
    except Exception as e:
        logging.error(format_exc())
        sys.exit(1)

    sys.exit(0)
