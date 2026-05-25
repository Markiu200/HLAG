from pathlib import Path
from node import Node
from file import File


class CSSFile(File):
    def __init__(self, path: Path, parent: Node):
        super().__init__(path, parent)

    def get_css(self) -> str:
        """For CSS files, return whole file but encase it in &lt;style&gt; tags"""
        result = "<style>\n"
        with open(self.path) as f:
            for line in f:
                result += "  " + line
        result += "\n</style>\n"
        return result


if __name__ == "__main__":
    test_file = CSSFile(Path("D:\\hlag\\webpage\\020_ticket_tracker\\010_current_ticket.html"), Node(Path(".")))
    print(test_file)
