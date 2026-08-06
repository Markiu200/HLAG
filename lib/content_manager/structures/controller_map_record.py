class ControllerMapRecord:
    def __init__(self, module: str, controller: str):
        self.module = module
        self.controller = controller

    def get_as_js_controller_map_record(self) -> str:
        return f'["{self.module}", {self.controller}]'
