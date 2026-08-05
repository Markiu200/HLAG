class InstanceDBEntry:
    def __init__(self, module, data, meta):
        self.module = module
        self.data = data
        self.meta = meta


if __name__ == "__main__":
    a = InstanceDBEntry("module", 12, 45)
    print(a.module, a.data, a.meta)
