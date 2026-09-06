import tkinter as tk
from tkinter import ttk
from lib.n_config import Config


class ConfigWidget(ttk.Labelframe):
    def __init__(self, parent, config: Config):
        super().__init__(parent)
        self.parent = parent
        self.config = config
        self.config_ns = self.config.get_config("raw_image")
        self["text"] = "Raw Image"
        # Label
        self.frame = ttk.Frame(self)
        self.label = ttk.Label(self.frame, text="Save As:", width=22)
        self.label.pack(side=tk.LEFT)
        self.frame.pack(side=tk.TOP, expand=True, fill="both")
        # Radio buttons
        self.radio_var = tk.StringVar()
        self.base64_radio = ttk.Radiobutton(self.frame, text='base64', value="True", variable=self.radio_var, command=self.set_base)
        self.assets_radio = ttk.Radiobutton(self.frame, text='assets', value="False", variable=self.radio_var, command=self.set_base)
        self.assets_radio.invoke()
        self.base64_radio.pack(side=tk.LEFT, padx=(0, 20))
        self.assets_radio.pack(side=tk.LEFT)

    def set_base(self):
        if self.radio_var.get() == "True":
            self.config_ns.set("base64", True)
        if self.radio_var.get() == "False":
            self.config_ns.set("base64", False)
