import re
from pathlib import PurePath
from logging import Logger
# Own imports
from models.config import config
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue


class MetadataReader:
    possible_keys = [key.value for key in NodeMetadataKey]
    type_possible_values = [key.value for key in NodeMetadataTypeValue]

    def __init__(self, logger: Logger | None = None):
        self.logger = logger
        self.was_anything_else = False

    @classmethod
    def key_to_enum_type(cls, key):
        if isinstance(key, NodeMetadataKey):
            return key
        if key in MetadataReader.possible_keys:
            return NodeMetadataKey(key)
        return None

    @classmethod
    def type_value_to_enum_type(cls, value):
        if isinstance(value, NodeMetadataTypeValue):
            return value
        if value in MetadataReader.type_possible_values:
            return NodeMetadataTypeValue(value)
        return None

    def get_metadata_from_file(self, path: PurePath) -> (dict, bool):
        metadata = dict()
        was_anything_else = False
        with open(path) as f:
            for line in f.readlines():
                # lines can be commented out with "//"
                # todo add to tests
                if line.startswith("//"):
                    continue

                # empty lines also ignored
                # todo add to tests
                if len(line.strip()) == 0:
                    continue

                # do not read file further when tags end
                if not line.startswith("[%>"):
                    was_anything_else = True
                    break

                # if there's actually any tag, then get metadata
                retrieved = self.get_metadata_from_line(line)
                for key, value in retrieved[0].items():
                    metadata[key] = value

                # it there's any non-tag in a line, stop reading
                if was_anything_else or retrieved[1]:
                    was_anything_else = True
                    break

        return metadata, was_anything_else

    def get_metadata_from_line(self, line: str) -> (dict, bool):
        result_dict = dict()
        was_anything_else = False

        if line.startswith("[%>"):
            reg_search = re.search(r'(?:\[%>)(.*?):(.*?)]', line)

            while reg_search:
                processed = self._process_findings(reg_search)
                if processed is not None:
                    result_dict[processed[0]] = processed[1]

                line = line.replace(reg_search.group(0), "").strip()
                reg_search = None
                if line.startswith("[%>"):
                    reg_search = re.search(r'(?:\[%>)(.*?):(.*?)]', line)

        if len(line) > 0:
            was_anything_else = True

        return result_dict, was_anything_else

    def _process_findings(self, reg_search: re.Match) -> tuple | None:
        key = reg_search.groups()[0].lower()
        value = reg_search.groups()[1]

        # check if key is ok
        if key not in MetadataReader.possible_keys:
            if self.logger:
                config.logger.warning(f"Metadata key '{key}' is not recognized and is ignored")
            return None

        # check if value of key of 'type' is ok
        if key == "type" and value.lower() not in MetadataReader.type_possible_values:
            if self.logger:
                config.logger.warning(
                    f"Metadata value '{value}' for 'type' key is not recognized and is ignored")
            return None

        key = MetadataReader.key_to_enum_type(key)
        if key == NodeMetadataKey.TYPE:
            value = MetadataReader.type_value_to_enum_type(value.lower())

        return key, value

    def get_metadata_from_lines(self, lines: iter) -> list[tuple[dict, bool]]:
        metadata_list = list()

        for line in lines:
            result = self.get_metadata_from_line(line)
            metadata_list.append((result[0], result[1]))

        return metadata_list


def get_metadata(path: PurePath, logger: Logger = None):
    metadata = dict()
    had_anything_else = False

    with open(path) as f:
        for line in f.readlines():
            if line.startswith("//"):
                continue

            reg_search = re.search(r'(?:\[%>)(.*?):(.*?)]', line)
            if reg_search is None:
                if len(line.strip()) == 0:
                    had_anything_else = False
                    continue

                if len(line.strip()) > 0:
                    had_anything_else = True
                    continue

            if reg_search:
                # user did not provide key or value (or both)
                if len(reg_search.groups()) < 2:
                    if logger:
                        config.logger.warning(f"Metadata for line {line} has no key:value pair, line is ignored")
                    continue

                # both key and value are here, check for errors
                key = reg_search.groups()[0].lower()
                value = reg_search.groups()[1]
                # check if key is ok
                if key not in MetadataReader.possible_keys:
                    if logger:
                        config.logger.warning(f"Metadata key '{key}' is not recognized and is ignored")
                    continue
                # check if value of key of 'type' is ok
                if key == "type" and value.lower() not in MetadataReader.type_possible_values:
                    if logger:
                        config.logger.warning(
                            f"Metadata value '{value}' for 'type' key is not recognized and is ignored")
                    continue

            key = MetadataReader.key_to_enum_type(key)
            if key == NodeMetadataKey.TYPE:
                value = MetadataReader.type_value_to_enum_type(value.lower())
            metadata[key] = value

    # if had_anything_else is False and metadata.get(NodeMetadataKey.TYPE) is None and len(metadata) > 0:
    #     metadata[NodeMetadataKey.TYPE] = NodeMetadataTypeValue.METAFILE

    return metadata, had_anything_else


if __name__ == "__main__":
    metadata_reader = MetadataReader()
    got_meta = metadata_reader.get_metadata_from_line("[%>title:jeff][%>type:metafile]")
    print(got_meta)
