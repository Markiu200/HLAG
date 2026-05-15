from pathlib import Path
import gui
from models.prog_args import ProgArgs
from builder import SiteBuilder

import sys, os
import importlib

modules_lib_directory = str(Path(Path.cwd(), "modules"))
sys.path.append(modules_lib_directory)
print(modules_lib_directory)

modules_directory_list = [f.name for f in os.scandir(modules_lib_directory) if f.is_dir() and not f.name.startswith("_")]
modules_lib = []

for module in modules_directory_list:
    modules_lib.append((module, importlib.import_module(f"{module}.main", modules_lib_directory)))

# simple = importlib.import_module("fancy_article.fancy_world", modules_lib_directory)
# simple.fancy_article()

for module in modules_lib:
    module[1].main()

# import argparse


# todo Launch part - check for arguments
# if gui is enabled - then stop reading for other arguments and take them from GUI
# else read all the args and assess defaults
config: ProgArgs = gui.start()
if not Path(config.target_path).exists():
    raise FileExistsError("File or directory of targeted path not found")

# todo Invoke program
print("And so on...")
# site_builder = SiteBuilder(root_directory_path=Path(config.target_path), images_as_base64=config.embed_images)

# todo Write result
# with open("output.html", "w") as file:
#     file.write(site_builder.build())
