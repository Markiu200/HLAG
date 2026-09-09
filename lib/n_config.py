class ConfigItem:
    def __init__(self, key: str, default=None):
        self.key = key
        self.value = default
        self.default = default

    def set(self, value):
        self.value = value

    def get(self):
        return self.value


class ConfigNamespace:
    def __init__(self, namespace: str, subscribers, widget=None):
        self.namespace = namespace
        self.config_items: dict[str, ConfigItem] = dict()
        self.subscribers = subscribers
        self.widget = widget

    def set_widget(self, widget):
        self.widget = widget

    def get_widget(self):
        return self.widget

    def add_config_item(self, key, default=None):
        if not self.config_items.get(key):
            self.config_items[key] = ConfigItem(key, default)

    def get(self, key):
        if self.config_items.get(key):
            return self.config_items.get(key).get()
        else:
            return None

    def get_default(self, key):
        if self.config_items.get(key):
            return self.config_items.get(key).default
        else:
            return None

    def set(self, key, value, propagate: bool = True):
        if key in self.config_items:
            self.config_items.get(key).set(value)
            if propagate:
                for callback in self.subscribers:
                    callback(self.namespace, key, value)
        else:
            raise RuntimeError(f"{key} is not a config item in base config")


class Config:
    def __init__(self):
        self.namespaces: dict[str, ConfigNamespace] = dict()
        self.subscribers: callable = []
        self.base_config_ns = "base_config"
        self.base_config = ConfigNamespace(self.base_config_ns, self.subscribers)

    def register_namespace(self, namespace: str) -> ConfigNamespace | None:
        if not self.namespaces.get(namespace) and namespace != self.base_config_ns:
            self.namespaces[namespace] = ConfigNamespace(namespace, self.subscribers)
            return self.namespaces.get(namespace)
        else:
            return None

    def get_base_config(self):
        return self.base_config

    def get_config(self, namespace: str) -> ConfigNamespace | None:
        if self.namespaces.get(namespace):
            return self.namespaces.get(namespace)
        elif namespace == self.base_config_ns:
            return self.base_config
        else:
            return None

    def subscribe(self, callback):
        self.subscribers.append(callback)


if __name__ == '__main__':
    config = Config()
    print(config)
