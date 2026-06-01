from pathlib import PurePath
import re
from logging import Logger
# Own imports
from models.config import config

possible_keys = ("title", "type", "module", "meta")
type_possible_values = ("dictionary", "image", "metafile", "unsupported")


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
                if len(reg_search.groups()) < 2:
                    if logger:
                        config.logger.warning(f"Metadata for line {line} has no key:value pair, line is ignored")
                    continue
                key = reg_search.groups()[0]
                value = reg_search.groups()[1]
                if key not in possible_keys:
                    if logger:
                        config.logger.warning(f"Metadata key '{key}' is not recognized and is ignored")
                    continue
                if key == "type" and value not in type_possible_values:
                    if logger:
                        config.logger.warning(f"Metadata value '{value}' for 'type' key is not recognized and is ignored")
                    continue

            metadata[key] = value

    if had_anything_else is False and metadata.get("type") is None and len(metadata) > 0:
        metadata["type"] = "metafile"

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
