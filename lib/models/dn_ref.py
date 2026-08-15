class Ref:
    def __init__(self, module: str, ref_id: int):
        self.module = module
        self.ref_id = ref_id

    def as_string(self) -> str:
        return f"[&_JSREF({self.module},{self.ref_id})_&]"
