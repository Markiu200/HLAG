from lib.imodule import IModule
if __name__ == '__main__':
    from sys import path as sys_path
    from pathlib import PurePath
    sys_path.append(str(PurePath(__file__).parent.parent))


class DummyPMModue(IModule):
    def __init__(self, codename: str):
        super().__init__()
        self.info = {
            "codename": codename,
            "priority": 1,
            "controller": "".join([codename, "Controller"])
        }

    def get_metadata(self, value, is_file: bool) -> dict:
        return dict()

    def parse(self, value, metadata: dict, is_file: bool) -> str:
        return f"Dummy parse result from codename {self.info.get('codename')}; value: {value}; metadata: {metadata}; is_file: {is_file}"


__all__ = [DummyPMModue]
