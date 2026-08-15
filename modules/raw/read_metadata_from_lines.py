from importlib import import_module
rmfs = import_module(f"raw.read_metadata_from_string")


def read_metadata_from_lines(lines: list[str], newline_sequence: str) -> dict:
    """'cursor' is set to either \n
        * last character of last line that contained meta tag, \n
        * last character of meta tag in line that contains any other characters outside meta tags.
        :return: [dict] of found metadata in list of lines."""
    metadata = dict()
    cursor = 0

    for line in lines:
        received_metadata = rmfs.get_metadata_from_string(line)
        if len(received_metadata) > 0:
            for key, value in received_metadata.items():
                metadata[key] = value
        cursor += received_metadata["cursor"]
        line_after_cursor = line[received_metadata["cursor"]:]
        line_after_cursor_length = len(line_after_cursor)
        if len(line_after_cursor.strip()) > 0:
            # If there's any characters afterwards, stop iterating over the rest of the lines.
            # Previous method call (to parse one line) makes sure that remaining content is not another meta tag.
            break
        cursor += line_after_cursor_length  # If there is nothing more other than whitespaces - add them to cursor and keep iterating
        cursor += len(newline_sequence) - 1  # If newline sequence is "\r\n" then move cursor further to match the sequence

    metadata["cursor"] = cursor

    return metadata
