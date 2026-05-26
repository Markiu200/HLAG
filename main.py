import sys
import logging
from pathlib import Path
# Own imports
from models.config import Config
import gui
from lib.module_manager import ModuleManager
from lib.outline_manager import OutlineManager
from lib.structure_reader_new import StructureReader


# Start basic logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("logs.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Start module manager
modules_lib_directory = str(Path(Path.cwd(), "modules"))
mmanager = ModuleManager(modules_lib_directory)

# Read config from user input
# todo Launch part - make it launchable w/o GUI
# import argparse
config: Config = gui.start()
# assuming it is not checked at input level, do the extra directory scan
if not Path(config.target_path).exists():
    logger.error(f"Root directory of {config.target_path} does not exist!")
    raise FileExistsError("File or directory of targeted path not found")
if Path(config.target_path) == Path.cwd():
    logger.error(f"Root directory of {config.target_path} not allowed! Choose another.")
    raise IsADirectoryError(f"Root directory of {config.target_path} not allowed!")

logger.info(f"Root directory set to {config.target_path}.")

# Initialize all the managers
omanager = OutlineManager(config=config)
structure_reader = StructureReader(
    config=config,
    outline_manager=omanager
)

# Run the script
structure_reader.scan()
print(omanager.root.dom_id)
print("And so on...")
print(omanager.registered_nodes)

# folders are in navigator
#   Unless there's only one folder or none at all

# site_builder = SiteBuilder(root_directory_path=Path(config.target_path), images_as_base64=config.embed_images)

# todo Write result
# with open("output.html", "w") as file:
#     file.write(site_builder.build())
