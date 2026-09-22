from lib.n_config import ConfigNamespace
import tkinter as tk
from tkinter import ttk


class MyWidget:
    def __init__(self, config_item: str, config_ns: ConfigNamespace, parent, label: str, focus_callback=None):
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
