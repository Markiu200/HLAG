from abc import ABC, abstractmethod
from models import Card, InstanceDBEntry


class IModule(ABC):
    @classmethod
    def get_metadata(cls, card: Card) -> dict:
        if card.file:
            return cls.get_metadata_from_file(card)
        else:
            return cls.get_metadata_from_data(card)

    @classmethod
    def parse(cls, card: Card) -> InstanceDBEntry:
        if card.file:
            return cls.parse_file(card)
        else:
            return cls.parse_data(card)

    @classmethod
    def json_sanitize(cls, line: str):
        result = line.replace("\\", "\\\\")
        result = result.replace("$", "\\$")
        return fr"`{result}`"

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
    def get_metadata_from_file(cls, card: Card) -> dict:
        """
        :param card: -todo-
        :return: dict of metadata it found and some information about the read itself
        """
        pass

    @classmethod
    @abstractmethod
    def get_metadata_from_data(cls, card: Card) -> dict:
        """
        This will be most likely used when dealing with references.
        :param card: -todo-
        :return: dict of metadata it found and some information about the read itself
        """
        pass

    @classmethod
    @abstractmethod
    def parse_file(cls, card: Card) -> InstanceDBEntry:
        """This method is what produces our final dict() of information to be used
        by ContentManager to craft the JSREF. All the references there might have been
        should have been replaced before.
        'from_file' version is most likely to be used during initial node handling.
        """

    @classmethod
    @abstractmethod
    def parse_data(cls, card: Card) -> InstanceDBEntry:
        """This method is what produces our final dict() of information to be used
        by ContentManager to craft the JSREF. All the references there might have been
        should have been replaced before.
        'from_string' version is most likely to be used when dealing with references."""
