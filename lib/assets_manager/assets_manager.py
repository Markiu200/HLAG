from pathlib import PurePath
import os
import shutil
# Own imports
from config import config


class AssetsManager:
    @classmethod
    def assets_folder_exist(cls) -> bool:
        return os.path.exists(str(PurePath(config.assets_path, config.assets_dir_name)))

    @classmethod
    def initialize(cls):
        if cls.assets_folder_exist():
            # temporary commented out - better not remove anything without confirmation for now
            pass
            # with os.scandir(str(PurePath(config.assets_path, config.assets_dir_name))) as old_assets:
            #     for asset in old_assets:
            #         if os.path.isfile(asset.path):
            #             os.remove(asset.path)
        else:
            os.mkdir(str(PurePath(config.assets_path, config.assets_dir_name)))

    @classmethod
    def new_asset_name(cls, path: PurePath) -> str:
        target_path_len = len(config.target_path.parts)
        this_path_rel = path.parts[target_path_len:]
        new_name = "_".join(["", *this_path_rel])
        return new_name

    @classmethod
    def register_asset(cls, path: PurePath) -> str:
        """Copies file from path to assets directory and returns it's relative path as str.
        :param path: Path of file in directory strtucture
        :return Relative path of asset in new location"""
        new_name = cls.new_asset_name(path)
        if os.path.exists(str(PurePath(config.assets_path, config.assets_dir_name, new_name))):
            return os.path.sep.join([config.assets_dir_name, new_name])
        else:
            shutil.copy(path, str(PurePath(config.assets_path, config.assets_dir_name, new_name)))
            return os.path.sep.join([config.assets_dir_name, new_name])


if __name__ == "__main__":
    config.target_path = PurePath(r'D:\hlag_links')
    config.assets_path = PurePath(r'D:\hlag')
    config.assets_dir_name = "f_assets"
    my_path = PurePath(r'D:\hlag_links\py_tkinter\_img1.png')
    print(AssetsManager.new_asset_name(my_path))
