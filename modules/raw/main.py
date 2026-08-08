import re
from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, Card, InstanceDBEntry
from module_management import IModule
#
from txt_check import TXTCheck
import replace_orders as rr
import read_metadata_from_file as rmff
import read_metadata_from_lines as rmfl


def get_module():
    return Raw


class Raw(IModule):
    module_path = PurePath(__file__).parent

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
        ModuleFacade.register_check(TXTCheck())

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))

    @classmethod
    def get_metadata_from_file(cls, card: Card) -> dict:
        return rmff.get_metadata_from_file(card.node.path)

    @classmethod
    def get_metadata_from_data(cls, card: Card) -> dict:
        return rmfl.read_metadata_from_lines([card.content])

    @classmethod
    def replace_orders(cls, card: Card) -> str:
        """
        :param card: -todo-
        :return: content from Data structure, but with orders replaced with jsrefs
        """
        return rr.replace_orders(card)

    @classmethod
    def parse_file(cls, card: Card) -> InstanceDBEntry:
        past_meta_location = card.node.metadata.get("cursor", 0)
        with open(card.node.path) as f:
            f.seek(past_meta_location)
            card.content = f.read()
        card.file = False
        return cls.parse_data(card)

    @classmethod
    def parse_data(cls, card: Card) -> InstanceDBEntry:
        append_brs = False if card.meta.get("autobr") == "disable" else True
        enable_html = False if card.meta.get("html") == "disable" else True
        enable_references = False if card.meta.get("references") == "disable" else True

        content = cls.replace_orders(card)

        pattern = r'\[%JSREF\(.*?\)%]'
        data_list = []
        current_data = ""
        splitted = content.splitlines()
        #
        for i in range(len(splitted)):
            # --- references ---
            if enable_references:
                current_line = splitted[i]
                jsref_found = re.search(pattern, current_line)
                if jsref_found:
                    while jsref_found:
                        parts = current_line.split(sep=jsref_found.group(), maxsplit=1)
                        # append left part (if any) to current_data and flush
                        if len(parts[0]) + len(current_data) > 0:
                            data_list.append({
                                "isRef": 0,
                                "line": "".join([current_data, parts[0]])
                            })
                        # append that find and flush
                        data_list.append({
                            "isRef": 1,
                            "line": jsref_found.group()
                        })
                        # current_data is now right side
                        current_data = parts[1]
                        # search again in what is left
                        jsref_found = re.search(pattern, current_data)
                else:
                    current_data = "".join([current_data, splitted[i]])
            else:
                # --- add line ---
                current_data = "".join([current_data, splitted[i]])
            # --- br ---
            if append_brs:
                if i != len(splitted) - 1:
                    current_data = "".join([current_data, "</br>"])
        # finish
        if len(current_data) > 0:
            data_list.append({
                "isRef": 0,
                "line": current_data
            })
        #
        result_entry = InstanceDBEntry(
            module=cls.get_info()["name"],
            data={"nodes": data_list},
            meta=card.meta
        )
        return result_entry
