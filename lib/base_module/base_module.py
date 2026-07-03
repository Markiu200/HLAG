from abc import ABC, abstractmethod
import re
from dataclasses import dataclass
# Own imports
from structure_scanner.document_tree.document_node import DocumentNode
from module_manager import ModuleManager


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
    def __init__(self, begin: int, end: int, key: str, value: str, content: str):
        super().__init__(begin, end)
        self.key = key
        self.value = value
        self.content = content


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
    def _match_refs(cls, ordered_list: list[BaseReference], reference: Reference, current_id: int) -> tuple[ReferenceEnd, int]:
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

    def __init__(self, node: DocumentNode):
        self.node = node
        self.content: str = ""
        self.reference_list: list[Reference] = []

    def read(self):
        with open(self.node.path) as f:
            f.seek(self.node.metadata["cursor"])
            self.content = f.read()

    def replace_references(self):
        ref_list = []
        for item in re.finditer(BaseModule.reference_regex, self.content):
            ref_list.append(
                Reference(
                    begin=item.regs[0][0],
                    end=item.regs[0][1],
                    key=item.groups()[0],
                    value=item.groups()[1],
                    content=""
                )
            )
        end_ref_list = []
        for item in re.finditer(BaseModule.end_reference_regex, self.content):
            end_ref_list.append(
                ReferenceEnd(
                    begin=item.regs[0][0],
                    end=item.regs[0][1]
                )
            )
        final_list = BaseModule._combine(ref_list, end_ref_list)
        #
        resolve_id = 0
        for id_, item in enumerate(final_list):
            if id_ < resolve_id:
                continue
            resolve_id += 1
            if isinstance(item, Reference):
                if item.key in BaseModule.spanned_references:
                    res = BaseModule._match_refs(final_list, item, id_)
                    # todo: this
                    resolve_id = res[1]
                    item.content = self.content[item.end:res[0].begin]
                    item.end = res[0].end
                    self.reference_list.append(item)
                else:
                    self.reference_list.append(item)
        #
        reference_counter = len(self.reference_list) - 1
        for reference in reversed(self.reference_list):
            self.content = self.content.replace(self.content[reference.begin:reference.end], f"[%{reference_counter}%]", 1)
            reference_counter -= 1

    def write(self, output: str) -> str:
        # todo: replacing references
        return output

    @abstractmethod
    def print(self):
        pass
