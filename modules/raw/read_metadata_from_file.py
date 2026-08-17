from pathlib import PurePath
import re
from importlib import import_module
from tag_matcher import TagMatcher, TagPair
rmfl = import_module(f"raw.read_metadata_from_lines")


def get_metadata_from_file(path: PurePath) -> dict:
    starting_tag = "[-["
    ending_tag = "]-]"
    meta_tags = TagPair({starting_tag}, {ending_tag})
    tag_lines = []
    metadata = dict()
    #
    with open(path, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if starting_tag in line:
                tag_lines.append(line)
            else:
                break
    #
    items = TagMatcher.match("".join(tag_lines), [meta_tags]).get_tree()
    for item in items:
        if item.is_tag():
            parts = item.get_inner().split("=", 1)
            if len(parts) == 2:
                metadata[parts[0]] = parts[1]
        else:
            if len(item.tag.strip()) > 0:  # Check if it's any sort of blank line or characters
                break
    # metadata["fileMeta"] = items
    return metadata


def get_metadata_from_file2(path: PurePath) -> dict:
    """'cursor' is set to either \n
        * last character of last line that contained meta tag, \n
        * last character of meta tag in line that contains any other characters outside meta tags.
        :return: [dict] of found metadata in given file."""
    tag_regex = r'\[=>(.*?):(.*?)<=]'
    metadata = dict()
    newline_sequence = ""
    lines_with_meta = []

    with open(path, "rb") as f:
        # Step 1 - write down newline sequence
        has_things_in_it = True
        first_line = f.readline()
        if not first_line:
            has_things_in_it = False
        else:
            first_line = first_line.decode()
            if first_line.endswith("\n"):  # Saving newline sequence for similar need, but for methods that have no access to original file
                if first_line.endswith("\r\n"):
                    newline_sequence = "\r\n"
                else:
                    newline_sequence = "\n"
            if first_line.endswith("\r"):
                newline_sequence = "\r"
            metadata["newlineSeq"] = newline_sequence

        # Step 2 - iterate over lines and see and write down all lines with meta tags in them
        if has_things_in_it:
            f.seek(0)
            while True:
                line = f.readline()
                if not line:
                    break
                line = str(line.decode()).replace("\r\n", "\n")
                reg_search = re.match(tag_regex, line.lstrip())
                lines_with_meta.append(line)
                if not reg_search:
                    break

    got = rmfl.read_metadata_from_lines(lines_with_meta, newline_sequence)
    if len(got) > 0:
        for key, value in got.items():
            metadata[key] = value

    return metadata
