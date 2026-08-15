from pathlib import PurePath
import xml.etree.ElementTree as ElementTree
import re
# Own imports
from module_facade import ModuleFacade, Card, InstanceDBEntry
from module_management import IModule


def get_module_main_class():
    return CodeCopy


class Code:
    def __init__(self, code: list):
        self.code: list = code

    def print_for_data_entry(self) -> str:
        result = '['
        #
        mid_list = []
        for part in self.code:
            if isinstance(part, int):
                mid_list.append(str(part))
            else:
                mid_list.append(IModule.json_sanitize(part))
        mid_string = ", ".join(mid_list)
        #
        result = "".join([result, mid_string, ']'])
        return result


class CodeVariables:
    def __init__(self, variables: list[dict]):
        self.variables: list[dict] = variables

    def print_for_data_entry(self) -> str:
        if len(self.variables) > 0:
            listed_vars = []
            for var in self.variables:
                prepared_default = IModule.json_sanitize(var.get("default"))
                if prepared_default == "null":
                    prepared_default = IModule.json_sanitize(f'<{var.get("variable")}>')
                one_var = "".join([
                    '[', str(var.get("position")), ', ',
                    '{"variable": ', IModule.json_sanitize(var.get("variable")),
                    ', "default": ', prepared_default, '}]'])
                listed_vars.append(one_var)
            result_mid = ", ".join(listed_vars)
            result = "".join(['new Map([', result_mid, '])'])
            return result
        else:
            return "null"


class CodeItem:
    def __init__(self, code: Code, variables: CodeVariables):
        self.code: Code = code
        self.variables: CodeVariables = variables

    def print_record(self) -> str:
        result = "".join([
            '{"code": ',
            self.code.print_for_data_entry(),
            ', "variables": ',
            self.variables.print_for_data_entry(),
            '}'
        ])
        return result


class CodeCopy(IModule):
    module_path = PurePath(__file__).parent

    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "code_copy",
            "priority": 1,
            "dependencies": [],
            "controller": "CodeCopyModuleController"
        }

    @classmethod
    def register_checks(cls):
        pass

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))

    @classmethod
    def get_metadata_from_file(cls, card: Card) -> dict:
        return ModuleFacade.get_module("raw").get_metadata_from_file(card)

    @classmethod
    def get_metadata_from_data(cls, card: Card) -> dict:
        return ModuleFacade.get_module("raw").get_metadata_from_data(card)

    @classmethod
    def parse_file(cls, card: Card) -> InstanceDBEntry:
        return ModuleFacade.get_module("raw").parse_data(card)

    @classmethod
    def parse_data_internal(cls, card: Card) -> dict:
        root = ElementTree.fromstring(card.content)

        xml_code_items = root.findall("codeItem")
        code_item_list: list[CodeItem] = []
        for xml_code_item in xml_code_items:

            # Variables
            variables = []
            position = 0
            for variable in xml_code_item.findall("variable"):
                variables.append({
                    "position": position,
                    "variable": variable.text,
                    "default": variable.get("default")
                })
                position += 1
            variables_object = CodeVariables(variables)

            # Code
            re_pattern_mid = "|".join([re.escape(v["variable"]) for v in variables])
            re_pattern = rf"({re_pattern_mid})"
            #
            code = xml_code_item.find("code")
            if code is None:
                continue
            code_split = re.split(re_pattern, code.text)
            #
            for i, part in enumerate(code_split):
                for variable in variables:
                    if str(part).startswith(variable["variable"]):
                        code_split[i] = variable["position"]
                        break
            code_split[:] = [item for item in code_split if item != '']
            #
            code_object = Code(code_split)

            # Append ready item
            code_item_list.append(CodeItem(
                code=code_object,
                variables=variables_object
            ))
        return {
            "module": cls.get_info()["name"],
            "data": code_item_list,
            "meta": card.meta
        }

    @classmethod
    def parse_data(cls, card: Card) -> InstanceDBEntry:
        internal_data = cls.parse_data_internal(card)
        #
        proper_mid = ", ".join([i.print_record() for i in internal_data["data"]])
        proper_data = "".join(['{"codeList": [', proper_mid, ']}'])
        #
        return InstanceDBEntry(
            module=internal_data["module"],
            data=proper_data,
            meta=internal_data["meta"]
        )
