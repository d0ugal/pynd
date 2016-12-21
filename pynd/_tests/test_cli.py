import logging

from .. import cli


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
