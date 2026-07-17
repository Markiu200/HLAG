import re


def get_metadata_from_string(data: str):
    tag_regex = r'\[%>(.*?):(.*?)]'
    metadata = dict()
    cursor = 0

    while True:
        # set up for look ahead
        previous_length = len(data)
        stripped = data.lstrip()
        # see if there's any matches
        reg_search = re.match(tag_regex, stripped)
        # if no matches, leave it all as it is
        if not reg_search:
            break
        # if matches, do the actual strip and move the cursor the strip amount
        data = data.lstrip()
        cursor += previous_length - len(data)
        # move the cursor the match amount and prepare string for new search
        cursor += reg_search.regs[0][1]
        data = data.replace(reg_search.group(0), "", 1)
        # update metadata
        metadata[reg_search.groups()[0].lower()] = reg_search.groups()[1].lower()

    metadata["cursor"] = cursor
    return metadata
