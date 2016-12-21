import logging

import mock

from .. import __main__


def test_parse_args_empty():
    args = __main__.parse_args([".", "--class"])
    assert not args.doc_
    assert args.class_
    assert not args.def_
    assert not args.import_


def test_logger():
    args = __main__.parse_args([".", ])
    log = __main__.setup_logging(args)
    assert log.level == logging.ERROR


def test_logger_verbose():
    args = __main__.parse_args([".", "--verbose"])
    log = __main__.setup_logging(args)
    assert log.level == logging.INFO


def test_logger_debug():
    args = __main__.parse_args([".", "--debug"])
    log = __main__.setup_logging(args)
    assert log.level == logging.DEBUG


def test_main():
    with mock.patch("pynd.search.search") as mocked_search:
        __main__.main(['.'])
    mocked_search.assert_called_once_with(__main__.parse_args(['.']))


def test_main_interrupt():
    with mock.patch("pynd.search.search", side_effect=KeyboardInterrupt()):
        __main__.main(['.'])
