class HTMLFile:
    def __init__(self, path: str):
        self.path = path

    def to_string(self) -> str:
        """For HTML files, only return contents of &lt;body&gt; as is, but as &lt;article&gt."""
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
        result = f"<article>{result}</article>"
        return result