class Card:
    def __init__(self, node, file: bool, meta: dict | None, content, extensions=None):
        self.node = node
        self.file = file
        self.meta = meta
        self.content = content
        self.extensions = extensions
