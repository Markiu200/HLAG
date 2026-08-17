import re
from pathlib import PurePath
from importlib import import_module
# Own imports
from module_facade import ModuleFacade, Card, InstanceDBEntry, Ref
from module_management import IModule
from tag_matcher import TagPair, TagMatcher, RightPart, Middle, Part


def get_module_main_class():
    return Raw


class Raw(IModule):
    module_path = PurePath(__file__).parent
    txt_check = import_module(f"raw.txt_check")
    #
    meta_tags = ("[-[", "]-]")
    meta_tags_tagpair = TagPair({meta_tags[0]}, {meta_tags[1]})
    order_tags = ("[%>mod:", "<%]")
    order_tags_tagpair = TagPair({order_tags[0]}, {order_tags[1]})

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
        tag_lines = []
        metadata = dict()
        #
        with open(card.node.path, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if cls.meta_tags[0] in line:
                    tag_lines.append(line)
                else:
                    break
        #
        items = TagMatcher.match("".join(tag_lines), [cls.meta_tags_tagpair]).get_tree()
        for item in items:
            if item.is_tag():
                parts = item.get_inner().split("=", 1)
                if len(parts) == 2:
                    metadata[parts[0]] = parts[1]
            else:
                if len(item.tag.strip()) > 0:  # Check if it's any sort of blank line or characters
                    break
        return metadata

    @classmethod
    def get_metadata_from_data(cls, card: Card) -> dict:
        return dict()  # turns out this method is never used in practice, unless other modules would like to use it

    @classmethod
    def parse_file(cls, card: Card) -> InstanceDBEntry:
        return cls.parse_data(card)

    @classmethod
    def parse_data(cls, card: Card) -> InstanceDBEntry:
        # Step 1 - If parsing file, get content from file
        if card.file:
            with open(card.node.path) as f:
                card.content = f.read()

        # Step 2 - Read metadata, remove them from text, and adjust newlines
        items = TagMatcher.match(card.content, [cls.meta_tags_tagpair, cls.order_tags_tagpair]).get_tree()
        ## reading metadata
        for item in items:
            if item.is_tag() and item.get_left().tag == "[-[":
                parts = item.inner_text.split("=", 1)
                if len(parts) == 2:
                    card.meta[parts[0]] = parts[1]
        ## removing metadata and adjusting newlines
        cls.craft(items, card)

        # Step 3 - Replace orders
        content = cls.replace_orders(card)

        # Step 4 - Do the parsing
        ## read metadata
        ignore_lines = card.meta.get("ignore-lines")
        enable_references = False if card.meta.get("references") == "disabled" else True
        #
        pattern = rf'({re.escape(Ref.start_tag)}.*?{re.escape(Ref.end_tag)})'
        data_list = []
        current_data = ""
        splitted = content.splitlines(keepends=True)
        #
        for line in splitted:
            if ignore_lines:
                line = cls.ignore_lines_filter(pattern=ignore_lines, line=line)
            if enable_references:
                parts = re.split(pattern, line)
                even = True
                for part in parts:
                    if even:
                        current_data = "".join([current_data, part])
                        data_list.append(Text(current_data))
                        current_data = ""
                        even = not even
                    else:
                        data_list.append(Order(line))
                        even = not even
            else:
                data_list.append(Text(line))

        # Step 5 - Return InstanceDBEntry
        merged_data_list = ", ".join([item.js_prepared() for item in data_list])
        result_data = "".join(['{"nodes": [', merged_data_list, "]}"])
        #
        result_entry = InstanceDBEntry(
            module=cls.get_info()["name"],
            data=result_data,
            meta=card.meta
        )
        return result_entry

    @classmethod
    def replace_orders(cls, card: Card) -> str:
        """
        :param card: Card with "content" set to string in question.
        :return: content from Data structure, but with orders replaced with jsrefs
        """
        nested_item_count = 0
        new_content = ""
        #
        items = TagMatcher.match(card.content, [cls.order_tags_tagpair]).get_tree()
        for item in items:
            if item.is_tag():
                order = item.get_inner()
                parts = order.split("=", 1)
                module_name = parts[0]
                content = parts[1]
                #
                new_meta = dict(card.meta)
                if new_meta.get("relPath"):  # Make relPath "unique"
                    new_meta["relPath"] = "_".join([new_meta["relPath"], str(nested_item_count)])
                    nested_item_count += 1
                if new_meta.get("relLink"):  # relLink belongs only to the requester, not children
                    new_meta.pop("relLink")
                new_meta["module"] = module_name
                order_card = Card(
                    node=card.node,
                    file=False,
                    meta=new_meta,
                    content=content
                )
                jsref = ModuleFacade.content_manager.get_ref(order_card).as_string()
                new_content = "".join([new_content, jsref])
            else:
                new_content = "".join([new_content, item.tag])
        return new_content

    @classmethod
    def ignore_lines_filter(cls, pattern: str, line: str):
        parts = line.split(pattern)
        return parts[0]

    @classmethod
    def craft(cls, items: list[Part], card: Card) -> Card:
        new_content = ""
        encountered_meta = False
        for item in items:
            if isinstance(item, Middle):
                # If text is after metatag, we assume new line character was there
                # for an aesthetic choice. One newline is stripped and rest remains.
                if encountered_meta and item.tag.startswith("\n"):
                    item.tag = item.tag.replace("\n", "", 1)
                new_content = "".join([new_content, item.tag])
            #
            elif isinstance(item, RightPart) and item.get_left().tag == "[-[":
                # If tag is metadata tag, include it in card's metadata.
                # Do not add that tag to text.
                encountered_meta = True
                parts = item.inner_text.split("=", 1)
                if len(parts) == 2:
                    card.meta[parts[0]] = parts[1]
            #
            elif isinstance(item, RightPart) and item.get_left().tag == "[%>mod:":
                # If tag is order tag, include entire tag in text - it will be parsed
                # by "replace orders" method later. For reason similar to metadata tags,
                # if "content" of this tag begins with newline, one newline will be removed.
                parts = item.inner_text.split("=", 1)
                if len(parts) == 2 and parts[1].startswith("\n"):
                    starting_bit = "".join([item.get_left().tag, parts[0], "="])
                    item.outer_text = item.outer_text.replace(f"{starting_bit}\n", starting_bit, 1)
                new_content = "".join([new_content, item.outer_text])
        #
        card.content = new_content
        return card


class Element:
    def js_prepared(self) -> str:
        pass


class Text(Element):
    def __init__(self, string: str):
        self.string = string

    def js_prepared(self) -> str:
        return "".join(['{"isRef": 0, "line": ', IModule.json_sanitize(self.string), "}"])


class Order(Element):
    def __init__(self, string: str):
        self.string = string

    def js_prepared(self) -> str:
        return "".join(['{"isRef": 1, "line": `', self.string, "`}"])
