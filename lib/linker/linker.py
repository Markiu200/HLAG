import ast
from pathlib import PurePath
# Own imports
from content_manager import ContentManager
from structure_scanner import StructureScanner
from models import Ref


class LinkRecord:
    def __init__(self, link: str, ref: Ref):
        self.link = link
        self.ref = ref

    def print(self):
        # ["link", {"module": "module", "instance_id": "instance_id"}]
        return "".join(['["', self.link, '", {"module": "', self.ref.module, '", "instance_id": "', str(self.ref.ref_id), '"}]'])


class Linker:
    @classmethod
    def collect_and_pair_from_scanner(cls) -> list[LinkRecord]:
        pairs = []
        for node in StructureScanner.tree:
            if node.has_attribute("directory"):
                host_path = node.metadata.get("hostPath", None)
                first_item = None
                if len(node.children) > 0:
                    first_item = node.children[0]
                if host_path and first_item:
                    pairs.append(LinkRecord(
                        link=host_path,
                        ref=first_item.ref
                    ))
        return pairs

    @classmethod
    def collect_from_content(cls) -> (dict, dict):
        instances = ContentManager.get_instance_records()
        links = dict()
        hosts = dict()
        for instance in instances:
            entry_meta = instance.instance_db_entry.meta
            if isinstance(entry_meta, str):
                try:
                    entry_meta = ast.literal_eval(entry_meta)
                except ValueError or TypeError or SyntaxError or MemoryError or RecursionError:
                    continue
            rel_path = entry_meta.get("relPath", None)
            rel_link = entry_meta.get("relLink", None)
            host_path = entry_meta.get("hostPath", None)
            if rel_path:
                links[rel_path] = host_path
            if rel_link:
                links[rel_link] = host_path
            if host_path:
                hosts[host_path] = instance
        return links, hosts

    @classmethod
    def pair(cls, links, hosts) -> list:
        pairs = []
        for link, host in links.items():
            host_for_link = hosts.get(host)
            host_ref = host_for_link.ref
            pairs.append(LinkRecord(
                link=link,
                ref=host_ref
            ))
        return pairs

    @classmethod
    def print_js(cls):
        links, hosts = cls.collect_from_content()
        content_pairs = cls.pair(links, hosts)
        directory_links = cls.collect_and_pair_from_scanner()
        all_pairs = content_pairs
        all_pairs.extend(directory_links)

        pairs_combined = ", ".join((pair.print() for pair in all_pairs))
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
