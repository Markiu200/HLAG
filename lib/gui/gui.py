import tkinter as tk
from tkinter import ttk,filedialog
from pathlib import PurePath
import json
import os
# Own imports
from lib.n_config import Config
from lib.print_logger import PrintLogger


class UserGUI:
    def __init__(self, config: Config):
        # Setup properties
        self.config = config
        self.logger = self.config.get_base_config().get("logger")
        self.module_path = PurePath(__file__).parent
        if self.config.get_base_config().get("base_path"):
            self.default_saved_projects_path = PurePath(self.config.get_base_config().get("base_path"), "saved_projects")
        else:
            self.default_saved_projects_path = PurePath(self.module_path, "saved_projects")
        if self.config.get_base_config().get("base_path"):
            self.last_state_path = PurePath(self.config.get_base_config().get("base_path"), "last_state.dat")
        else:
            self.last_state_path = PurePath(self.module_path, "last_state.dat")
        #
        self.config_widgets = []
        self.config_namespaces_names = [self.config.get_base_config().namespace]
        for config_ns_ in self.config.namespaces.values():
            self.config_namespaces_names.append(config_ns_.namespace)
        self.last_state = dict()
        # Setup tk widgets
        self.root = tk.Tk()
        self.root.title('Pagemaker')
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def add_config_widget(self, widget):
        self.config_widgets.append(widget)

    def start(self):
        # Menubar
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label='Save Project', command=self.save_project)
        file_menu.add_command(label='Load Project', command=self.load_project)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.on_exit)
        menubar.add_cascade(label='File', menu=file_menu, underline=0)
        #
        self.root.config(menu=menubar)

        # Containers
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=tk.LEFT, pady=10, ipadx=10, expand=True, fill=tk.Y)
        options_frame = ttk.Frame(self.root)
        options_frame.pack(side=tk.LEFT, pady=5, expand=True, fill=tk.X)

        # Buttons
        run_button = ttk.Button(button_frame, text="Run", width=10)
        run_button.pack(side=tk.TOP)
        temp_save = ttk.Button(button_frame, text="TMP save", width=10, command=self.save_last)
        temp_save.pack(side=tk.TOP)
        temp_load = ttk.Button(button_frame, text="TMP load", width=10, command=self.load_last)
        temp_load.pack(side=tk.TOP)

        # Pack all config widgets
        for widget in self.config_widgets:
            config_widget = widget(options_frame, self.config)
            config_widget.pack(side=tk.TOP, expand=True, fill=tk.X, padx=10, pady=10, ipadx=10, ipady=5)

        # Load last state
        self.load_last()

        # Running
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        finally:
            self.root.mainloop()

    def save_state(self):
        # Collect all ConfigNamespaces
        all_namespaces = []
        for config_ns in self.config_namespaces_names:
            all_namespaces.append(self.config.get_config(config_ns))
        # Iterate over them and save eligible values
        for config_ns in all_namespaces:
            ns_name = config_ns.namespace
            self.last_state[ns_name] = []
            for config_item in config_ns.config_items.values():
                key = config_item.key
                value = config_item.value
                if isinstance(value, str) or isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
                    self.last_state[ns_name].append((key, value))
                elif isinstance(value, PurePath):
                    self.last_state[ns_name].append((key, str(value)))
                else:
                    if self.logger:
                        self.logger.debug(f"{key} not eligible for last state")

    def save_last(self):
        self.save_state()
        # Save to file
        try:
            with open(self.last_state_path, "wb") as f:
                f.write(json.dumps(self.last_state).encode('utf-8'))
        except Exception as e:
            if self.logger:
                self.logger.error(f"An error {e} occurred while attempting to save state - state not saved")

    def load_state(self, path: PurePath):
        loaded_state = None
        # Load from file
        try:
            with open(path, "rb") as f:
                file_contents = f.read()
                loaded_state = json.loads(file_contents)
        except Exception as e:
            if self.logger:
                self.logger.error(f"An error {e} occurred while attempting to load last state - last state not loaded")
        return loaded_state

    def load_configs(self, state):
        if state:
            for loaded_state_ns_name, data in state.items():
                if loaded_state_ns_name in self.config_namespaces_names:
                    config_ns = self.config.get_config(loaded_state_ns_name)
                    for config_item in data:
                        try:
                            config_ns.set(config_item[0], config_item[1])
                        except Exception as e:
                            if self.logger:
                                self.logger.info(
                                    f"Loaded state for {loaded_state_ns_name} has key {data[0]} saved, but current config has no such key registered - skipping.")

    def load_last(self):
        loaded_state = self.load_state(self.last_state_path)
        # Set configs
        self.load_configs(loaded_state)

    def save_project(self):
        project_path = filedialog.asksaveasfilename(
            defaultextension='.dmproj',
            filetypes=[("Documaker project", '*.dmproj')],
            initialdir=str(self.default_saved_projects_path)
        )
        self.save_state()
        # Save to file
        try:
            with open(project_path, "wb") as f:
                f.write(json.dumps(self.last_state).encode('utf-8'))
        except Exception as e:
            if self.logger:
                self.logger.error(f"An error {e} occurred while attempting to save state - state not saved")

    def load_project(self):
        load_path = open_file_dialog(self.default_saved_projects_path)
        if load_path:
            state = self.load_state(PurePath(load_path))
            self.load_configs(state)

    def on_exit(self):
        self.save_last()
        self.root.destroy()


def open_file_dialog(initial_dir: str | PurePath = None):
    if initial_dir and os.path.isdir(initial_dir):
        filename = filedialog.askopenfilename(initialdir=initial_dir)
    else:
        filename = filedialog.askopenfilename()
    return filename


if __name__ == "__main__":
    logger = PrintLogger()

    config_ = Config()
    base_config = config_.base_config
    base_path = PurePath(__file__).parent.parent.parent
    base_config.add_path_config_item("base_path", base_path)
    base_config.add_path_config_item("target_path", PurePath(base_path, "inputs"))
    base_config.add_path_config_item("output_path", PurePath(base_path, "outputs"))
    base_config.add_path_config_item("assets_path", PurePath(base_path, "outputs"))
    base_config.add_path_config_item("modules_path", PurePath(base_path, "modules"))
    base_config.add_config_item("assets_dir_name", "assets")
    base_config.add_config_item("output_name", "output.html")
    base_config.add_config_item("output_title", "GUI")
    base_config.add_config_item("logger", logger)
    base_config.add_config_item("logger_level", 20)

    gui_ = UserGUI(config_)
    gui_.start()

    print(config_)
