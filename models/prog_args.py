from pathlib import PurePath


class ProgArgs:
    def __init__(self,
                 target_path: str | PurePath = None,
                 embed_images: bool = False
                 ):
        self.embed_images = embed_images
        self.target_path = target_path

    def __str__(self):
        return f"target_path:{self.target_path}; embed_images:{self.embed_images}"
