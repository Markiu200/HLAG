# Own imports
from module_facade import BaseCheck, DocumentNode


class ImgCheck(BaseCheck):
    def check(self, node: DocumentNode):
        meta = dict()
        if (node.path.suffix == ".jpg"
                or node.path.suffix == ".jpeg"
                or node.path.suffix == ".png"):
            meta = {"module": "raw_image_file"}
            node.add_metadata(meta)
        return meta
