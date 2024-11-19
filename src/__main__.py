import sys
from traceback import format_exc
import logging

from .cli import parse_args

# The ugliest airflow client you ever did see

if __name__ == '__main__':
    args = parse_args()
    try:
        args.cmd(args)
    except Exception as e:
        logging.error(format_exc())
        sys.exit(1)

    sys.exit(0)
