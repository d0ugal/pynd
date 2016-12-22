# pynd - search within Python code

You say it like find, but with a p. pind.

## Installation

We recommend installation with pip.

```
$ pip install pynd
$ pynd -h
```

!!! warning

    pynd is in very early stages of development. Almost anything could change
    without warning. You have been warned ;-)


## What & Why?

Pynd is a bit like grep, but it understand Python syntax. This means you can
do things like search within docstrings only or list and search function names.


## Usage Examples

### Listing and searching within Python

List all the Python classes in every Python file under the current working
directory.

```
$ pynd --class
```

Find all classes that match a pattern.

```
$ pynd MyClass --class
```

The `--class` argument can be replaced or used in combination with other node
types. For example, find all functions or classes that contain the word `test`.

```
$ pynd test --class --def --ignore-case
```

### Docstrings

Searching within docstrings is simple with pynd. It works in a similar way
as the other node matches, but it will output the full docstring and the 
class or function that it is attached to.

```
$ pynd TODO --doc
```

The above search will find all docstrings that contain TODO. If no term is 
provided, then all docstrings will be output.

### Supported Node Types

pynd currently supports the following node types.

* `--class` - Matches classes.
* `--def` - All function definitions.
* `--import` - matches import statements
* `--doc` - matches within docstrings

### Show full usage

```
usage: pynd [-h] [--ignore-dir [IGNORE_DIR [IGNORE_DIR ...]]] [--verbose]
            [--debug] [--ignore-case] [--files-with-matches] [-d] [-c] [-f]
            [-i]
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
  --ignore-dir [IGNORE_DIR [IGNORE_DIR ...]]
                        A pattern to exclude directories. This must be a valid
                        Python regular expression. It can be provided multiple
                        times.
  --verbose             Explain what is happening.
  --debug               Output excessively to make debugging easier
  --ignore-case         Make all the regular expression matching case
                        insesitive.
  --files-with-matches  Don't output all the results, just the paths to files
                        that contain a result.
  -d, --doc             Match class and function docstrings.
  -c, --class           Match class names.
  -f, --def             Match function names.
  -i, --import          Match imported package names.
```