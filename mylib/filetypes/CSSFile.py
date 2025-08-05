from File import File

class CSSFile(File):
    def __init__(self, path: str):
        super().__init__(path)

    def to_string(self) -> str:
        """For CSS files, return whole file but encase it in &lt;style&gt; tags"""
        result = "<style>\r\n"
        with open(self.path) as f:
            for line in f:
                result += line
        result += "</style>\r\n"
        return result
    
    def __str__(self):
        return self.to_string()

if __name__ == "__main__":
    test_file = CSSFile("D:\\hlag\\webpage\\020_ticket_tracker\\010_current_ticket.html")
    print(test_file)
    