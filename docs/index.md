# pynd - search within Python code

You say it like find, but with a p. pind.

## Installation

We recommend installation with pip.

```text
$ pip install pynd
$ pynd -h
```

!!! warning

    pynd is in very early stages of development. Almost anything could change
    without warning. You have been warned ;-)

### Platform support

We recommend Python 3.4 or above. pynd was written for Python 3 and backported
to Python 2.7. It is supported and tested under Linux and OSX. Python 2 and
Windows support are done on a "best effort" basis.

## What & Why?

Pynd is a bit like grep, but it understand Python syntax. This means you can
do things like search within docstrings only or list and search function names.


## Usage Examples

### Search everything

By default, pynd will accept a pattern and use that to check against all the
AST nodes that it understands. This means, you can easily search across 
functions, class, docstrings and calls.

```text
$ pynd call --ignore-case
./pynd/filters.py
124:class CallFilter(NodeTypeFilter):
165:        CallFilter('C', 'call', (ast.Call, ),

./pynd/pattern.py
27:    def __call__(self, value):

./pynd/_tests/test_main.py
22:    mocked_search.assert_called_once_with(cli.parse_args(['.']))
```

In the above example we search for the pattern "call" everywhere in a 
case-insensitive search.

### Listing and searching within Python

List all the Python classes in every Python file under the current working
directory.

```text
$ pynd --class
./pynd/astutils.py
22:class ASTWalker(object):

./pynd/filters.py
20:class NodeTypeFilter(object):
85:class DocString(NodeTypeFilter):
109:class NameFilter(NodeTypeFilter):
```

Find all classes that match a pattern.

```text
$ pynd AST --class
./pynd/astutils.py
22:class ASTWalker(object):
```

The `--class` argument can be replaced or used in combination with other node
types. For example, find all functions or classes that contain the word `test`.

```text
$ pynd filter --class --def --ignore-case
./pynd/filters.py
20:class NodeTypeFilter(object):
109:class NameFilter(NodeTypeFilter):
121:def get_all_filters():
136:def get_active_filters(args):
```

### Finding the definition and usage

Finding where a function is defined can be useful, but we also want to know
where it is used.

```text
$ pynd get_all_filters --def --call
./pynd/cli.py
50:    for f in filters.get_all_filters():

./pynd/filters.py
153:def get_all_filters():
172:    return [f for f in get_all_filters() if f.is_activated(args)]

./pynd/search.py
55:        activated_filters = filters.get_all_filters()

```

Note, this uses a simple name match - so if you have multiple functions with
the same name, it will find them all.


### Docstrings

Searching within docstrings is simple with pynd. It works in a similar way
as the other node matches, but it will output the full docstring and the 
class or function that it is attached to.

```text
$ pynd TODO --doc
./pynd/filters.py
103:    def get_source(self, path, node):
Get the source line for a particular node.

TODO: Strippng the last line here is a hack - how should we do it
properly?
```

The above search will find all docstrings that contain TODO. If no term is 
provided, then all docstrings will be displayed.

### Public & Private

The flags `--private` and `--public` can be used to filter by the common Python
convention of a leading underscore to mark someting as private. This means
that `--private` will only match results starting with a underscore and 
`--public` will only match results starting without. These can be used in 
combination with other searched but can't both be used together.

```text
pynd --private --def
./pynd/astutils.py
34:    def _is_python(self, path):
38:    def _is_ignored(self, directory):
44:    def _walk_files(self, path):
66:    def _read(self, file_path):

./pynd/filters.py
101:    def _get_docstring(self, node):
```

### Supported Node Types

pynd currently supports the following node types.

* `--doc` - matches within docstrings
* `--class` - Matches classes.
* `--def` - All function definitions.
* `--import` - Matches import statements
* `--call` - Matches calls to functions or new classes
* `--attr` - Matches attributes on objects

### Show full usage

```text
usage: pynd [-h] [--version] [--ignore-dir [IGNORE_DIR [IGNORE_DIR ...]]]
            [--ignore-case] [--files-with-matches] [--show-stats]
            [--public | --private] [--verbose | --debug] [-d] [-c] [-f] [-i]
            [-C] [-a]
            [PATTERN] [FILES OR DIRECTORIES [FILES OR DIRECTORIES ...]]

Search for PATTERN in each Python file in filesystem from the current
directory down. If any files or directories are specified then only those are
checked.

positional arguments:
  PATTERN               The pattern to match against. This must be a valid
                        Python regular expression.
  FILES OR DIRECTORIES  A file or directory to limit the search scope. This
                        can be provided multiple times.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --ignore-dir [IGNORE_DIR [IGNORE_DIR ...]]
                        A pattern to exclude directories. This must be a valid
                        Python regular expression. It can be provided multiple
                        times.
  --ignore-case         Make all the regular expression matching case
                        insesitive.
  --files-with-matches  Don't output all the results, just the paths to files
                        that contain a result.
  --show-stats          At the end, show some stats.
  --public              Only show results considered to be public in Python.
                        They don't start with an underscore.
  --private             Only show results considered to be private in Python.
                        They start with an underscore.
  --verbose             Explain what is happening.
  --debug               Output excessively to make debugging easier
  -d, --doc             Match class and function docstrings.
  -c, --class           Match class names.
  -f, --def             Match function names.
  -i, --import          Match imported package names.
  -C, --call            Match call statements.
  -a, --attr            Match attributes on objects
```
