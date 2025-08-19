import os
import shutil
from pathlib import Path
from filetypes.png_file import PNGFile


class ImagesFolder:
    def __init__(self, folder_path: Path):
        self.folder_path = folder_path
        self.registered_images = []

    def check_if_images_folder_exist(self) -> bool:
        return os.path.exists(self.folder_path)

    def get_new_path(self, image: PNGFile) -> Path:
        return self.folder_path / image.src

    def check_if_image_already_in_folder(self, image: PNGFile) -> bool:
        return os.path.exists(self.get_new_path(image))

    def copy_image_to_folder(self, image: PNGFile):
        # https://stackoverflow.com/questions/123198/how-do-i-copy-a-file
        if not self.check_if_image_already_in_folder(image):
            shutil.copy(self.get_new_path(image), self.folder_path)

    def copy_images_to_folder(self):
        if not self.check_if_images_folder_exist():
            raise FileNotFoundError(f"Images directory '{self.folder_path}' is not found.")
        for image in self.registered_images:
            self.copy_image_to_folder(image)
