from pathlib import Path
from file import File
from node import Node

class HTMLFile(File):
    def __init__(self, path: Path, parent: Node):
        super().__init__(path, parent)

    def to_string(self) -> str:
        """For HTML files, only return contents of &lt;body&gt; as is, but as &lt;section&gt."""
        result = ""
        save_flag = False
        with open(self.path) as f:
            for line in f:
                if "<body>" in line:
                    save_flag = True
                    continue
                if "</body>" in line:
                    break
                if save_flag:
                    result += line
        result = f"<section>{result}</section>"
        return result
    
    def __str__(self):
        return self.to_string()