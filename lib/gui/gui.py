import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from config import config
from pathlib import PurePath


def open_directory_dialog(site_directory_text):
    filename = filedialog.askdirectory()
    site_directory_text.set(filename)


def start():
    root = tk.Tk()
    root.title('Makesite')
    # root.geometry('300x100')

    # Static bits
    site_directory_label = ttk.Label(root, text='Directory:')

    # Interactive bits
    site_directory_text = tk.StringVar()
    site_directory = ttk.Entry(root, textvariable=site_directory_text)

    site_directory_browse_button = ttk.Button(root, text='browse',
                                              command=lambda v=site_directory_text: open_directory_dialog(v))

    # Packing
    site_directory_label.pack(side=tk.LEFT)
    site_directory.pack(side=tk.LEFT)
    site_directory_browse_button.pack(side=tk.LEFT)

    # Running
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root.mainloop()

    # Return settings to main program after completion
    # todo temporary check for empty directory
    if site_directory_text.get() == "":
        # raise NotADirectoryError(f"Root directory not set!")
        site_directory_text.set('D:\\hlag\\webpage')

    # return Config(
    #     target_path=PurePath(site_directory_text.get()),
    #     embed_images=False
    # )
    config.target_path = PurePath(site_directory_text.get())
    config.embed_images = False


if __name__ == "__main__":
    start()

    hold_the_screen = input("Press any key to exit...")
