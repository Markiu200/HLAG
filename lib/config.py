from pathlib import PurePath
from dataclasses import dataclass
from logging import Logger


@ dataclass
class Config:
    target_path: PurePath
    output_path: PurePath
    assets_path: PurePath
    modules_path: PurePath
    output_name: str
    document_title: str
    embed_images: bool
    base_path_length: int
    logger: Logger | None


config = Config(PurePath(), PurePath(), PurePath(), PurePath(), "", "", False, 0, None)
