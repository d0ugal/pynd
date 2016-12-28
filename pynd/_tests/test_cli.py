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

import pytest

import logging

from pynd import cli


def test_parse_args_empty():
    args = cli.parse_args([])
    assert args.pattern == "."
    assert args.paths == ['.']
    assert not args.doc_
    assert not args.class_
    assert not args.def_
    assert not args.import_


def test_parse_args_class_only():
    args = cli.parse_args(["--class"])
    assert not args.doc_
    assert args.class_
    assert not args.def_
    assert not args.import_


def test_logger():
    args = cli.parse_args([".", ])
    log = cli.setup_logging(args)
    assert log.level == logging.ERROR


def test_logger_verbose():
    args = cli.parse_args([".", "--verbose"])
    log = cli.setup_logging(args)
    assert log.level == logging.INFO
    assert args.verbose
    assert not args.debug


def test_logger_debug():
    args = cli.parse_args([".", "--debug"])
    log = cli.setup_logging(args)
    assert log.level == logging.DEBUG
    assert not args.verbose
    assert args.debug


def test_debug_and_verbose():
    with pytest.raises(SystemExit):
        cli.parse_args([".", "--debug", "--verbose"])
