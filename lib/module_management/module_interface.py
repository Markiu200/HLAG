from abc import ABC, abstractmethod
from structure_scanner.document_tree import DocumentNode
from models import Data, InstanceDBEntry


class IModule(ABC):
    @classmethod
    @abstractmethod
    def get_info(cls) -> dict:
        """
        :return: Dictionary of module info, including data such as priority or
        dependencies.
        """
        pass

    @classmethod
    @abstractmethod
    def register_checks(cls):
        """This is what should be done before StructureScanner starts it's scan.
        Not every module should implement this (just have 'pass' in body). Only
        these that actually introduce some new extension to the game.
        """
        pass

    @classmethod
    @abstractmethod
    def register_files(cls):
        """This is where we register our JS and CSS for final product. This method
        will be invoked only if ContentManager finds that the module was indeed used.
        Every module should probably register at least a .js file.
        """
        pass

    @classmethod
    @abstractmethod
    def get_metadata_from_file(cls, node: DocumentNode) -> dict:
        """
        :param node: DocumentNode of the file in question - it gets it's path from there,
        but it should't be used to actually modify the metadata.
        :return: dict of metadata it found and some information about the read itself
        """
        pass

    @classmethod
    @abstractmethod
    def get_metadata_from_data(cls, data: Data) -> dict:
        """
        This will be most likely used when dealing with references.
        :param data: Data structure to read metadata from - Data.content for reading, and Data.meta for passing current metadata.
        but it should't be used to actually modify the metadata.
        :return: dict of metadata it found and some information about the read itself
        """
        pass

    @classmethod
    @abstractmethod
    def parse_file(cls, node: DocumentNode) -> InstanceDBEntry:
        """This method is what produces our final dict() of information to be used
        by ContentManager to craft the JSREF. All the references there might have been
        should have been replaced before.
        'from_file' version is most likely to be used during initial node handling.
        """

    @classmethod
    @abstractmethod
    def parse_data(cls, data: Data) -> InstanceDBEntry:
        """This method is what produces our final dict() of information to be used
        by ContentManager to craft the JSREF. All the references there might have been
        should have been replaced before.
        'from_string' version is most likely to be used when dealing with references."""
