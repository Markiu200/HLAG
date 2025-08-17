import re
from pathlib import Path
from file import File
from node import Node
from png_file import PNGFile


class HTMLFile(File):
    def __init__(self, path: Path, parent: Node, images_to_base64 = True):
        super().__init__(path, parent)
        self.images_to_base64 = images_to_base64

    def to_string(self) -> str:
        """For HTML files, only return contents of &lt;body&gt; as is, but as &lt;section&gt."""
        result = ""
        save_flag = False
        with open(self.path) as f:
            for line in f:
                if "<body>" in line:
                    save_flag = True
                    continue
                if "</body>" in line:
                    break
                if save_flag:
                    result += self.parse_line(line)
        return result

    def parse_line(self, line):
        if re.match("^ *<img ", line):
            if self.images_to_base64:
                image_file = self.get_corresponding_image_file(line)
                return image_file.get_base64_img_element()
            else:
                return line
        else:
            return line

    def get_corresponding_image_file(self, line) -> PNGFile:
        for node in self.parent.children:
            if str(node.path).endswith(self.get_src(line)):
                return node

    def get_src(self, line) -> str:
        # https://stackoverflow.com/questions/766372/python-non-greedy-regexes
        src_re = re.search('src="(.*?)"', line)
        return src_re.groups(1)[0]
