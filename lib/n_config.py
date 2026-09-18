from pathlib import PurePath
import json


# class SerializeResponse:
#     def __init__(self, state, exceptions):
#         self.state = state
#         self.exceptions = exceptions
#
#
# class ConfigItem:
#     def __init__(self, key: str, default=None):
#         self.key = key
#         self.value = default
#         self.default = default
#
#     def set(self, value):
#         self.value = value
#
#     def get(self):
#         return self.value
#
#     def get_serialized(self):
#         try:
#             json.dumps(self.value)
#             return self.value
#         except TypeError as e:
#             raise e
#
#
# class PathConfigItem(ConfigItem):
#     def __init__(self, key: str, default=None):
#         super().__init__(key, default)
#
#     def set(self, value):
#         if isinstance(value, str):
#             self.value = PurePath(value)
#         else:
#             self.value = value
#
#     def get(self) -> PurePath:
#         return self.value
#
#     def get_serialized(self):
#         return str(self.value)
#
#
# class ListConfigItem(ConfigItem):
#     def __init__(self, key: str, default=None):
#         if default is None:
#             super().__init__(key, [])
#         else:
#             super().__init__(key, default)
#
#     def set(self, value):
#         if isinstance(value, str):
#             self.value = list(json.loads(value))
#         elif isinstance(value, list):
#             self.value = value
#         else:
#             raise TypeError("Attempt to set ListConfigItem to something else than a list")
#
#     def get(self) -> list:
#         return self.value
#
#     def get_serialized(self):
#         return json.dumps(self.value)


class ConfigNamespace:
    # def __init__(self, name: str, subscribers, widget=None):
    def __init__(self, name: str, widget=None):
        self.name = name
        # self.config_items: dict[str, ConfigItem] = dict()
        self.config_items: dict = dict()
        self.subscribers = []
        self.widget = widget

    def set_widget(self, widget):
        self.widget = widget

    def get_widget(self):
        return self.widget

    # def add_config_item(self, key, default=None):
    #     if not self.config_items.get(key):
    #         self.config_items[key] = ConfigItem(key, default)
    #
    # def add_path_config_item(self, key, default=None):
    #     if not self.config_items.get(key):
    #         self.config_items[key] = PathConfigItem(key, default)
    #
    # def add_list_config_item(self, key, default=None):
    #     if not self.config_items.get(key):
    #         self.config_items[key] = ListConfigItem(key, default)

    def get(self, key):
        # if self.config_items.get(key):
        #     return self.config_items.get(key).get()
        # else:
        #     return None
        return self.config_items.get(key)

    def get_items(self) -> dict:
        return self.config_items

    def get_name(self) -> str:
        return self.name

    # def get_default(self, key):
    #     if self.config_items.get(key):
    #         return self.config_items.get(key).default
    #     else:
    #         return None

    # def set(self, key, value, propagate: bool = True):
    def set(self, key, value):
        if type(value) in (str, list, tuple, int, float):
            self.config_items[key] = value
        else:
            raise TypeError(f"Config item value {type(value)} not in allowed types list")
        # for config_item in config_ns.config_items.values():
        #     key = config_item.key
            # value = config_item.value
            # if isinstance(value, str) or isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
            #     state[ns_name].append((key, value))
            # elif isinstance(value, PurePath):
            #     state[ns_name].append((key, str(value)))
            # else:
            #     exception_list.append(key)
        #     try:
        #         state[ns_name].append((key, config_item.get_serialized()))
        #     except TypeError:
        #         exception_list.append(key)
        # return SerializeResponse(state, exception_list)
        # if key in self.config_items:
        #     self.config_items.get(key).set(value)
        #     if propagate:
        #         for callback in self.subscribers:
        #             callback(self.namespace, key, value)
        # else:
        #     raise RuntimeError(f"{key} is not a config item in base config")

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
        # self.subscribers: callable = []
        # self.base_config_ns = "base_config"
        if self.base_name:
            self.register_namespace(self.base_name)
        # self.base_config = ConfigNamespace(self.base_config_ns, self.subscribers)

    def register_namespace(self, namespace: str) -> ConfigNamespace | None:
        # if not self.namespaces.get(namespace) and namespace != self.base_config_ns:
        if not self.namespaces.get(namespace):
            # self.namespaces[namespace] = ConfigNamespace(namespace, self.subscribers)
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

    # def subscribe(self, callback):
    #     self.subscribers.append(callback)

    # def serialize(self):
    #     exception_list = []
    #     state = dict()
    #     for config_ns in (*self.namespaces.values(), self.base_config):
    #         ns_name = config_ns.namespace
    #         state[ns_name] = []
    #         for config_item in config_ns.config_items.values():
    #             key = config_item.key
    #             # value = config_item.value
    #             # if isinstance(value, str) or isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
    #             #     state[ns_name].append((key, value))
    #             # elif isinstance(value, PurePath):
    #             #     state[ns_name].append((key, str(value)))
    #             # else:
    #             #     exception_list.append(key)
    #             try:
    #                 state[ns_name].append((key, config_item.get_serialized()))
    #             except TypeError:
    #                 exception_list.append(key)
    #     return SerializeResponse(state, exception_list)
    #
    # def deserialize_update(self, state):
    #     exception_list = []
    #     if state:
    #         for loaded_state_ns_name, data in state.items():
    #             if loaded_state_ns_name in (*self.namespaces.keys(), self.base_config_ns):
    #                 config_ns = self.get_config(loaded_state_ns_name)
    #                 for config_item in data:
    #                     try:
    #                         config_ns.set(config_item[0], config_item[1])
    #                     except Exception as e:
    #                         exception_list.append((config_item[0], config_item[1]))
    #     return exception_list


if __name__ == '__main__':
    config_ = Config()
    print(config_)
