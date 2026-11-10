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
        self.gui_widget = None

    def pm_init(self):
        """This method will be invoked by PMModule manager after scan through all other modules is completed. It may remain empty,
        but it is intended to contain all registrations of prints, checks and so on. While it may be done in __init__, this allows
        module a chance to see complete module list in the manager, and allows module to finish its initialization."""
        return None

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
