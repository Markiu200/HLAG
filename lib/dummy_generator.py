from base_generator import BaseGenerator


class DummyGenerator(BaseGenerator):
    def generate(self) -> str:
        return "Dummy generator invoked. You have either generated root node or did not assign generator to a directory of a file."
