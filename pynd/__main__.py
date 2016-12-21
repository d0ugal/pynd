import argparse
import logging
import sys

from . import search
from . import filters


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('--ignore-case', action="store_true")
    parser.add_argument('--files-with-matches', action="store_true")

    filter_args = parser.add_mutually_exclusive_group()
    for f in filters.get_all_filters():
        name = f.arg_name()
        filter_args.add_argument(
            f.arg_short(), name, dest=f.arg_dest(), nargs='?',
            metavar=f.name.upper(), const=True)

    return parser


def parse_args(args):
    parser = create_parser()
    args = parser.parse_args(args)
    return args


def setup_logging(args):

    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    else:
        level = logging.ERROR

    log = logging.getLogger('pynd')
    log.setLevel(level)
    stream = logging.StreamHandler()
    stream.setLevel(level)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    stream.setFormatter(formatter)
    log.addHandler(stream)
    return log


def main(args=None):
    args = parse_args(args or sys.argv[1:])
    setup_logging(args)

    LOG = logging.getLogger(__name__)
    LOG.debug("Started with args: %r", args)

    try:
        search.search(args)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    sys.exit(main())
