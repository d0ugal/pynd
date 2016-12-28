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

from pynd import astutils


def test_is_python():
    walker = astutils.ASTWalker([], [])
    assert walker._is_python("real_python.py")


def test_is_not_python():
    walker = astutils.ASTWalker([], [])
    assert not walker._is_python("fake_python.yp")


def test_walk_files_none(tmpdir):
    walker = astutils.ASTWalker([], [])
    assert list(walker._walk_files(tmpdir.dirname)) == []


def test_walk_files_one(tmpdir):
    tmpdir.join("test.py").write("")
    tmpdir.join("test.not-py").write("")

    walker = astutils.ASTWalker([], [])

    assert len(list(walker._walk_files(tmpdir.dirname))) == 1


def test_read(tmpdir):
    source = tmpdir.join("test.py")
    source.write("testing")

    walker = astutils.ASTWalker([], [])

    assert walker._read(str(source)) == "testing"


def test_walk(tmpdir):
    tmpdir = tmpdir.mkdir("sub")
    tmpdir.join("test.py").write("import os")
    tmpdir.join("test.not-py").write("")

    walker = astutils.ASTWalker([tmpdir.dirname, ], [])

    result = list(walker.walk())
    name, ast = result[0]
    assert len(result) == 1
    assert name.endswith("sub/test.py")
    assert list(ast), []  # TODO: Wat. How does this pass?


def test_walk_syntax_error(tmpdir):
    tmpdir = tmpdir.mkdir("sub")
    tmpdir.join("test.py").write("import import")

    walker = astutils.ASTWalker([tmpdir.dirname, ], [])

    result = list(walker.walk())
    assert len(result) == 0
