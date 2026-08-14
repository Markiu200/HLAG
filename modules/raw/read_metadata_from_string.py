import re


def get_metadata_from_string(line: str) -> dict:
    """:return: [dict] of found metadata in line. 'cursor' is set to end of last found meta tag, or 0 if none found."""
    tag_regex = r'\[%>(.*?):(.*?)<]'
    metadata = dict()
    cursor = 0

    while True:
        initial_line_length = len(line)
        temporarily_lstripped_line = line.lstrip()
        reg_search = re.match(tag_regex, temporarily_lstripped_line)  # See if there's any matches
        if not reg_search:
            break  # If no matches, leave it all as it is
        line = line.lstrip()  # If matches - do the actual strip
        cursor += initial_line_length - len(line)  # Move the curser the lstrip amount
        cursor += reg_search.regs[0][1]  # Move the cursor to the end of match
        line = line.replace(reg_search.group(0), "", 1)  # Remove match from the line
        # update metadata
        metadata[reg_search.groups()[0]] = reg_search.groups()[1]

    metadata["cursor"] = cursor
    return metadata
