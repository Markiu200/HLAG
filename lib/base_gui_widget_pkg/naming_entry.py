from lib.n_config import ConfigNamespace
import tkinter as tk
from tkinter import ttk
# Own imports
from lib.base_gui_widget_pkg.my_widget import MyWidget


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
        # self.config_ns.set(self.config_item, self.entry_var.get(), propagate=False)
        self.config_ns.set(self.config_item, self.entry_var.get())
