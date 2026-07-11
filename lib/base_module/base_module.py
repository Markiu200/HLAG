from abc import ABC, abstractmethod
import re
# Own imports
from structure_scanner.document_tree.document_node import DocumentNode
from module_manager import ModuleManager
from structure_scanner.metadata_reader.metadata_reader import MetadataReader
# temp
from modules.text.main import Text
from content_manager import ContentManager


class BaseReference:
    def __init__(self, begin: int, end: int):
        self.begin = begin
        self.end = end

    def __lt__(self, other: 'BaseReference'):
        return self.begin < other.begin

    def __eq__(self, other: 'BaseReference'):
        return self.begin == other.begin


class ReferenceEnd(BaseReference):
    def __init__(self, begin: int, end: int):
        super().__init__(begin, end)


class Reference(BaseReference):
    def __init__(self, begin: int, end: int, number: int, key: str, value: str, content: str):
        super().__init__(begin, end)
        self.number = number
        self.key = key
        self.value = value
        self.content = content


class AReference:
    def __init__(self, content: str, meta: dict):
        self.content = content
        self.meta = meta
        self.print = None
        self.jsref = None


class BaseModule(ABC):
    module_manager = None
    # todo: make them configurable at runtime
    reference_regex = r'\[%(.*?):(.*?)%]'
    end_reference_regex = r'\[%end%]'
    spanned_references = ["mod"]
    valid_reference_keys = ["mod", "dict", "ins"]

    @classmethod
    def set_module_manager(cls, module_manager: ModuleManager):
        cls.module_manager = module_manager

    @classmethod
    def _combine(cls, reference_list: list[BaseReference], end_reference_list: list[BaseReference]) -> list[BaseReference]:
        full_list = reference_list
        full_list.extend(end_reference_list)
        full_list.sort()
        # This entire thing below is to validate whether user somehow nested tags (references) within each other
        result = []
        current_end = -1
        for item in full_list:
            if item.begin >= current_end:
                result.append(item)
                current_end = item.end
        return result

    @classmethod
    def _match_refs(cls, ordered_list: list[BaseReference], current_id: int) -> tuple[ReferenceEnd, int]:
        # todo maybe replace it with RPN  in the future
        stacked = 0
        new_id = current_id + 1
        for item in ordered_list[new_id:]:
            if not isinstance(item, ReferenceEnd):
                stacked += 1
                new_id += 1
            else:
                if stacked > 0:
                    stacked -= 1
                    new_id += 1
                else:
                    return item, new_id
        raise RuntimeError("Spanned module without end tag match")

    @classmethod
    def _match_refs2(cls, content: str, tag_end: int):
        # todo maybe replace it with RPN  in the future
        last_pos = tag_end
        count = 0
        # todo make that less baked in
        tag_delimiter_regex = r'\[%.*?%]'
        while True:
            reg_search = re.search(tag_delimiter_regex, content[last_pos:])
            if not reg_search:
                raise RuntimeError("Spanned module without end tag match")
            if reg_search.group() == "[%end%]":
                if count > 0:
                    count -= 1
                    last_pos += reg_search.regs[0][1]
                    continue
                else:
                    return ReferenceEnd(
                        begin=reg_search.regs[0][0] + last_pos,
                        end=reg_search.regs[0][1] + last_pos
                    )
            else:
                count += 1
                last_pos += reg_search.regs[0][1]
                continue

    @classmethod
    def get_jsref_from_file(cls, node: DocumentNode):
        with open(node.path) as f:
            content = f.read()
        # get metadata from file level
        top_reference = AReference(
            content=content,
            meta=dict(node.metadata)
        )
        return BaseModule.get_jsref_from_reference(top_reference)

    @classmethod
    def get_jsref_from_reference(cls, reference: AReference):
        # read metadata
        got_meta = MetadataReader.get_metadata_from_lines([reference.content])
        if len(got_meta.metadata) > 0:
            for key, value in got_meta.metadata.items():
                reference.meta[key]: value
        reference.content = reference.content[got_meta.cursor:]
        # replace part
        reference.content = BaseModule.replace_references(reference.content)
        # match module with meta
        # todo komunikacja z modulemanager
        reference.print = Text(reference.content, reference.meta).print
        # talk with ContentManager
        # todo something like sm_response = ContentManager.register_instance(reference.print())
        sm_response = ContentManager.register_instance(reference.print())
        reference.jsref = sm_response
        return reference.jsref

    @classmethod
    def replace_references(cls, content) -> str:
        while True:
            reg_search = re.search(BaseModule.reference_regex, content)
            if not reg_search:
                break
            #
            key = reg_search.groups()[0]
            # tmp
            new_reference = (0, 0, 0, "", "", "")
            #
            if key == "mod":
                new_reference = Reference(
                    begin=reg_search.regs[0][0],
                    end=reg_search.regs[0][1],
                    number=-1,
                    key=key,
                    value=reg_search.groups()[1],
                    content=""
                )
                end_reference = BaseModule._match_refs2(content, new_reference.end)
                new_reference.content = content[new_reference.end:end_reference.begin]
                new_reference.end = end_reference.end
            if key == "ins":
                # todo
                pass
            if key == "dict":
                # todo
                pass
            #
            new_areference = AReference(
                content=new_reference.content,
                meta=dict()
            )
            jsref = BaseModule.get_jsref_from_reference(new_areference)
            content = content.replace(content[new_reference.begin:new_reference.end], jsref)
        return content
