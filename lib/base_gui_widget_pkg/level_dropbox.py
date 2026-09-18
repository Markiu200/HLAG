from lib.n_config import ConfigNamespace
import tkinter as tk
from tkinter import ttk
import logging
# Own imports
from lib.base_gui_widget_pkg import MyWidget


class LevelDropbox(MyWidget):
    def __init__(
            self,
            config_item: str,
            config_ns: ConfigNamespace,
            parent: ttk.Widget,
            label: str,
            combobox_width: int,
            initial_combo: str = None,
            focus_callback=None
    ):
        super().__init__(config_item, config_ns, parent, label, focus_callback)
        self.logger = None
        if self.config_ns.get("logger_name"):
            self.logger = logging.getLogger(self.config_ns.get("logger_name"))
        #
        self.combobox_width = combobox_width
        self.combobox_values = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        # Combobox var
        self.combobox_var = tk.StringVar()
        if initial_combo:
            self.combobox_var.set(initial_combo)
        self.combobox_var.trace_add("write", self.set_config)
        # Combobox
        self.combobox = ttk.Combobox(
            self.frame,
            textvariable=self.combobox_var,
            width=self.combobox_width,
            state="readonly",
            values=self.combobox_values
        )
        if initial_combo:
            self.combobox.set(initial_combo)
        self.combobox.pack(side=tk.LEFT)

    def set_config(self, var, index, mode):
        level = logging.getLevelName(self.combobox_var.get())
        self.config_ns.set(self.config_item, level)
        if self.logger:
            self.logger.setLevel(level)

    def set_level(self, level: int):
        level_text = logging.getLevelName(level)
        self.combobox_var.set(level_text)
