from abc import ABC, abstractmethod
import re
from dataclasses import dataclass
# Own imports
from structure_scanner.document_tree.document_node import DocumentNode
from module_manager import ModuleManager


@dataclass
class Reference:
    key: str
    value: str
    content: str


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

    def __init__(self, node: DocumentNode):
        self.node = node
        self.content: str = ""
        self.reference_list: list[Reference] = []
        self.reference_counter: int = 0

    def read(self):
        with open(self.node.path) as f:
            f.seek(self.node.metadata["cursor"])
            self.content = f.read()

    def replace_references(self):
        while True:
            # todo: this thing
            reg_search = re.search(BaseModule.reference_regex, self.content)
            if not reg_search:
                break
            #
            key = reg_search.groups()[0]
            value = reg_search.groups()[1]
            if key not in BaseModule.valid_reference_keys:
                raise RuntimeError(f"Reference {key} is not registered as valid")
            #
            reference_begin = reg_search.regs[0][0]
            reference_end = reg_search.regs[0][1]
            end_reference_begin = reference_end  # if it is not spanned, this value doesn't matter
            end_reference_end = reference_end
            new_reference = Reference(
                key=key,
                value=value,
                content=""
            )
            #
            if key in BaseModule.spanned_references:
                # todo: replace it with simple re.search
                end_iter = re.finditer(BaseModule.end_reference_regex, self.content[reference_end:])
                if not end_iter:
                    raise RuntimeError("Reference not closed")
                last_end = None
                for i in end_iter:
                    last_end = i
                end_reference_begin = last_end.regs[0][0]
                end_reference_end = last_end.regs[0][1]
                new_reference.content = self.content[reference_end:end_reference_begin]
            #
            self.reference_list.append(new_reference)
            #
            self.content = self.content.replace(self.content[reference_begin:end_reference_end], f"[%{self.reference_counter}%]")
            self.reference_counter += 1

    def write(self, output: str) -> str:
        # todo: replacing references
        return output

    @abstractmethod
    def print(self):
        pass
