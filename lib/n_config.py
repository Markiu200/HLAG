class ConfigNamespace:
    def __init__(self, name: str, widget=None):
        self.name = name
        self.config_items: dict = dict()
        self.subscribers = []
        self.widget = widget

    def set_widget(self, widget):
        self.widget = widget

    def get_widget(self):
        return self.widget

    def get(self, key):
        return self.config_items.get(key)

    def get_items(self) -> dict:
        return self.config_items

    def get_name(self) -> str:
        return self.name

    def set(self, key, value):
        if type(value) in (str, list, tuple, int, float):
            self.config_items[key] = value
        else:
            raise TypeError(f"Config item value {type(value)} not in allowed types list")

    def subscribe_load(self, callback):
        self.subscribers.append(callback)

    def load(self, config: dict):
        self.config_items = dict(config.items())
        # On load
        for callback in self.subscribers:
            callback(self.config_items)

    def update(self, config: dict):
        for key, value in config.items():
            self.set(key, value)
        # On load
        for callback in self.subscribers:
            callback(self.config_items)


class Config:
    base_name = None

    @classmethod
    def set_base_name(cls, name: str):
        if not cls.base_name:
            cls.base_name = name

    def __init__(self):
        self.namespaces: dict[str, ConfigNamespace] = dict()
        if self.base_name:
            self.register_namespace(self.base_name)

    def register_namespace(self, namespace: str) -> ConfigNamespace | None:
        if not self.namespaces.get(namespace):
            self.namespaces[namespace] = ConfigNamespace(namespace)
            return self.namespaces.get(namespace)
        else:
            return None

    def get_base_config(self) -> ConfigNamespace | None:
        if self.base_name:
            return self.get_config(self.base_name)
        else:
            return None

    def get_config(self, namespace: str) -> ConfigNamespace | None:
        if self.namespaces.get(namespace):
            return self.namespaces.get(namespace)
        else:
            return None

    def load(self, config: dict):
        for name, namespace in config.items():
            if self.namespaces.get(name):
                self.namespaces.get(name).load(namespace)

    def update(self, config: dict):
        for name, namespace in config.items():
            if self.namespaces.get(name):
                self.namespaces.get(name).update(namespace)

    def as_serializable(self) -> dict:
        serializable = dict()
        for name, config in self.namespaces.items():
            serializable[name] = config.get_items()
        return serializable


if __name__ == '__main__':
    config_ = Config()
    print(config_)
