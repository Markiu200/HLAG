import tkinter as tk
from pathlib import PurePath
# Own imports
from lib.n_config import Config
from lib.print_logger import PrintLogger


class UserGUI:
    def __init__(self, config: Config):
        self.config = config
        self.module_path = PurePath(__file__).parent
        self.default_saved_projects_path = PurePath(self.module_path.parent.parent, 'saved_projects')
        self.settings_path = PurePath(self.module_path.parent.parent, "settings.dat")
        #
        self.config_widgets = []

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

        # Pack all config widgets
        for widget in self.config_widgets:
            config_widget = widget(root, self.config)
            config_widget.pack(side=tk.TOP, expand=True, fill=tk.X, padx=10, pady=10, ipadx=10, ipady=5)

        # Running
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        finally:
            root.mainloop()


def load_last():
    pass


def save_last():
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
