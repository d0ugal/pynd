from . import astutils
from . import filters

CLEAR = "\x1b[0m"
GREEN = "\x1b[1;32m"
YELLOW = "\x1b[1;33m"


def _print(colour, text):
    print("{}{}{}".format(colour, text, CLEAR))


def display_result(filter_, file_path, node):
    source = filter_.get_source(file_path, node)
    print("{}{}{}:{}".format(YELLOW, node.lineno, CLEAR, source))


def print_file_path(file_path, first):
    if not first:
        print()
    _print(GREEN, file_path)


def search(args):

    ast_walker = astutils.ASTWalker(args.files)
    files_with_matches = set()
    activated_filters = filters.get_active_filters(args)

    for i, (file_path, nodes) in enumerate(ast_walker.walk()):

        for node in nodes:

            for f in activated_filters:
                if f.match(node, args):

                    if file_path not in files_with_matches:
                        files_with_matches.add(file_path)
                        first = len(files_with_matches) == 1
                        print_file_path(file_path, first=first)

                    display_result(f, file_path, node)
