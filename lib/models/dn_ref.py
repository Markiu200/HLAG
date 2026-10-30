class Ref:
    start_tag = "[&_JSREF("
    end_tag = ")_&]"

    def __init__(self, module: str, ref_id: int):
        self.module = module
        self.ref_id = ref_id

    def __str__(self):
        return self.as_string()

    def __repr__(self):
        return self.as_string()

    def as_string(self) -> str:
        return f"{Ref.start_tag}{self.module},{self.ref_id}{Ref.end_tag}"
