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
import io
import logging
import os
import os.path

LOG = logging.getLogger(__name__)


class ASTWalker(object):
    """Abstract Syntax Tree Walker

    Given a set of paths on the file system create an interator that returns
    a tuple for each Python file containing the file path and an iterator
    for that files ast nodes.
    """

    def __init__(self, paths, ignore_dirs):
        self.paths = paths
        self.ignore_dirs = ignore_dirs

    def _is_python(self, path):
        # TODO: We might want to support other files here? i.e. shebang?
        return path.endswith(".py")

    def _is_ignored(self, directory):
        for ignore_pat in self.ignore_dirs:
            if ignore_pat(directory):
                return True
        return False

    def _walk_files(self, path):
        """Walk paths and yield Python paths

        Directories and files are yielded in alphabetical order. Directories
        starting with a "." are skipped. As are those that match any provided
        ignore patterns.
        """

        if os.path.isfile(path):
            yield path
        elif not os.path.isdir(path):
            LOG.error("The path '%s' can't be found.", path)
            raise StopIteration

        for root, dirs, filenames in os.walk(path):
            # Remove dot-directories from the dirs list.
            dirs[:] = sorted(d for d in dirs if not d.startswith('.') and
                             not self._is_ignored(d))
            for filename in sorted(filenames):
                if self._is_python(filename):
                    yield os.path.join(root, filename)

    def _read(self, file_path):
        LOG.debug("Reading file: %s", file_path)
        # TODO: Do we need to handle other file encodings?
        with io.open(file_path, "r", encoding="utf-8") as source_file:
            return source_file.read()

    def _walk_ast(self, node, top=False):
        if not hasattr(node, 'parent'):
            node.parent = None
            node.parents = []
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, ast.AST):
                        self._walk_ast(item)
                        self._set_parnt_fields(item, node, field, index)
            elif isinstance(value, ast.AST):
                self._walk_ast(value)
                self._set_parnt_fields(value, node, field)

        if top:
            return ast.walk(node)

    def _set_parnt_fields(self, node, parent, field, index=None):
        node.parent = parent
        node.parents.append(parent)
        node.parent_field = field
        node.parent_field_index = index

    def walk(self):
        for path in self.paths:
            LOG.info("Searching %s", path)
            for file_path in self._walk_files(path):
                try:
                    source = self._read(file_path)
                    yield file_path, self._walk_ast(ast.parse(source), top=True)
                except SyntaxError:
                    LOG.exception("Failed to parse %s. Could it be a "
                                  "incompatible Python version?", file_path)
                except UnicodeDecodeError:
                    LOG.exception("Failed to decode %s.")
