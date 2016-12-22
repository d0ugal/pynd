#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

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
