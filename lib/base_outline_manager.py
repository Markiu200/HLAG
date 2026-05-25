from abc import ABC, abstractmethod


class BaseOutlineManager(ABC):
    @abstractmethod
    def register(self, path, filename):
        """Register a file or directory that needs to be in final product.

        Positional arguments:
        path -- relative path to the file starting w/o filename, starting from root directory
        filename -- filename w/o path
        """
