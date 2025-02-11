# view_records.py
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from utils import center_window


def open_view_records(homepage_window, root):
    homepage_window.withdraw()
    global view_records_window
    view_records_window = tk.Toplevel(root)
    view_records_window.title("View Records")
    center_window(view_records_window, 500, 400)
    label = tk.Label(view_records_window, text="This is UPE Records")
    label.pack(pady=50)


    btn_addmembers_window = ttk.Button(view_records_window, text="Add Members", command=open_add_members())

    btn_homepage_window = ttk.Button(view_records_window, text="Back to Homepage", command=lambda: [view_records_window.destroy(), homepage_window.deiconify()])
    btn_homepage_window.pack(pady=10)

def open_add_members():
    view_records_window.withdraw()
    global add_members_window
    add_members_window = tk.Toplevel()
    center_window(view_records_window, 500, 400)
