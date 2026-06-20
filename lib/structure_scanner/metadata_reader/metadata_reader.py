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
    has_leftovers: bool
    leftovers: str
    last_line: int


class MetadataReader:
    possible_keys = [key.value for key in NodeMetadataKey]
    type_possible_values = [key.value for key in NodeMetadataTypeValue]

    def __init__(self, logger: Logger | None = None):
        self.logger = logger
        self.tag_regex = r'^(?:\[%>)(.*?):(.*?)]'

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

    def get_metadata_from_file(self, path: PurePath) -> ReadResults:
        metadata = dict()
        last_line = 0

        result = None
        with open(path) as f:
            for line in f.readlines():
                last_line += 1
                result = self.get_metadata_from_line(line)
                if len(result.metadata) > 0:
                    for key, value in result.metadata.items():
                        metadata[key] = value
                if result.last_line == -1:
                    # if it was empty line, last line was actually previous one
                    last_line -= 1
                    break
                if result.last_line > 0:
                    break

        if result is None:
            return ReadResults(
                metadata=dict(),
                has_leftovers=False,
                leftovers="",
                last_line=last_line
            )
        else:
            return ReadResults(
                metadata=metadata,
                has_leftovers=result.has_leftovers,
                leftovers=result.leftovers,
                last_line=last_line
            )

    def get_metadata_from_lines(self, lines: iter) -> ReadResults:
        metadata = dict()
        last_line = 0

        result = None
        for line in lines:
            line += 1
            result = self.get_metadata_from_line(line)
            if len(result.metadata) > 0:
                for key, value in result.metadata.items():
                    metadata[key] = value
            if result.last_line == -1:
                # if it was empty line, last line was actually previous one
                last_line -= 1
                break
            if result.last_line > 0:
                break

        if result is None:
            return ReadResults(
                metadata=dict(),
                has_leftovers=False,
                leftovers="",
                last_line=last_line
            )
        else:
            return ReadResults(
                metadata=metadata,
                has_leftovers=result.has_leftovers,
                leftovers=result.leftovers,
                last_line=last_line
            )

    def get_metadata_from_line(self, line: str) -> ReadResults:
        metadata = dict()
        has_leftovers = False
        last_line = 0

        # first check if the line would be considered as "last" for reader - empty line
        if len(line.strip()) == 0:
            last_line = -1

        # strip the comments
        comment_search = re.search(r'(//.*)', line)
        if comment_search is not None:
            line = line.replace(comment_search.group(0), "")

        line = line.strip()
        reg_search = re.match(self.tag_regex, line)

        while reg_search:
            processed = self._process_findings(reg_search)
            if processed is not None:
                metadata[processed[0]] = processed[1]

            line = line.replace(reg_search.group(0), "").strip()
            reg_search = re.match(self.tag_regex, line)

        leftovers = line
        if len(leftovers) > 0:
            has_leftovers = True
            # second check if the line would be considered "last" for reader - leftovers
            last_line = 1

        return ReadResults(
            metadata=metadata,
            has_leftovers=has_leftovers,
            leftovers=leftovers,
            last_line=last_line
        )

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


if __name__ == "__main__":
    pass
