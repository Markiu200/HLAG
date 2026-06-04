import re
from pathlib import PurePath
from logging import Logger
# Own imports
from models.config import config
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue

possible_keys = [key.value for key in NodeMetadataKey]
type_possible_values = [key.value for key in NodeMetadataTypeValue]


def key_to_enum_type(key):
    if isinstance(key, NodeMetadataKey):
        return key
    if key in possible_keys:
        return NodeMetadataKey(key)
    return None


def type_value_to_enum_type(value):
    if isinstance(value, NodeMetadataTypeValue):
        return value
    if value in possible_keys:
        return NodeMetadataTypeValue(value)
    return None


def get_metadata(path: PurePath, logger: Logger = None):
    metadata = dict()
    had_anything_else = False

    with open(path) as f:
        for line in f.readlines():
            if line.startswith("//"):
                continue

            reg_search = re.search('^\[%>(.*?)\:(.*?)\]', line)
            if reg_search is None:
                if len(line.strip()) == 0:
                    had_anything_else = False
                    continue

                if len(line.strip()) > 0:
                    had_anything_else = True
                    continue

            if reg_search:
                # user did not provide key or value (or both)
                # todo add in tests wrongly typed in data
                if len(reg_search.groups()) < 2:
                    if logger:
                        config.logger.warning(f"Metadata for line {line} has no key:value pair, line is ignored")
                    continue

                # both key and value are here, check for errors
                key = reg_search.groups()[0].lower()
                value = reg_search.groups()[1]
                # check if key is ok
                if key not in possible_keys:
                    if logger:
                        config.logger.warning(f"Metadata key '{key}' is not recognized and is ignored")
                    continue
                # check if value of key of 'type' is ok
                if key == "type" and value.lower() not in type_possible_values:
                    if logger:
                        config.logger.warning(f"Metadata value '{value}' for 'type' key is not recognized and is ignored")
                    continue

            key = key_to_enum_type(key)
            if key == NodeMetadataKey.TYPE:
                value = type_value_to_enum_type(value.lower())
            metadata[key] = value

    if had_anything_else is False and metadata.get(NodeMetadataKey.TYPE) is None and len(metadata) > 0:
        metadata[NodeMetadataKey.TYPE] = NodeMetadataTypeValue.METAFILE

    return metadata


if __name__ == "__main__":
    test_files = (
        PurePath("D:\\hlag\\tests\\metafiles\\meta1.txt"),
        PurePath("D:\\hlag\\tests\\metafiles\\meta2.txt"),
        PurePath("D:\\hlag\\tests\\metafiles\\meta3.txt"),
        PurePath("D:\\hlag\\tests\\metafiles\\meta4.txt"),
        PurePath("D:\\hlag\\tests\\metafiles\\meta5.txt"),
    )

    for test_file in test_files:
        test_metadata = get_metadata(test_file)
        for tkey, tvalue in test_metadata.items():
            print(f"{tkey}: {tvalue}")
        print()

    # test_lines = [
    #     "[%>title:jeff]"
    #     "[%>title]",
    #     "[>title]",
    #     "[%>title]jeff]",
    #     "[%>title:jeff][%>title:jeff]"
    # ]
    #
    # for test_line in test_lines:
    #     test_reg_search = re.search('^\[%>(.*?)\:(.*?)\]', test_line)
    #     print(test_reg_search)
    #     if test_reg_search is not None:
    #         print(test_reg_search.groups())
    #
    # print(len("\n".strip()))
    # print("\n".strip() is None)
