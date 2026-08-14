from pathlib import PurePath
import re
# Own imports
import read_metadata_from_lines as rmfl


def get_metadata_from_file(path: PurePath) -> dict:
    """'cursor' is set to either \n
        * last character of last line that contained meta tag, \n
        * last character of meta tag in line that contains any other characters outside meta tags.
        :return: [dict] of found metadata in given file."""
    tag_regex = r'\[%>(.*?):(.*?)<]'
    metadata = dict()
    lines = []

    with open(path, "rb") as f:
        while True:
            line = f.readline()
            if not line:
                break
            # This keeps original newline combinations, instead of auto translating them to "\n"
            line = line.decode()
            #
            reg_search = re.match(tag_regex, line.lstrip())
            lines.append(line)
            if not reg_search:
                break

    got = rmfl.read_metadata_from_lines(lines)
    if len(got) > 0:
        for key, value in got.items():
            metadata[key] = value

    return metadata
