from pathlib import PurePath
import os
import shutil
# Own imports
from base_assets_manager import BaseAssetsManager
from n_config import Config


class AssetsManager(BaseAssetsManager):
    def __init__(self, config: Config):
        self.config = config
        self.assets_dir_path = PurePath(
                config.get_base_config().get("assets_path"),
                config.get_base_config().get("assets_dir_name")
        )
        self.registered_assets = []
        self.logger = self.config.get_base_config().get("logger")

    def assets_folder_exist(self) -> bool:
        return os.path.exists(str(PurePath(
            self.config.get_base_config().get("assets_path"),
            self.config.get_base_config().get("assets_dir_name")
        )))

    def initialize(self):
        if not self.assets_folder_exist():
            os.mkdir(str(self.assets_dir_path))
            if self.logger:
                self.logger.info(f"Assets folder {self.assets_dir_path} has been created")

    def new_asset_name(self, path: PurePath) -> str:
        target_path_len = len(self.config.base_config.get("target_path").parts)
        this_path_rel = path.parts[target_path_len:]
        new_name = "_".join(["", *this_path_rel])
        return new_name

    def register_asset(self, path: PurePath) -> str | None:
        """Copies file from path to assets directory and returns it's relative path as str.
        :param path: Path of file in directory strtucture
        :return Relative path of asset in new location, or None if file already exists"""
        new_name = self.new_asset_name(path)
        if os.path.exists(str(PurePath(self.assets_dir_path, new_name))):
            if self.logger:
                self.logger.info(f"Asset {new_name} already exisits - skipping")
            return None
        else:
            self.registered_assets.append((path, str(PurePath(self.assets_dir_path, new_name))))
            return os.path.sep.join([self.config.get_base_config().get("assets_dir_name"), new_name])

    def copy_assets(self):
        for asset in self.registered_assets:
            try:
                shutil.copy(asset[0], asset[1])
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error while copying {asset[0]} to {asset[1]}, skipping copy - dependent resource in output file will not work!\n{e}")


if __name__ == "__main__":
    config_ = Config()
    base_config = config_.get_base_config()
    base_config.add_config_item("target_path", PurePath(r'D:\hlag_links\py_tkinter'))
    base_config.add_config_item("output_path", PurePath(PurePath(__file__).parent.parent.parent, r'outputs'))
    base_config.add_config_item("assets_path", PurePath(PurePath(__file__).parent.parent.parent, r'outputs'))
    base_config.add_config_item("modules_path", PurePath(PurePath(__file__).parent.parent.parent, "modules"))
    base_config.add_config_item("assets_dir_name", "assets")
    base_config.add_config_item("output_name", "output.html")
    base_config.add_config_item("output_title", "AssetsManager")
    base_config.add_config_item("logger", None)

    my_path = PurePath(r'D:\hlag_links\py_tkinter\_img1.png')

    assets_manager = AssetsManager(config=config_)
    print(assets_manager.new_asset_name(my_path))
    assets_manager.copy_assets()
