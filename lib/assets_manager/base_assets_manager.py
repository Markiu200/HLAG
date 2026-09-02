from abc import ABC, abstractmethod
from pathlib import PurePath


class BaseAssetsManager(ABC):
    @abstractmethod
    def register_asset(self, path: PurePath):
        pass

    @abstractmethod
    def copy_assets(self):
        pass
