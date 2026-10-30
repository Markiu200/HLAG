from abc import ABC, abstractmethod
# Own imports
if __name__ == '__main__':
    from sys import path as sys_path
    from pathlib import PurePath
    sys_path.append(str(PurePath(__file__).parent.parent))
from lib.base_check import BaseCheck


class IModule(ABC):
    def __init__(self):
        self.info = dict()
        self.checks: list[BaseCheck] = []
        self.gui_widget = None

    @abstractmethod
    def get_metadata(self, value, is_file: bool) -> dict:
        pass

    @abstractmethod
    def parse(self, value, metadata: dict, is_file: bool) -> str:
        pass

    @classmethod
    def json_sanitize(cls, line: str | None):
        if line is None:
            return 'null'
        result = line.replace("\\", "\\\\")
        result = result.replace("$", "\\$")
        result = result.replace("`", "\\`")
        return fr"`{result}`"
