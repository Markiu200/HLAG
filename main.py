# Built-in imports
# import argparse
import sys
import logging
from pathlib import Path

# Own imports
import gui
import lib.module_manager
from models.prog_args import ProgArgs


# Start basic logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("logs.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Start module manager
modules_lib_directory = str(Path(Path.cwd(), "modules"))
mmanager = lib.module_manager.ModuleManager(modules_lib_directory)


# todo Launch part - make it launchable w/o GUI
# if gui is enabled - then stop reading for other arguments and take them from GUI
# else read all the args and assess defaults
config: ProgArgs = gui.start()
if not Path(config.target_path).exists():
    raise FileExistsError("File or directory of targeted path not found")

# todo Read structure
# ignore oos_ nodes
# folders are in navigator
#   Unless there's only one folder or none at all



print("And so on...")
# site_builder = SiteBuilder(root_directory_path=Path(config.target_path), images_as_base64=config.embed_images)

# todo Write result
# with open("output.html", "w") as file:
#     file.write(site_builder.build())
