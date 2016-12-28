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

import ast
import linecache
import logging

LOG = logging.getLogger(__name__)


class NodeTypeFilter(object):
    """AST Node Filter

    Match specific types of AST nodes.

    Given a short name, full name a tuple of nodes to match provide a way to
    filter the nodes in an AST.
    """

    def __init__(self, short, name, types, help):

        # TODO: I'm not sure that the short name belongs here, since it is only
        #       used for the CLI. Not sure where to move it?
        self.short = short
        self.name = name
        self.help = help

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
        """Where to store the args.

        This is done to avoid name conflicts with python keywords.
        """
        return "{}_".format(self.name)

    def is_activated(self, args):
        """Is the filter in use?

        If a user provides `--class Foo` then the value will be "Foo" and it is
        in use, or if the user provides `--class` then the value will be True
        and also in use.
        """
        return getattr(args, self.arg_dest())

    def match(self, node, patterns):

        if type(node) not in self.types:
            return

        result = False

        for pattern in patterns:
            LOG.debug("Testing pattern %r", pattern)
            result = self.cmp(node, pattern)
            # We want to make sure each pattern is True, but exit early if one
            # is False to be more efficient.
            if not result:
                LOG.debug("Failed to match pattern %r", pattern)
                break

        return result

    def get_source(self, path, node):
        # TODO: Strippng the last line here is a hack - how should we do it
        # properly?
        return linecache.getline(path, node.lineno)[:-1]

    def cmp(self, node, pattern):
        raise NotImplemented


class DocString(NodeTypeFilter):

    def __init__(self, *args, **kwargs):
        super(DocString, self).__init__(*args, **kwargs)

    def _get_docstring(self, node):
        return ast.get_docstring(node)

    def cmp(self, node, pattern):
        docstring = ast.get_docstring(node)
        if docstring is None:
            return False
        LOG.debug("Comparing %r and %r", docstring, pattern.pattern)
        return pattern(docstring)

    def get_source(self, path, node):
        """Get the source line for a particular node.

        TODO: Strippng the last line here is a hack - how should we do it
        properly?
        """
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


class CallFilter(NodeTypeFilter):

    def cmp(self, node, pattern):
        # TODO: The logic in here is nasty. Is there a better way we can more
        # genertically match rather than handling specific cases?

        if isinstance(node.func, ast.Name):
            # This seems to be when we create instances of classes that are
            # in the local file.
            return pattern(node.func.id)

        if hasattr(node.func, 'attr') and pattern(node.func.attr):
            return True

        if (hasattr(node.func, 'value') and hasattr(node.func.value, 's') and
           pattern(node.func.value.s)):
            # This seems to be when we are calling methods on strings - not
            # sure if it could be anything else.
            return True

        # TODO: Support callables in more situations. For example, chained
        # calls mean node.func.func is a thing.

        LOG.debug("Failed to recognise call structure to test the pattern. "
                  "Node %s on line %s", node, node.lineno)

        return False


class AttrFilter(NodeTypeFilter):
    def cmp(self, node, pattern):
        return pattern(node.attr)


class ImportFilter(NodeTypeFilter):
    def cmp(self, node, pattern):

        for name in node.names:
            if pattern(name.name):
                return True

        if isinstance(node, ast.ImportFrom):
            if node.module and pattern(node.module):
                return True
        elif not isinstance(node, ast.Import):
            LOG.warning("Unknown import node")

        return False


def get_all_filters():
    """Return all the available filters"""
    return (
        # TODO: Add ast.Module to the docstring search.
        DocString('d', 'doc', (ast.FunctionDef, ast.ClassDef, ),
                  help="Match class and function docstrings."),
        NameFilter('c', 'class', (ast.ClassDef, ),
                  help="Match class names."),
        NameFilter('f', 'def', (ast.FunctionDef, ),
                  help="Match function names."),
        ImportFilter('i', 'import', (ast.Import, ast.ImportFrom, ),
                     help="Match imported package names."),
        CallFilter('C', 'call', (ast.Call, ),
                  help="Match call statements."),
        AttrFilter('a', 'attr', (ast.Attribute, ),
                  help="Match attributes on objects"),
    )


def get_active_filters(args):
    """Return all the enabled filters"""
    return [f for f in get_all_filters() if f.is_activated(args)]
