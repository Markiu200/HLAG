from pathlib import PurePath
from importlib import import_module
import re
# Own imports
from lib.imodule import IModule
from lib.module_manager import ModuleManager
from lib.tag_matcher import TagPair, TagMatcher, Part, RightPart, Middle


def register(module_manager: ModuleManager):
    return Raw(module_manager)


class Raw(IModule):
    def __init__(self, module_manager: ModuleManager | None = None):
        super().__init__()
        self.module_path = PurePath(__file__).parent
        self.info = {
            "codename": "raw",
            "priority": 1,
            "controller": "RawModuleController"
        }
        self.module_manager = module_manager
        if self.module_manager:
            self.config = module_manager.config
            # Register prints
            js_path = PurePath(self.module_path, "js.js")
            controller_path = PurePath(self.module_path, "raw.js")
            self.module_manager.register_print(self, js_path, "js", is_file=True, is_delayed=False)
            self.module_manager.register_print(self, controller_path, "js", is_file=True, is_delayed=False)
            # Register checks
            txt_check = import_module("raw.txt_check")
            self.module_manager.register_check(self, txt_check.TXTCheck(), "mid")
            # Fetch config data
            self.jsref_open = self.config.get_base_config().get("jstag_open")
            self.jsref_close = self.config.get_base_config().get("jstag_close")
        else:
            self.jsref_open = "[&_JSREF("
            self.jsref_close = ")_&]"

        # Module work related
        self.meta_tags = ("[-[", "]-]")
        self.meta_tags_tagpair = TagPair({self.meta_tags[0]}, {self.meta_tags[1]})
        self.order_tags = ("[%>mod:", "<%]")
        self.order_tags_tagpair = TagPair({self.order_tags[0]}, {self.order_tags[1]})

    def get_metadata(self, value, is_file: bool) -> dict:
        if is_file:
            return self.get_metadata_from_file(value)
        else:
            return self.get_metadata_from_data(value)

    def get_metadata_from_data(self, value: str) -> dict:
        raw_lines = value.splitlines()
        tag_lines = []
        metadata = dict()
        #
        for line in raw_lines:
            if self.meta_tags[0] in line:
                tag_lines.append(line)
            else:
                break
        #
        items = TagMatcher.match("".join(tag_lines), [self.meta_tags_tagpair]).get_tree()
        for item in items:
            if item.is_tag():
                parts = item.get_inner().split("=", 1)
                if len(parts) == 2:
                    metadata[parts[0]] = parts[1]
            else:
                if len(item.tag.strip()) > 0:  # Check if it's any sort of blank line or characters
                    break
        return metadata

    def get_metadata_from_file(self, value) -> dict:
        tag_lines = []
        metadata = dict()
        #
        with open(str(value), "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if self.meta_tags[0] in line:
                    tag_lines.append(line)
                else:
                    break
        #
        items = TagMatcher.match("".join(tag_lines), [self.meta_tags_tagpair]).get_tree()
        for item in items:
            if item.is_tag():
                parts = item.get_inner().split("=", 1)
                if len(parts) == 2:
                    metadata[parts[0]] = parts[1]
            else:
                if len(item.tag.strip()) > 0:  # Check if it's any sort of blank line or characters
                    break
        return metadata

    def parse(self, value, metadata: dict, is_file: bool) -> str:
        # Step 1 - If parsing file, get content from file
        if is_file:
            with open(str(value)) as f:
                content = f.read()
        else:
            content = value

        # Step 2 - Read metadata, remove them from text, and adjust newlines
        items = TagMatcher.match(content, [self.meta_tags_tagpair, self.order_tags_tagpair]).get_tree()
        ## reading metadata
        for item in items:
            if item.is_tag() and item.get_left().tag == self.meta_tags[0]:
                parts = item.inner_text.split("=", 1)
                if len(parts) == 2:
                    metadata[parts[0]] = parts[1]
        ## removing metadata and adjusting newlines
        content = self.craft(items)

        # Step 3 - Replace orders
        content = self.replace_orders(content, metadata)

        # Step 4 - Do the parsing
        ## read metadata
        ignore_lines = metadata.get("ignore-lines")
        enable_references = False if metadata.get("references") == "disabled" else True

        ## parse
        data_list = []

        if ignore_lines:
            splitted = content.splitlines(keepends=True)
            after_ignoring = []
            for line in splitted:
                after_ignoring.append(Raw.ignore_lines_filter(pattern=ignore_lines, line=line))
            content = "".join(after_ignoring)

        if enable_references:
            pattern = rf'({re.escape(self.jsref_open)}.*?{re.escape(self.jsref_close)})'
            parts = re.split(pattern, content)
            even = True
            for part in parts:
                if even:
                    data_list.append(Text(part))
                    even = not even
                else:
                    data_list.append(Order(part))
                    even = not even
        else:
            data_list.append(Text(content))

        # Step 5 - Return encoded content
        merged_data_list = ", ".join([item.js_prepared() for item in data_list])
        result_data = "".join(['{"nodes": [', merged_data_list, "]}"])
        #
        # result_entry = InstanceDBEntry(
        #     module=self.get_info()["name"],
        #     data=result_data,
        #     meta=card.meta
        # )
        return result_data

    def replace_orders(self, content: str, metadata: dict) -> str:
        """
        :param content: Input string.
        :param metadata: Metadata of containing DocumentNode (metadata passed to parse method)
        :return: String with orders replaced with jsrefs
        """
        nested_item_count = 0
        new_content = ""
        #
        items = TagMatcher.match(content, [self.order_tags_tagpair]).get_tree()
        for item in items:
            if item.is_tag():
                order = item.get_inner()
                parts = order.split("=", 1)
                module_name = parts[0]
                content = parts[1]
                #
                new_meta = dict(metadata)
                if new_meta.get("relPath"):  # Make relPath "unique"
                    new_meta["relPath"] = "_".join([new_meta["relPath"], str(nested_item_count)])
                    nested_item_count += 1
                if new_meta.get("relLink"):  # relLink belongs only to the requester, not children
                    new_meta.pop("relLink")
                new_meta["module"] = module_name
                # order_card = Card(
                #     node=card.node,
                #     file=False,
                #     meta=new_meta,
                #     content=content
                # )
                # jsref = ModuleFacade.snippets.get_ref(order_card).as_string()
                if self.module_manager:
                    jsref = self.module_manager.toolbox.content_manager.nest_ref(
                        parts[0], parts[1], new_meta
                    )
                    jsref = f"{self.jsref_open}{jsref.module},{jsref.ref_id}{self.jsref_close}"
                else:
                    jsref = f"{self.jsref_open}REPL,X{self.jsref_close}"
                new_content = "".join([new_content, jsref])
            else:
                new_content = "".join([new_content, item.tag])
        return new_content

    @classmethod
    def ignore_lines_filter(cls, pattern: str, line: str):
        parts = line.split(pattern)
        return parts[0]

    def craft(self, items: list[Part]) -> str:
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
            elif isinstance(item, RightPart) and item.get_left().tag == self.meta_tags[0]:
                # If tag is metadata tag, include it in card's metadata.
                # Do not add that tag to text.
                encountered_meta = True
                # parts = item.inner_text.split("=", 1)     # we did this already?
                # if len(parts) == 2:
                #     card.meta[parts[0]] = parts[1]
            #
            elif isinstance(item, RightPart) and item.get_left().tag == self.order_tags[0]:
                # If tag is order tag, include entire tag in text - it will be parsed
                # by "replace orders" method later. For reason similar to metadata tags,
                # if "content" of this tag begins with newline, one newline will be removed.
                parts = item.inner_text.split("=", 1)
                if len(parts) == 2 and parts[1].startswith("\n"):
                    starting_bit = "".join([item.get_left().tag, parts[0], "="])
                    item.outer_text = item.outer_text.replace(f"{starting_bit}\n", starting_bit, 1)
                new_content = "".join([new_content, item.outer_text])
        #
        return new_content


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


_all_ = [Raw]

if __name__ == '__main__':
    pmmodule_ = Raw()
    ml_ = pmmodule_.meta_tags[0]
    mr_ = pmmodule_.meta_tags[1]
    text1_ = f"""{ml_}ignore-lines=---{mr_}Post meta;
Hello world! {pmmodule_.order_tags[0]}raw=This is the nested tag{pmmodule_.order_tags[1]}. Post nest."""
    print(pmmodule_.get_metadata(text1_, is_file=False))
    print(pmmodule_.parse(text1_, dict(), is_file=False))
