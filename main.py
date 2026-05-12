import os

if __name__ == "__main__":
    from sys import path as syspath
    from pathlib import Path

    while "mylib" in os.getcwd():
        os.chdir("..")
    syspath.append(str(Path('./mylib/').absolute()))
    syspath.append(str(Path('./models/').absolute()))
    syspath.append(str(Path('./mylib/filetypes').absolute()))

import gui
from models.prog_args import ProgArgs
from builder import SiteBuilder

# import argparse


# todo Launch part - check for arguments
# if gui is enabled - then stop reading for other arguments and take them from GUI
# else read all the args and assess defaults
config: ProgArgs = gui.start()
if not Path(config.target_path).exists():
    raise FileExistsError("File or directory of targeted path not found")

# todo Invoke program
site_builder = SiteBuilder(root_directory_path=Path(config.target_path), images_as_base64=config.embed_images)

# todo Write result
with open("output.html", "w") as file:
    file.write(site_builder.build())
