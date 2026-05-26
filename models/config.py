from pathlib import PurePath
from dataclasses import dataclass
from logging import Logger


@ dataclass
class Config:
    target_path: PurePath
    embed_images: bool
    base_path_length: int
    logger: Logger | None


config = Config(PurePath(), False, 0, None)
