import re


class IndentTracker:
    saved_indent = ""

    @classmethod
    def indent(cls, line: str) -> str:
        current_indent = re.match(r'\s*', line).group()
        lines = line.split("\n")
        result = "".join([IndentTracker.saved_indent, lines[0]])

        new_indent = ""
        for line in lines[1:]:
            new_indent = re.match(r'\s*', line).group()
            result = "".join([result, "\n", current_indent, line])

        IndentTracker.saved_indent = "".join([IndentTracker.saved_indent, new_indent])
        return result

    @classmethod
    def get_indent(cls):
        return IndentTracker.saved_indent
