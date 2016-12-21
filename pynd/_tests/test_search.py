import mock

from .. import cli
from .. import search


def test_search(tmpdir):

    tmpdir = tmpdir.mkdir("sub")
    tmpdir.join("test.py").write("class MyClass1: pass\nclass MyClass2: pass")
    tmpdir.join("test.not-py").write("")

    args = cli.parse_args(['.', tmpdir.dirname, '--class'])

    with mock.patch("pynd.search.display_result") as display_result:
        search.search(args)

    assert display_result.call_count == 2
