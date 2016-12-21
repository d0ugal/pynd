import mock

from .. import __main__
from .. import cli


def test_main():
    with mock.patch("pynd.search.search") as mocked_search:
        __main__.main(['.'])
    mocked_search.assert_called_once_with(cli.parse_args(['.']))


def test_main_no_args():
    """Should display the help only and exist. Not starting a search."""
    with mock.patch("pynd.search.search") as mocked_search:
        __main__.main([])
    assert mocked_search.call_count == 0


def test_main_interrupt():
    with mock.patch("pynd.search.search", side_effect=KeyboardInterrupt()):
        __main__.main(['.'])
