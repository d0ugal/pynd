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

import pynd
from pynd import filters


def create_parser():
    parser = argparse.ArgumentParser(description=(
        """Search for PATTERN in each Python file in filesystem from the
        current directory down. If any files or directories are specified then
        only those are checked.
        """
    ))
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(pynd.__version__))
    parser.add_argument('pattern', metavar="PATTERN", default=".", nargs="?",
                        help=("The pattern to match against. This must be a "
                              "valid Python regular expression."))
    parser.add_argument('paths', metavar="FILES OR DIRECTORIES",
                        nargs='*', default=[".", ],
                        help=("A file or directory to limit the search scope. "
                              "This can be provided multiple times."))
    parser.add_argument('--ignore-dir', nargs="*", default=[],
                        help=("A pattern to exclude directories. This must be "
                              "a valid Python regular expression. It can be "
                              "provided multiple times."))
    parser.add_argument('--ignore-case', action="store_true",
                        help=("Make all the regular expression matching case "
                              "insesitive."))
    parser.add_argument('--files-with-matches', action="store_true",
                        help=("Don't output all the results, just the paths "
                              "to files that contain a result."))
    parser.add_argument('--show-stats', action="store_true",
                        help=("At the end, show some stats."))

    pub_mutex = parser.add_mutually_exclusive_group()
    pub_mutex.add_argument('--public', action="store_const",
                           const="^(?!_.*$).*$",
                           help=("Only show results considered to be public "
                                 "in Python. They don't start with an "
                                 "underscore."))
    pub_mutex.add_argument('--private', action="store_const",
                           const="^(?!__.*$)_.*$",
                           help=("Only show results considered to be private "
                                 "in Python. They start with an underscore."))

    log_mutex = parser.add_mutually_exclusive_group()
    log_mutex.add_argument('--verbose', action="store_true",
                           help="Explain what is happening.")
    log_mutex.add_argument('--debug', action="store_true",
                           help="Output excessively to make debugging easier")

    for f in filters.get_all_filters():
        name = f.arg_name()
        parser.add_argument(
            f.arg_short(), name, dest=f.arg_dest(), action="store_true",
            help=f.help)

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
