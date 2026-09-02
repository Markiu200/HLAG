from pathlib import PurePath


class ConfigItem:
    def __init__(self, key: str, default=None, widget=None):
        self.key = key
        self.value = default
        self.default = default
        self.widget = widget


class BaseConfigNamespace:
    def __init__(self):
        self.config_items: dict[str, ConfigItem] = dict()

    def add_config_item(self, key, default=None):
        if not self.config_items.get(key):
            self.config_items[key] = ConfigItem(key, default)

    def get(self, key):
        if self.config_items.get(key):
            return self.config_items.get(key).value
        else:
            return None

    def set(self, key, value):
        if key in self.config_items:
            self.config_items.get(key).value = value
        else:
            raise RuntimeError(f"{key} is not a config item in base config")


class ConfigNamespace(BaseConfigNamespace):
    def __init__(self, namespace: str):
        super().__init__()
        self.namespace = namespace

    def get(self, key):
        if self.config_items.get(key):
            return self.config_items.get(key).value
        else:
            raise RuntimeError(f"{key} is not a config item in {self.namespace} config")


class Config:
    def __init__(self):
        self.namespaces: dict[str, ConfigNamespace] = dict()
        self.base_config = BaseConfigNamespace()

    def register_namespace(self, namespace: str) -> ConfigNamespace | None:
        if not self.namespaces.get(namespace):
            self.namespaces[namespace] = ConfigNamespace(namespace)
            return self.namespaces.get(namespace)
        else:
            return None

    def get_base_config(self):
        return self.base_config

    def get_config(self, namespace: str) -> ConfigNamespace | None:
        if self.namespaces.get(namespace):
            return self.namespaces.get(namespace)
        else:
            return None


if __name__ == '__main__':
    config = Config()
    print(config)
