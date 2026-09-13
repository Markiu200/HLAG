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
