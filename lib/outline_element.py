from pathlib import PurePath
# Own imports
from base_generator import BaseGenerator


class OutlineElement:
    def __init__(self, rel_path: PurePath, abs_path: PurePath, filename: str):
        self.rel_path = rel_path
        self.abs_path = abs_path
        self.filename = filename
        self.dom_id = None
        self.generator: BaseGenerator | None = None
        #
        self.create_dom_id()

    def create_dom_id(self):
        self.dom_id = ".".join([*self.rel_path.parts, self.filename])

    def set_generator(self, generator: BaseGenerator):
        self.generator = generator
