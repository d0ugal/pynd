import ast
import linecache
import logging

LOG = logging.getLogger(__name__)


class NodeTypeFilter(object):
    """
    AST Node Filter

    Match specific types of AST nodes.

    Given a short name, full name a tuple of nodes to match provide a way to
    filter the nodes in an AST.
    """

    def __init__(self, short, name, types):

        # TODO: I'm not sure that the short name belongs here, since it is only
        #       used for the CLI. Not sure where to move it?
        self.short = short
        self.name = name

        # TODO: We might want to handle lists or other iterables being passed
        #       in eventually? at the moment this will just wrap the iterable
        #       in a tuple.
        if not isinstance(types, tuple):
            types = (types, )

        self.types = types

    def arg_short(self):
        """Short name for the CLI. For example -c is short for --class."""
        return "-{}".format(self.short)

    def arg_name(self):
        """CLI arg name. for example --class is used for filtering by class"""
        return "--{}".format(self.name)

    def arg_dest(self):
        """
        Where to store the args.

        This is done to avoid name conflicts with python keywords.
        """
        return "{}_".format(self.name)

    def is_activated(self, args):
        """
        Is the filter in use?

        If a user provides `--class Foo` then the value will be "Foo" and it is
        in use, or if the user provides `--class` then the value will be True
        and also in use.
        """
        return getattr(args, self.arg_dest())

    def match(self, node, pattern):
        for type_ in self.types:
            if type_ != type(node):
                continue
            return self.cmp(node, pattern)
        return False

    def get_source(self, path, node):
        # TODO: Strippng the last line here is a hack - how should we do it
        # properly?
        return linecache.getline(path, node.lineno)[:-1]

    def cmp(self, node, patters):
        raise NotImplemented


class DocString(NodeTypeFilter):

    def __init__(self, *args, **kwargs):
        super(DocString, self).__init__(*args, **kwargs)

    def _get_docstring(self, node):
        return ast.get_docstring(node)

    def _include_all(self, node):
        return False

    def cmp(self, node, pattern):
        docstring = ast.get_docstring(node)
        if docstring is None:
            return False
        LOG.debug("Comparing %r and %r", docstring, pattern)
        return pattern(docstring)

    def get_source(self, path, node):
        # TODO: Strippng the last line here is a hack - how should we do it
        # properly?
        return linecache.getline(path, node.lineno) + self._get_docstring(node)


class NameFilter(NodeTypeFilter):

    def cmp(self, node, pattern):
        if hasattr(node, "name"):
            return pattern(node.name)
        if hasattr(node, "names"):
            for name in node.names:
                if pattern(name.name):
                    return True
        return False


def get_all_filters():
    """Return all the available filters"""
    return (
        DocString('d', 'doc', (ast.FunctionDef, ast.ClassDef, )),  # TODO: Add ast.Module
        NameFilter('c', 'class', (ast.ClassDef, )),
        NameFilter('f', 'def', (ast.FunctionDef, )),
        NameFilter('i', 'import', (ast.Import, ast.ImportFrom, )),
    )


def get_active_filters(args):
    """Return all the enabled filters"""
    return [f for f in get_all_filters() if f.is_activated(args)]
