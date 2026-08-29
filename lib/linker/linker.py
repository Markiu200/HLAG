import ast
from pathlib import PurePath
# Own imports
from content_manager import ContentManager
from structure_scanner import StructureScanner
from models import Ref


class LinkRecord:
    def __init__(self, link: str, rel_path: str, rel_ref: Ref, host_path: str, host_ref: Ref):
        self.link = link
        self.rel_path = rel_path
        self.rel_ref = rel_ref
        self.host_path = host_path
        self.host_ref = host_ref
        #
        self.rel_ref_string = "null"
        if rel_ref:
            self.rel_ref_string = "".join(['{"module": `', self.rel_ref.module, '`, "id": ', str(self.rel_ref.ref_id), '}'])
        self.host_ref_string = "null"
        if host_ref:
            self.host_ref_string = "".join(['{"module": `', self.host_ref.module, '`, "id": ', str(self.host_ref.ref_id), '}'])

    def as_json(self):
        # ["link", {"subject": {"relPath": "relPath", "linkRef": {"module": "module", "id": id}}, "host": {"hostPath": "hostPath", "hostRef": {"module": "module", "id": id}}}]
        return "".join(['["', self.link, '", {',
                        '"subject": {"relPath": `', self.rel_path, '`, "relRef": ', self.rel_ref_string, '}, ',
                        '"host": {"hostPath": `', self.host_path, '`, "hostRef": ', self.host_ref_string, '}}]'])


class Linker:
    link_map: list[LinkRecord] = []

    @classmethod
    def pair_directories(cls):
        """"""
        for node in StructureScanner.tree:
            if node.has_attribute("directory"):
                host_path = node.metadata.get("hostPath", None)
                rel_path = node.metadata.get("relPath", None)
                rel_link = node.metadata.get("relLink", None)
                if host_path:
                    cls.link_map.append(LinkRecord(
                        link=host_path,
                        rel_path=rel_path,
                        rel_ref=node.ref,
                        host_path=host_path,
                        host_ref=node.ref
                    ))
                    if rel_link:
                        cls.link_map.append(LinkRecord(
                            link=rel_link,
                            rel_path=rel_path,
                            rel_ref=node.ref,
                            host_path=host_path,
                            host_ref=node.ref
                        ))

    @classmethod
    def pair_files(cls):
        links = dict()
        hosts = dict()
        for instance in ContentManager.get_instance_records():  # For each registered module instance (as InstanceDBRecord)
            entry_meta = instance.instance_db_entry.meta
            if isinstance(entry_meta, str):  # Try to translate str into dict, if metadata is saved as str
                try:
                    entry_meta = ast.literal_eval(entry_meta)
                except ValueError or TypeError or SyntaxError or MemoryError or RecursionError:
                    continue
            #
            host_path = entry_meta.get("hostPath", None)
            rel_path = entry_meta.get("relPath", None)
            rel_link = entry_meta.get("relLink", None)
            # All rel_links and rel_paths go to one dict, and all their hosts to another, for easier substitution later
            if rel_path:
                links[rel_path] = {"host_path": host_path, "instance": instance}
            if rel_link:
                links[rel_link] = {"host_path": host_path, "instance": instance}
            if host_path:
                hosts[host_path] = instance
            #
        for link, data in links.items():
            entry_meta = data["instance"].instance_db_entry.meta
            if isinstance(entry_meta, str):  # Try to translate str into dict, if metadata is saved as str
                try:
                    entry_meta = ast.literal_eval(entry_meta)
                except ValueError or TypeError or SyntaxError or MemoryError or RecursionError:
                    continue
            #
            host_of_link = hosts.get(data["host_path"])
            rel_path = entry_meta.get("relPath")
            if not rel_path:
                rel_path = link
            rel_ref = data["instance"].ref
            host_path = data["host_path"]
            host_ref = host_of_link.ref
            #
            cls.link_map.append(LinkRecord(
                link=link,
                rel_path=rel_path,
                rel_ref=rel_ref,
                host_path=host_path,
                host_ref=host_ref
            ))

    @classmethod
    def print_js(cls):
        cls.pair_files()
        cls.pair_directories()
        pairs_combined = ", ".join((pair.as_json() for pair in cls.link_map))
        result = "".join(['static linkMap = new Map([', pairs_combined, ']);\n'])
        #
        with open(PurePath(PurePath(__file__).parent, r"linker.js")) as f:
            lines = f.readlines()
            for line in lines:
                if "//PLACEHOLDER_FOR_LINKMAP" in line:
                    parts = line.split("//PLACEHOLDER_FOR_LINKMAP")
                    yield "".join([parts[0], result])
                else:
                    yield line
