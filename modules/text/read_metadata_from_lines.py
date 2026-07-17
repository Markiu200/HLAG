import read_metadata_from_string as rmfs


def read_metadata_from_lines(lines: list[str]):
    metadata = dict()
    cursor = 0

    for line in lines:
        got = rmfs.get_metadata_from_string(line)
        if len(got.metadata) > 0:
            for key, value in got.metadata.items():
                metadata[key] = value
        cursor += got.cursor
        line_after = line[got.cursor:]
        line_after_len = len(line_after)
        if len(line_after.strip()) > 0:
            # checks if after getting all the metadata from line there's more text
            break
        # if there wasn't but there were whitespaces - add them to cursor
        cursor += line_after_len

    metadata["cursor"] = cursor

    return metadata
