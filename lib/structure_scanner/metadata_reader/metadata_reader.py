import re
from pathlib import PurePath
from logging import Logger
from dataclasses import dataclass
# Own imports
from models.config import config
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue


@dataclass
class ReadResults:
    metadata: dict
    cursor: int


class MetadataReader:
    possible_keys = [key.value for key in NodeMetadataKey]
    type_possible_values = [key.value for key in NodeMetadataTypeValue]
    tag_regex = None
    logger = None

    @classmethod
    def key_to_enum_type(cls, key: str | NodeMetadataKey):
        """Translates string representation of key to enum type."""
        if isinstance(key, NodeMetadataKey):
            return key
        if key in MetadataReader.possible_keys:
            return NodeMetadataKey(key)
        return None

    @classmethod
    def type_value_to_enum_type(cls, value: str | NodeMetadataTypeValue):
        """Translates string representation of value for TYPE key to enum type."""
        if isinstance(value, NodeMetadataTypeValue):
            return value
        if value in MetadataReader.type_possible_values:
            return NodeMetadataTypeValue(value)
        return None

    @classmethod
    def set_tag_regex(cls, reg: str):
        cls.tag_regex = reg

    @classmethod
    def set_logger(cls, logger: Logger):
        cls.logger = logger

    @classmethod
    def get_metadata_from_file(cls, path: PurePath) -> ReadResults:
        metadata = dict()
        lines = []

        with open(path) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                reg_search = re.match(MetadataReader.tag_regex, line.lstrip())
                lines.append(line)
                if not reg_search:
                    break

        got = MetadataReader.get_metadata_from_lines(lines)
        if len(got.metadata) > 0:
            for key, value in got.metadata.items():
                metadata[key] = value

        return ReadResults(
            metadata=metadata,
            cursor=got.cursor
        )

    @classmethod
    def get_metadata_from_lines(cls, lines: list[str]) -> ReadResults:
        metadata = dict()
        cursor = 0

        for line in lines:
            got = MetadataReader.get_metadata_from_string(line)
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

        return ReadResults(
            metadata=metadata,
            cursor=cursor
        )

    @classmethod
    def get_metadata_from_string(cls, data: str) -> ReadResults:
        metadata = dict()
        cursor = 0

        while True:
            # set up for look ahead
            p_len = len(data)
            stripped = data.lstrip()
            # see if there's any matches
            reg_search = re.match(MetadataReader.tag_regex, stripped)
            # if no matches, leave it all as it is
            if not reg_search:
                break
            # if matches, do the actual strip and move the cursor the strip amount
            data = data.lstrip()
            cursor += p_len - len(data)
            # move the cursor the match amount and prepare string for new search
            cursor += reg_search.regs[0][1]
            data = data.replace(reg_search.group(0), "", 1)
            # process the match as needed
            processed = MetadataReader._process_findings(reg_search)
            if processed is not None:
                metadata[processed[0]] = processed[1]

        return ReadResults(
            metadata=metadata,
            cursor=cursor
        )

    @classmethod
    def _process_findings(cls, reg_search: re.Match) -> tuple | None:
        key = reg_search.groups()[0].lower()
        value = reg_search.groups()[1].lower()

        # check if key is ok
        if key not in MetadataReader.possible_keys:
            if MetadataReader.logger:
                config.logger.warning(f"Metadata key '{key}' is not recognized and is ignored")
            return None

        # check if value of key of 'type' is ok
        if key == "type" and value not in MetadataReader.type_possible_values:
            if MetadataReader.logger:
                config.logger.warning(
                    f"Metadata value '{value}' for 'type' key is not recognized and is ignored")
            return None

        key = MetadataReader.key_to_enum_type(key)
        if key == NodeMetadataKey.TYPE:
            value = MetadataReader.type_value_to_enum_type(value.lower())

        return key, value


if __name__ == "__main__":
    pass
