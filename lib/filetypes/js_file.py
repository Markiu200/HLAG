if __name__ == "__main__":
    import os
    from sys import path as syspath
    from pathlib import Path

    while "mylib" in os.getcwd():
        os.chdir("..")
    syspath.append(str(Path('lib/').absolute()))
from pathlib import Path
from file import File
from node import Node


class JSFile(File):
    def __init__(self, path: Path, parent: Node):
        super().__init__(path, parent)

    def to_string(self) -> str:
        """For JS files, only return contents file as is, but wraps it in &lt;script&gt; tag."""
        result = "<script>\n"
        with open(self.path) as f:
            for line in f:
                result += "  "+line
        result += "\n</script>"
        return result
