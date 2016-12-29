import ast
import os.path

import pytest

from pynd import astutils
from pynd import filters
from pynd import pattern

@pytest.fixture
def ast_test_code():
    source_path = os.path.join(os.path.dirname(__file__), "test_code.txt")
    with open(source_path) as f:
        source = f.read()

    walker = astutils.ASTWalker([], [])
    return walker._walk_ast(ast.parse(source), top=True)

@pytest.fixture
def all_filters():
    return {f.name: f for f in filters.get_all_filters()}

def test_docstring(all_filters, ast_test_code):

    f = all_filters['doc']
    patterns = [pattern.compile('docstring'), ]

    for node in ast_test_code:
        if isinstance(node, ast.Module):
            assert f.match(node, patterns)
        else:
            assert not f.match(node, patterns)

def test_docstring_no_match(all_filters, ast_test_code):

    f = all_filters['doc']
    patterns = [pattern.compile('nomatches'), ]

    for node in ast_test_code:
        assert not f.match(node, patterns)

def test_import(all_filters, ast_test_code):

    f = all_filters['import']
    patterns = [pattern.compile('mything'), ]

    count = 0
    for node in ast_test_code:
        if f.match(node, patterns):
            count += 1
            assert isinstance(node, (ast.Import, ast.ImportFrom))

    assert count == 2

def test_import_no_match(all_filters, ast_test_code):

    f = all_filters['import']
    patterns = [pattern.compile('notimported'), ]

    for node in ast_test_code:
        assert not f.match(node, patterns)

def test_call(all_filters, ast_test_code):

    f = all_filters['call']
    patterns = [pattern.compile('juice'), ]
    count = 0

    for node in ast_test_code:
        if f.match(node, patterns):
            assert isinstance(node, (ast.Call))
            count += 1

    assert count == 1


def test_call_no_match(all_filters, ast_test_code):

    f = all_filters['call']
    patterns = [pattern.compile('sauce'), ]

    for node in ast_test_code:
        assert not f.match(node, patterns)
