from .dn_data import Data


class Card:
    def __init__(self, module: str, data: Data):
        self.module = module
        self.data = data
