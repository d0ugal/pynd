import ast
import io
import os
import os.path
import logging

LOG = logging.getLogger(__name__)


class ASTWalker(object):
    """
    Abstract Syntax Tree Walker

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
        """
        Walk through all the files and directories in alphabetical order for
        the given path and yield all paths to the Python files.
        """
        for root, dirs, filenames in os.walk(path):
            # Remove dot-directories from the dirs list.
            dirs[:] = sorted(d for d in dirs if not d.startswith('.')
                             and not self._is_ignored(d))
            for filename in sorted(filenames):
                if self._is_python(filename):
                    yield os.path.join(root, filename)

    def _read(self, file_path):
        LOG.debug("Reading file: %s", file_path)
        # TODO: Do we need to handle other file encodings?
        with io.open(file_path, "r", encoding="utf-8") as source_file:
            return source_file.read()

    def walk(self):
        for path in self.paths:
            LOG.info("Searching %s", path)
            for file_path in self._walk_files(path):
                try:
                    source = self._read(file_path)
                    yield file_path, ast.walk(ast.parse(source))
                except SyntaxError:
                    LOG.exception("Failed to parse {}. Could it be a "
                                  "incompatible Python version?")
                except UnicodeDecodeError:
                    LOG.exception("Failed to decode {}.")
