import os
from tkinter import ttk, filedialog
# Own imports
from base_gui_widget_pkg import LevelDropbox, NamingEntry, DirectoryCombobox
from gui import UserGUI
from n_config import Config, ConfigNamespace


class BaseConfigWidget(ttk.Labelframe):
    def __init__(self, gui: UserGUI):
        self.gui = gui
        self.config_frame = gui.get_config_frame()
        self.config: Config = gui.get_config()
        self.persistent_config: Config = gui.get_persistent_config()
        self.base_config: ConfigNamespace = self.config.get_base_config()
        super().__init__(self.config_frame)
        self.blockers = set()
        #
        self["text"] = "Base Config"
        self.combo_width = 80
        self.entry_width = 40
        self.config.get_base_config().subscribe_load(self.load)

        # Initialize persistent config
        self.persistent_config_ns = self.persistent_config.get_base_config()
        self.persistent_config.get_base_config().subscribe_load(self.persistent_load)

        # Target path
        self.target_config_widget = DirectoryCombobox(
            config_item="target_path",
            config_ns=self.base_config,
            persistent_config_ns=self.persistent_config_ns,
            persistent_item="target_dropdown",
            parent=self,
            label='Input Directory:',
            combobox_width=self.combo_width,
            initial_combo=self.base_config.get("target_path"),
            focus_callback=self.gui.focus_track
        )

        # Output path
        self.output_config_widget = DirectoryCombobox(
            config_item="output_path",
            config_ns=self.base_config,
            persistent_config_ns=self.persistent_config_ns,
            persistent_item="output_dropdown",
            parent=self,
            label='Output Directory:',
            combobox_width=self.combo_width,
            initial_combo=self.base_config.get("output_path"),
            focus_callback=self.gui.focus_track
        )

        # Widgets path
        self.widgets_config_widget = DirectoryCombobox(
            config_item="modules_path",
            config_ns=self.base_config,
            parent=self,
            label='Widgets Directory:',
            combobox_width=self.combo_width,
            initial_combo=self.base_config.get("modules_path"),
            focus_callback=self.gui.focus_track
        )

        # Assets directory name
        self.assets_config_widget = NamingEntry(
            config_item="assets_dir_name",
            config_ns=self.base_config,
            parent=self,
            label='Assets Directory Name:',
            input_width=self.entry_width,
            initial_input=self.base_config.get("assets_dir_name"),
            focus_callback=self.gui.focus_track
        )

        # Output file name
        self.output_name_config_widget = NamingEntry(
            config_item="output_name",
            config_ns=self.base_config,
            parent=self,
            label='Output File Name:',
            input_width=self.entry_width,
            initial_input=self.base_config.get("output_name"),
            focus_callback=self.gui.focus_track
        )

        # Output title
        self.output_title_config_widget = NamingEntry(
            config_item="output_title",
            config_ns=self.base_config,
            parent=self,
            label='Output Title:',
            input_width=self.entry_width,
            initial_input=self.base_config.get("output_title"),
            focus_callback=self.gui.focus_track
        )
        # Logger level
        self.logger_level_config_widget = LevelDropbox(
            config_item="logger_level",
            config_ns=self.base_config,
            parent=self,
            label='Logger Level:',
            combobox_width=10,
            initial_combo="DEBUG"
        )

        # JSREF opening tag
        self.jsref_open_widget = NamingEntry(
            config_item="jstag_open",
            config_ns=self.base_config,
            parent=self,
            label='JSREF opening tag:',
            input_width=self.entry_width,
            initial_input=self.base_config.get("jstag_open"),
            focus_callback=self.gui.focus_track
        )

        # JSREF closing tag
        self.jsref_close_widget = NamingEntry(
            config_item="jstag_close",
            config_ns=self.base_config,
            parent=self,
            label='JSREF closing tag:',
            input_width=self.entry_width,
            initial_input=self.base_config.get("jstag_close"),
            focus_callback=self.gui.focus_track
        )

    def load(self, config: ConfigNamespace):
        if config.get("target_path"):
            self.target_config_widget.combobox.set(config.get("target_path"))
            self.target_config_widget.check_correct()
        if config.get("output_path"):
            self.output_config_widget.combobox.set(config.get("output_path"))
            self.output_config_widget.check_correct()
        if config.get("modules_path"):
            self.widgets_config_widget.combobox.set(config.get("modules_path"))
            self.widgets_config_widget.check_correct()
        if config.get("assets_dir_name"):
            self.assets_config_widget.entry_var.set(config.get("assets_dir_name"))
        if config.get("output_name"):
            self.output_name_config_widget.entry_var.set(config.get("output_name"))
        if config.get("output_title"):
            self.output_title_config_widget.entry_var.set(config.get("output_title"))
        if config.get("logger_level"):
            self.logger_level_config_widget.set_level(config.get("logger_level"))
        if config.get("jstag_open"):
            self.jsref_open_widget.entry_var.set(config.get("jstag_open"))
        if config.get("jstag_close"):
            self.jsref_close_widget.entry_var.set(config.get("jstag_close"))

    def persistent_load(self, config: ConfigNamespace):
        if config.get("target_dropdown"):
            self.target_config_widget.load_persistent()
        if config.get("output_dropdown"):
            self.output_config_widget.load_persistent()

    def block(self, blocker):
        self.blockers.add(blocker)
        if len(self.blockers) > 0:
            self.gui.block(self)
        else:
            self.gui.unblock(self)

    def unblock(self, blocker):
        if blocker in self.blockers:
            self.blockers.remove(blocker)
            if len(self.blockers) > 0:
                self.gui.block(self)
            else:
                self.gui.unblock(self)


def open_directory_dialog(site_directory_text, initial_dir: str = None):
    if initial_dir and os.path.isdir(initial_dir):
        filename = filedialog.askdirectory(initialdir=initial_dir)
    else:
        filename = filedialog.askdirectory()
    site_directory_text.set(filename)
