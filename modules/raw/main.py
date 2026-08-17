import re
from pathlib import PurePath
from importlib import import_module
# Own imports
from module_facade import ModuleFacade, Card, InstanceDBEntry
from module_management import IModule
from tag_matcher import TagPair, TagMatcher


def get_module_main_class():
    return Raw


class Raw(IModule):
    module_path = PurePath(__file__).parent
    txt_check = import_module(f"raw.txt_check")
    rr = import_module(f"raw.replace_orders")
    rmff = import_module(f"raw.read_metadata_from_file")
    rmfl = import_module(f"raw.read_metadata_from_lines")

    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "raw",
            "priority": 1,
            "dependencies": [],
            "controller": "RawModuleController"
        }

    @classmethod
    def register_checks(cls):
        ModuleFacade.register_check(cls.txt_check.TXTCheck())

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))
        ModuleFacade.register_css(PurePath(cls.module_path, "raw.css"))

    @classmethod
    def get_metadata_from_file(cls, card: Card) -> dict:
        return cls.rmff.get_metadata_from_file(card.node.path)

    @classmethod
    def get_metadata_from_data(cls, card: Card) -> dict:
        return cls.rmfl.read_metadata_from_lines([card.content])

    @classmethod
    def replace_orders(cls, card: Card) -> str:
        """
        :param card: Card with "content" set to string in question.
        :return: content from Data structure, but with orders replaced with jsrefs
        """
        return cls.rr.replace_orders(card)

    @classmethod
    def parse_file(cls, card: Card) -> InstanceDBEntry:
        with open(card.node.path) as f:
            card.content = f.read()
        # card.file = False
        #
        tree = card.meta.get("fileMeta")
        if tree is not None:
            for item in tree:
                if item.is_tag():
                    outer = item.get_outer()
                    card.content = card.content.replace(outer, "", 1)
                else:
                    if len(item.tag.strip()) > 0:  # Check if it's any sort of blank line or characters
                        break
            card.meta.pop("fileMeta")
        return cls.parse_data(card)

        # past_meta_location = card.node.metadata.get("cursor", 0)
        # with open(card.node.path) as f:
        #     f.seek(past_meta_location)
        #     card.content = f.read()
        # card.file = False
        # return cls.parse_data(card)

    @classmethod
    def parse_data(cls, card: Card) -> InstanceDBEntry:
        meta_tags = TagPair({"[-["}, {"]-]"})
        items = TagMatcher.match(card.content, [meta_tags]).get_tree()
        for item in items:
            if item.is_tag():
                parts = item.get_inner().split("=", 1)
                if len(parts) == 2:
                    card.meta[parts[0]] = parts[1]
                outer = item.get_outer()
                card.content = card.content.replace(outer, "", 1)
            else:
                if len(item.tag.strip()) > 0:  # Check if it's any sort of blank line or characters
                    break


        # content_metadata = cls.rmfl.read_metadata_from_lines(card.content.splitlines(), card.meta.get("newlineSeq", ""))
        # if len(content_metadata) > 0:
        #     for key, value in content_metadata.items():
        #         card.meta[key] = value
        # card.content = card.content[card.meta["cursor"]:]

        ignore_lines = card.meta.get("ignore-lines")
        enable_references = False if card.meta.get("references") == "disabled" else True

        content = cls.replace_orders(card)
        # content = card.content

        pattern = r'\[&_JSREF\(.*?\)_&]'
        data_list = []
        current_data = ""
        splitted = content.splitlines(keepends=True)
        #
        for line in splitted:
            if ignore_lines:
                if line.startswith(ignore_lines):
                    continue
                line = cls.ignore_lines_filter(pattern=ignore_lines, line=line)
            if enable_references:
                jsref_found = re.search(pattern, line)
                if jsref_found:
                    remainder = line
                    while jsref_found:
                        parts = remainder.split(sep=jsref_found.group(), maxsplit=1)
                        if len(parts[0]) + len(current_data) > 0:  # append left part (if any) to current_data and flush
                            data_list.append({
                                "isRef": 0,
                                "line": "".join([current_data, parts[0]])
                            })
                            current_data = ""
                        data_list.append({  # append that find and flush
                            "isRef": 1,
                            "line": jsref_found.group()
                        })
                        remainder = parts[1]
                        jsref_found = re.search(pattern, remainder)  # search again in what is left
                        if not jsref_found:
                            current_data = parts[1]
                else:
                    current_data = "".join([current_data, line])
            else:
                # --- add line ---
                current_data = "".join([current_data, line])
        # finish
        if len(current_data) > 0:
            data_list.append({
                "isRef": 0,
                "line": current_data
            })
        #
        result_data = '{"nodes": ['
        for i, item in enumerate(data_list):
            result_data = "".join([
                result_data,
                "{",
                f'"isRef": {item["isRef"]}, "line": {cls.json_sanitize(item["line"])}',
                "}"]
            )
            if i < len(data_list) - 1:
                result_data = "".join([result_data, ", "])
        result_data = "".join([result_data, "]}"])

        result_entry = InstanceDBEntry(
            module=cls.get_info()["name"],
            data=result_data,
            meta=card.meta
        )
        return result_entry

    @classmethod
    def ignore_lines_filter(cls, pattern: str, line: str):
        parts = line.split(pattern)
        return parts[0]