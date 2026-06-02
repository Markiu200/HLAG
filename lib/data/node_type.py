from enum import Enum


class NodeMetadataKey(Enum):
    TITLE = "title"
    TYPE = "type"
    MODULE = "module"
    META = "meta"


class NodeMetadataTypeValue(Enum):
    TEXT = "text"
    DICTIONARY = "dictionary"
    IMAGE = "image"
    METAFILE = "metafile"
    CONTAINER = "container"
    UNSUPPORTED = "unsupported"
