from lib.n_config import ConfigNamespace
import tkinter as tk
from tkinter import ttk, filedialog
import os
# Own imports
from lib.base_gui_widget_pkg import MyWidget


class DirectoryCombobox(MyWidget):
    def __init__(
            self,
            config_item: str,
            config_ns: ConfigNamespace,
            parent: ttk.Widget,
            label: str,
            combobox_width: int,
            persistent_config_ns: ConfigNamespace = None,
            persistent_item: str = None,
            initial_combo: str = None,
            focus_callback=None
    ):
        super().__init__(config_item, config_ns, parent, label, focus_callback)
        self.persistent_config_ns = persistent_config_ns
        self.persistent_item = persistent_item
        self.combobox_width = combobox_width

        # Combobox dropdown
        self.dropdown_values = []
        if self.persistent_item:
            if self.persistent_config_ns.get(self.config_item):
                self.dropdown_values = self.config_ns.get(self.persistent_item)
            else:
                self.dropdown_values = []
                self.persistent_config_ns.set(self.persistent_item, [])
        else:  # If persistent_item wasn't set, it is assumed it is not meant to be saved persistently
            self.dropdown_values = []

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
            values=tuple(self.dropdown_values)
        )
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
        # self.config_ns.set(self.config_item, self.combobox_var.get(), propagate=False)
        self.config_ns.set(self.config_item, self.combobox_var.get())

    def on_leave(self, event):
        if self.check_correct():
            self.add_dropdown_value(self.combobox_var.get())
        # self.combobox.config(values=tuple(self.dropdown_values))

    def on_enter(self, event):
        if self.focus_callback:
            self.focus_callback(self.combobox)

    def check_correct(self) -> bool:
        if not os.path.isdir(self.combobox_var.get()):
            self.error_label_var.set("Given path is not a valid directory")
            return False
        else:
            self.error_label_var.set("")
            return True

    def load_persistent(self):
        if self.persistent_config_ns.get(self.persistent_item):
            self.dropdown_values = self.persistent_config_ns.get(self.persistent_item)
            self.combobox.config(values=self.dropdown_values)
        # else:
        #     self.persistent_config_ns.set(self.persistent_item, [])

    def add_dropdown_value(self, value):
        if value not in self.dropdown_values:
            self.dropdown_values.insert(0, value)
            if len(self.dropdown_values) > 6:
                self.dropdown_values = self.dropdown_values[:6]
            if self.persistent_item:  # If persistent_item wasn't set, it is assumed it is not meant to be saved persistently
                self.persistent_config_ns.set(self.persistent_item, self.dropdown_values)
            self.combobox.config(values=self.dropdown_values)

    # def load_persistent(self):
    #     if self.persistent_config_ns and self.persistent_item:
    #         if self.persistent_config_ns.get(self.persistent_item) is not None:
    #             self.dropdown_values = self.persistent_config_ns.get(self.persistent_item)
    #         else:
    #             self.persistent_config_ns.add_list_config_item("target_dropdown", [])
    #             self.dropdown_values = []
    #
    # def add_persistent(self, path: str):
    #     if path not in self.dropdown_values:
    #         self.dropdown_values.append(path)
    #         self.persistent_config_ns.set(self.persistent_item, self.dropdown_values, propagate=False)
