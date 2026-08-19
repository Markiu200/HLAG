import ast
# Own imports
from content_manager import ContentManager
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
    def fetch_content_from_scanner(cls) -> (dict, dict):
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
        links, hosts = cls.fetch_content_from_scanner()
        pairs = cls.pair(links, hosts)
        pairs_combined = ", ".join((pair.print() for pair in pairs))
        result = "".join(['static linkMap = new Map([', pairs_combined, ']);'])
        yield ""
