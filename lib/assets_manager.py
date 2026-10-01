import os
import shutil
import logging
from pathlib import PurePath
# Own imports
if __name__ == '__main__':
    from sys import path as sys_path
    sys_path.append(str(PurePath(__file__).parent.parent))
from lib.i_assets_manager import IAssetsManager


class AssetsManager(IAssetsManager):
    def __init__(self, assets_dir_name: str, input_dir_path: PurePath, output_dir_path: PurePath, logger_name: str = None):
        self.assets_dir_name = assets_dir_name
        self.input_dir_path = input_dir_path
        self.output_dir_path = output_dir_path
        self.assets_dir_path = PurePath(self.output_dir_path, self.assets_dir_name)
        self.registered_assets = []
        self.logger = None
        if logger_name:
            self.logger = logging.getLogger(logger_name)

    def assets_directory_exist(self) -> bool:
        return os.path.exists(str(self.assets_dir_path))

    def get_new_asset_name(self, path: PurePath) -> str:
        target_path_len = len(self.input_dir_path.parts)
        this_path_rel = path.parts[target_path_len:]
        new_name = "_".join(["", *this_path_rel])
        return new_name

    def register_asset(self, path: PurePath) -> str | None:
        """Copies file from path to assets directory and returns it's relative path as str.
        :param path: Path of file in input directory structure
        :return Relative path of asset in new location, or None if file already exists"""
        new_name = self.get_new_asset_name(path)
        if os.path.exists(str(PurePath(self.assets_dir_path, new_name))):
            if self.logger:
                self.logger.info(f"Asset {new_name} already exisits - skipping")
            return None
        else:
            self.registered_assets.append((path, str(PurePath(self.assets_dir_path, new_name))))
            return os.path.sep.join([self.assets_dir_path, new_name])

    def copy_assets(self):
        if len(self.registered_assets) > 0:
            if not self.assets_directory_exist():
                os.mkdir(str(self.assets_dir_path))
                if self.logger:
                    self.logger.info(f"Assets folder {self.assets_dir_path} has been created")
            #
            for asset in self.registered_assets:
                try:
                    shutil.copy(asset[0], asset[1])
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Error while copying {asset[0]} to {asset[1]}, skipping copy - dependent resource in output file will not work!\n{e}")


if __name__ == "__main__":
    base_path_ = PurePath(__file__).parent
    input_dir_path_ = PurePath(base_path_, "inputs")
    output_dir_path_ = PurePath(base_path_, "outputs")
    image_path_ = PurePath(input_dir_path_, "some_directory", "my_image.png")
    #
    assets_manager = AssetsManager(
        assets_dir_name="assets",
        input_dir_path=input_dir_path_,
        output_dir_path=output_dir_path_
    )
    print(assets_manager.get_new_asset_name(image_path_))
