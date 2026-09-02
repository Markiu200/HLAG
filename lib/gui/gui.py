import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import PurePath

from config import config

module_path = PurePath(__file__).parent
settings_path = PurePath(module_path, "settings")
default_saved_projects_path = PurePath(module_path.parent.parent, 'saved_projects')


def open_directory_dialog(site_directory_text):
    filename = filedialog.askdirectory()
    site_directory_text.set(filename)


def load_last():
    pass


def save_last():
    pass


def save_project():
    pass


def load_project():
    pass


def start():
    root = tk.Tk()
    root.title('Makesite')

    # Menubar
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=False)
    file_menu.add_command(label='Save Project', command=save_project)
    file_menu.add_command(label='Load Project', command=load_project)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=root.destroy)
    menubar.add_cascade(label='File', menu=file_menu, underline=0)

    #
    root.config(menu=menubar)

    # Static bits
    site_directory_label = ttk.Label(root, text='Directory:')

    # Interactive bits
    target_directory_choice = tk.StringVar()
    site_directory = ttk.Combobox(root, textvariable=target_directory_choice)

    site_directory_browse_button = ttk.Button(root, text='browse',
                                              command=lambda v=target_directory_choice: open_directory_dialog(v))

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

    # todo temporary check for empty directory
    if target_directory_choice.get() == "":
        raise NotADirectoryError(f"Root directory not set!")
        # target_directory_choice.set('D:\\hlag\\webpage')

    config.target_path = PurePath(target_directory_choice.get())
    config.embed_images = False


if __name__ == "__main__":
    start()

    print(config)
    hold_the_screen = input("Press any key to exit...")
