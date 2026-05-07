import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


def open_directory_dialog(site_directory_text):
    filename = filedialog.askdirectory()
    site_directory_text.set(filename)


def main():
    root = tk.Tk()
    root.title('Makesite')
    # root.geometry('300x100')

    site_directory_label = ttk.Label(root, text='Directory:')

    site_directory_text = tk.StringVar()
    site_directory = ttk.Entry(root, textvariable=site_directory_text)

    site_directory_browse_button = ttk.Button(root, text='browse', command=lambda v=site_directory_text: open_directory_dialog(v))

    site_directory_label.pack(side=tk.LEFT)
    site_directory.pack(side=tk.LEFT)
    site_directory_browse_button.pack(side=tk.LEFT)

    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root.mainloop()

    print("Executed after mainloop")
    smileyface = input("ey")


if __name__ == "__main__":
    main()
