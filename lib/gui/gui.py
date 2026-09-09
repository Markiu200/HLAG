import tkinter as tk
from tkinter import ttk
from pathlib import PurePath
import json
# Own imports
from lib.n_config import Config
from lib.print_logger import PrintLogger


class UserGUI:
    def __init__(self, config: Config):
        self.config = config
        self.logger = self.config.get_base_config().get("logger")
        self.module_path = PurePath(__file__).parent
        self.default_saved_projects_path = PurePath(self.module_path.parent.parent, 'saved_projects')
        if self.config.get_base_config().get("base_path"):
            self.last_state_path = PurePath(self.config.get_base_config().get("base_path"), "last_state.dat")
        else:
            self.last_state_path = PurePath(self.module_path, "last_state.dat")
        #
        self.config_widgets = []
        self.last_state = dict()

    def add_config_widget(self, widget):
        self.config_widgets.append(widget)

    def start(self):
        root = tk.Tk()
        root.title('Pagemaker')

        # Menubar
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label='Save Project', command=save_project)
        file_menu.add_command(label='Load Project', command=load_project)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=root.destroy)
        menubar.add_cascade(label='File', menu=file_menu, underline=0)
        #
        root.config(menu=menubar)

        # Containers
        button_frame = ttk.Frame(root)
        button_frame.pack(side=tk.LEFT, pady=10, ipadx=10, expand=True, fill=tk.Y)
        options_frame = ttk.Frame(root)
        options_frame.pack(side=tk.LEFT, pady=5, expand=True, fill=tk.X)

        # Buttons
        run_button = ttk.Button(button_frame, text="Run", width=10)
        run_button.pack(side=tk.TOP)
        temp_save = ttk.Button(button_frame, text="TMP save", width=10, command=self.save_last)
        temp_save.pack(side=tk.TOP)

        # Pack all config widgets
        for widget in self.config_widgets:
            config_widget = widget(options_frame, self.config)
            config_widget.pack(side=tk.TOP, expand=True, fill=tk.X, padx=10, pady=10, ipadx=10, ipady=5)

        # Running
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        finally:
            root.mainloop()

    def save_last(self):
        # Collect all ConfigNamespaces
        all_namespaces = [self.config.get_base_config()]
        for config_ns_ in self.config.namespaces.values():
            all_namespaces.append(config_ns_)
        # Iterate over them and save eligible values
        for config_ns in all_namespaces:
            ns_name = config_ns.namespace
            self.last_state[ns_name] = []
            for config_item in config_ns.config_items.values():
                key = config_item.key
                value = config_item.value
                if isinstance(value, str) or isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
                    print("saved: ", ns_name, key, value)
                    self.last_state[ns_name].append((key, value))
                elif isinstance(value, PurePath):
                    print("saved: ", ns_name, key, str(value))
                    self.last_state[ns_name].append((key, str(value)))
                else:
                    print(f"{key} not eligible for last state")
        # Save to file
        try:
            with open(self.last_state_path, "wb") as f:
                f.write(json.dumps(self.last_state).encode('utf-8'))
        except Exception as e:
            if self.logger:
                self.logger.error(f"An error {e} occurred while attempting to save state - state not saved")
        print("saved")


def load_last():
    pass


def save_project():
    pass


def load_project():
    pass


if __name__ == "__main__":
    logger = PrintLogger()

    config_ = Config()
    base_config = config_.base_config
    base_path = PurePath(__file__).parent.parent.parent
    base_config.add_config_item("base_path", base_path)
    base_config.add_config_item("target_path", PurePath(base_path, "inputs"))
    base_config.add_config_item("output_path", PurePath(base_path, "outputs"))
    base_config.add_config_item("assets_path", PurePath(base_path, "outputs"))
    base_config.add_config_item("modules_path", PurePath(base_path, "modules"))
    base_config.add_config_item("assets_dir_name", "assets")
    base_config.add_config_item("output_name", "output.html")
    base_config.add_config_item("output_title", "GUI")
    base_config.add_config_item("logger", logger)
    base_config.add_config_item("logger_level", 20)

    gui_ = UserGUI(config_)
    gui_.start()

    print(config_)
