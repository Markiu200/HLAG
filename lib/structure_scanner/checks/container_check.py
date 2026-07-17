# Own imports
from base_check import BaseCheck
from structure_scanner.document_node import DocumentNode
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue


class ContainerCheck(BaseCheck):
    """Pre dir check"""
    def check(self, node: DocumentNode):
        meta = {NodeMetadataKey.TYPE: NodeMetadataTypeValue.UNSUPPORTED}
        node.add_metadata(meta)

        return meta
