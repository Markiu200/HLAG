import os
from tkinter import ttk, filedialog
# Own imports
from lib.base_gui_widget_pkg import LevelDropbox, NamingEntry, DirectoryCombobox
from lib.gui import UserGUI


class BaseConfigWidget(ttk.Labelframe):
    def __init__(self, gui: UserGUI):
        self.gui = gui
        self.config_frame = gui.get_config_frame()
        self.config = gui.config
        self.base_config = self.config.get_base_config()
        super().__init__(self.config_frame)
        #
        self["text"] = "Base Config"
        self.combo_width = 80
        self.entry_width = 40
        self.config.subscribe(self.load)

        # Target path
        self.target_config_widget = DirectoryCombobox(
            config_item="target_path",
            config_ns=self.base_config,
            parent=self,
            label='Target Directory:',
            combobox_width=self.combo_width,
            initial_combo=self.base_config.get_default("target_path"),
            focus_callback=self.gui.focus_track
        )

        # Output path
        self.output_config_widget = DirectoryCombobox(
            config_item="output_path",
            config_ns=self.base_config,
            parent=self,
            label='Output Directory:',
            combobox_width=self.combo_width,
            initial_combo=self.base_config.get_default("output_path"),
            focus_callback=self.gui.focus_track
        )

        # Widgets path
        self.widgets_config_widget = DirectoryCombobox(
            config_item="modules_path",
            config_ns=self.base_config,
            parent=self,
            label='Widgets Directory:',
            combobox_width=self.combo_width,
            initial_combo=self.base_config.get_default("modules_path"),
            focus_callback=self.gui.focus_track
        )

        # Assets directory name
        self.assets_config_widget = NamingEntry(
            config_item="assets_dir_name",
            config_ns=self.base_config,
            parent=self,
            label='Assets Directory Name:',
            input_width=self.entry_width,
            initial_input=self.base_config.get_default("assets_dir_name"),
            focus_callback=self.gui.focus_track
        )

        # Output file name
        self.output_name_config_widget = NamingEntry(
            config_item="output_name",
            config_ns=self.base_config,
            parent=self,
            label='Output File Name:',
            input_width=self.entry_width,
            initial_input=self.base_config.get_default("output_name"),
            focus_callback=self.gui.focus_track
        )

        # Output title
        self.output_title_config_widget = NamingEntry(
            config_item="output_title",
            config_ns=self.base_config,
            parent=self,
            label='Output Title:',
            input_width=self.entry_width,
            initial_input=self.base_config.get_default("output_title"),
            focus_callback=self.gui.focus_track
        )

        # Logger level
        self.logger_level_config_widget = LevelDropbox(
            config_item="logger_level",
            config_ns=self.base_config,
            parent=self,
            label='Logger Level:',
            combobox_width=9,
            initial_combo="Info"
        )

    def load(self, config_ns: str, key: str, value):
        if config_ns == "base_config":
            if key == "target_path":
                self.target_config_widget.combobox.set(value)
                self.target_config_widget.check_correct()
            elif key == "output_path":
                self.output_config_widget.combobox.set(value)
                self.output_config_widget.check_correct()
            elif key == "modules_path":
                self.widgets_config_widget.combobox.set(value)
                self.widgets_config_widget.check_correct()
            elif key == "assets_dir_name":
                self.assets_config_widget.entry_var.set(value)
            elif key == "output_name":
                self.output_name_config_widget.entry_var.set(value)
            elif key == "output_title":
                self.output_title_config_widget.entry_var.set(value)
            elif key == "logger_level":
                self.logger_level_config_widget.combobox.set(value)


def open_directory_dialog(site_directory_text, initial_dir: str = None):
    if initial_dir and os.path.isdir(initial_dir):
        filename = filedialog.askdirectory(initialdir=initial_dir)
    else:
        filename = filedialog.askdirectory()
    site_directory_text.set(filename)
