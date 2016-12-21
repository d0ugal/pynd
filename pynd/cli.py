import argparse
import logging

from . import filters


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', metavar="PATTERN", default=".", nargs="?")
    parser.add_argument('paths', metavar="FILES OR DIRECTORIES",
                        nargs='*', default=[".", ])
    parser.add_argument('--ignore-dir', nargs="*", default=[])
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('--ignore-case', action="store_true")
    parser.add_argument('--files-with-matches', action="store_true")

    for f in filters.get_all_filters():
        name = f.arg_name()
        parser.add_argument(
            f.arg_short(), name, dest=f.arg_dest(), action="store_true")

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
