import tkinter as tk
import os
from tkinter import ttk, filedialog
from lib.n_config import Config, ConfigNamespace
from lib.gui import UserGUI


def open_directory_dialog(site_directory_text, initial_dir: str = None):
    if initial_dir and os.path.isdir(initial_dir):
        filename = filedialog.askdirectory(initialdir=initial_dir)
    else:
        filename = filedialog.askdirectory()
    site_directory_text.set(filename)


class MyWidget:
    def __init__(self, config_item: str, config_ns: ConfigNamespace, parent: ttk.Widget, label: str, focus_callback=None):
        self.config_item = config_item
        self.config_ns = config_ns
        self.parent = parent
        self.label = label
        self.focus_callback = focus_callback
        # Label
        self.frame = ttk.Frame(parent)
        self.label = ttk.Label(self.frame, text=self.label, width=22)
        self.label.pack(side=tk.LEFT)
        self.frame.pack(side=tk.TOP, expand=True, fill="both")
        # Error label
        self.error_label_var = tk.StringVar()
        self.error_label = ttk.Label(parent, textvariable=self.error_label_var, foreground="red")
        self.error_label.config(font=("Arial", 8))
        self.error_label.pack(side=tk.TOP, expand=True, fill="both")


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
        self.combobox_width = combobox_width
        self.combobox_values = ("Debug", "Info", "Warning", "Error", "Critical")
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
        logger = self.config_ns.get("logger")
        if logger:
            self.config_ns.set(self.config_item, self.combobox_var.get(), propagate=False)
            logger.set_level_by_name(self.combobox_var.get())


class NamingEntry(MyWidget):
    def __init__(
            self,
            config_item: str,
            config_ns: ConfigNamespace,
            parent: ttk.Widget,
            label: str,
            input_width: int,
            initial_input: str = None,
            focus_callback=None
    ):
        super().__init__(config_item, config_ns, parent, label, focus_callback)
        self.entry_width = input_width
        # Entry var
        self.entry_var = tk.StringVar()
        self.entry_var.trace_add("write", self.set_config)
        # Entry
        self.entry = ttk.Entry(self.frame, textvariable=self.entry_var, width=self.entry_width)
        if initial_input:
            self.entry_var.set(initial_input)
        self.entry.bind("<FocusIn>", self.on_enter)
        # Packing
        self.entry.pack(side=tk.LEFT)

    def on_enter(self, event):
        if self.focus_callback:
            self.focus_callback(self.entry)

    def set_config(self, var, index, mode):
        self.config_ns.set(self.config_item, self.entry_var.get(), propagate=False)


class DirectoryCombobox(MyWidget):
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
        self.combobox_width = combobox_width
        # Combobox var
        self.combobox_var = tk.StringVar()
        if initial_combo:
            self.combobox_var.set(initial_combo)
        self.combobox_var.trace_add("write", self.set_config)
        # Combobox
        self.combobox = ttk.Combobox(self.frame, textvariable=self.combobox_var, width=self.combobox_width)
        if initial_combo:
            self.combobox.set(initial_combo)
        self.combobox.bind("<FocusOut>", self.on_leave)
        self.combobox.bind("<FocusIn>", self.on_enter)
        # Browse button
        self.browse_button = ttk.Button(
            self.frame,
            text='browse',
            width=8,
            command=self.open_directory_dialog,
            takefocus=0
        )
        # Packing
        self.combobox.pack(side=tk.LEFT)
        self.browse_button.pack(side=tk.LEFT)

    def open_directory_dialog(self):
        if self.combobox_var.get() and os.path.isdir(self.combobox_var.get()):
            selected = filedialog.askdirectory(initialdir=self.combobox_var.get())
            if selected:
                self.combobox_var.set(selected)
                self.check_correct()
        else:
            selected = filedialog.askdirectory()
            if selected:
                self.combobox_var.set(selected)
                self.check_correct()

    def set_config(self, var, index, mode):
        self.config_ns.set(self.config_item, self.combobox_var.get(), propagate=False)

    def on_leave(self, event):
        self.check_correct()

    def on_enter(self, event):
        if self.focus_callback:
            self.focus_callback(self.combobox)

    def check_correct(self):
        if not os.path.isdir(self.combobox_var.get()):
            self.error_label_var.set("Given path is not a valid directory")
        else:
            self.error_label_var.set("")


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
