import ast
import os
import os.path

class ASTWalker():

    def __init__(self, paths):
        self.paths = paths

    def _is_python(self, path):
        # TODO: We might want to support other files here? i.e. shebang?
        return path.endswith(".py")

    def _walk(self, path):
        for root, dirs, filenamess in os.walk(path):
            for filename in filenamess:
                if self._is_python(filename):
                    full = os.path.join(root, filename)
                    abs = os.path.abspath(full)
                    yield abs

    def _read(self, file_path):
        # TODO: Do we need to handle other file encodings?
        with open(file_path, "r", encoding="utf-8") as source_file:
            return source_file.read()

    def walk(self):
        for path in self.paths:
            for file_path in self._walk(path):
                source = self._read(file_path)
                yield file_path, ast.parse(source)

def search(paths):
    for file_path, x in ASTWalker(paths).walk():
        print(file_path)
        print(dir(x))
        print(x.body)
        break
