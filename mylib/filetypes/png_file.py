from pathlib import Path
import re
import struct
import base64
from file import File
from node import Node


class PNGFile(File):
    def __init__(self, path: Path, parent: Node):
        super().__init__(path, parent)
        self.html_tag = ""
        self.read_dimensions = None
        self.file_dimensions = None
        #
        self.base64 = None
        self.new_html = ""

    def get_dimensions_from_html(self):
        dim_re = re.search(' width="(\d+)" height="(\d+)"', self.html_tag)
        self.read_dimensions = (int(dim_re.groups(1)[0]), int(dim_re.groups(1)[1]))

    def get_file_dimensions(self):
        # https://stackoverflow.com/questions/8032642/how-can-i-obtain-the-image-size-using-a-standard-python-class-without-using-an
        # https://www.w3.org/TR/2003/REC-PNG-20031110/#5PNG-file-signature
        with open(self.path, 'rb') as fhandle:
            head = fhandle.read(24)
            if len(head) != 24:
                return
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
            self.file_dimensions = (width, height)

    def to_base64(self):
        # https://stackoverflow.com/questions/3715493/encoding-an-image-file-with-base64
        with open(self.path, "rb") as image_file:
            self.base64 = base64.b64encode(image_file.read())

    def get_base64_img_element(self):
        # https://stackoverflow.com/questions/8499633/how-to-display-base64-images-in-html
        # https://stackoverflow.com/questions/31526085/how-to-encode-an-image-into-an-html-file
        self.to_base64()
        self.get_file_dimensions()
        self.new_html = f"<img src=\"data:image/png;base64,f{self.base64}\" width=\"{self.file_dimensions[0]}\" height=\"{self.file_dimensions[1]}\"/>"
        return self.new_html


if __name__ == "__main__":
    parent_node_path = Path("D:\\hlag\\webpage\\030_exchange")
    parent_node = Node(parent_node_path, None)
    test_png = PNGFile(Path("D:\\hlag\\webpage\\030_exchange\\img.png"), parent_node)
    test_png.html_tag = '<img src="img.png" width="200" height="300">'
    #
    test_png.get_dimensions_from_html()
    test_png.get_file_dimensions()
