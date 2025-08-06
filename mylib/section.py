from filetypes.file import File

class Section:
    def __init__(self, webpage_files: list[File], id: str):
        self.webpage_files = webpage_files
        self.id = id
        self.parent = None
        self.children = None
    
    def create_section(self) -> str:
        result = f"<section id=\"{self.id}\">"
        for file in self.webpage_files:
            result += file.to_string()
        result += "</section>"
        return result