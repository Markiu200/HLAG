from pathlib import PurePath


class SerializeResponse:
    def __init__(self, state, exceptions):
        self.state = state
        self.exceptions = exceptions


class ConfigItem:
    def __init__(self, key: str, default=None):
        self.key = key
        self.value = default
        self.default = default

    def set(self, value):
        self.value = value

    def get(self):
        return self.value


class PathConfigItem(ConfigItem):
    def __init__(self, key: str, default=None):
        super().__init__(key, default)

    def set(self, value):
        if isinstance(value, str):
            self.value = PurePath(value)
        else:
            self.value = value

    def get(self) -> PurePath:
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

    def add_path_config_item(self, key, default=None):
        if not self.config_items.get(key):
            self.config_items[key] = PathConfigItem(key, default)

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

    def serialize(self):
        exception_list = []
        state = dict()
        for config_ns in (*self.namespaces.values(), self.base_config):
            ns_name = config_ns.namespace
            state[ns_name] = []
            for config_item in config_ns.config_items.values():
                key = config_item.key
                value = config_item.value
                if isinstance(value, str) or isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
                    state[ns_name].append((key, value))
                elif isinstance(value, PurePath):
                    state[ns_name].append((key, str(value)))
                else:
                    exception_list.append(key)
        return SerializeResponse(state, exception_list)

    def deserialize_update(self, state):
        exception_list = []
        if state:
            for loaded_state_ns_name, data in state.items():
                if loaded_state_ns_name in (*self.namespaces.keys(), self.base_config_ns):
                    config_ns = self.get_config(loaded_state_ns_name)
                    for config_item in data:
                        try:
                            config_ns.set(config_item[0], config_item[1])
                        except Exception as e:
                            exception_list.append((config_item[0], config_item[1]))
        return exception_list


if __name__ == '__main__':
    config = Config()
    print(config)
