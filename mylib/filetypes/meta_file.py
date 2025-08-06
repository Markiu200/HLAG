from file import File

class MetaFile(File):
    def __init__(self, path: str):
        super().__init__(path)

    def to_string(self) -> str:
        """Reads first line and takes it as section title."""
        with open(self.path) as f:
            line = f.readline()
        return line
    
    def __str__(self):
        return self.to_string()