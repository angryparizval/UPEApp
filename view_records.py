# view_records.py
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from utils import center_window

#Window to select which records and if the user wants to edit or view
def open_view_records(homepage_window, root):
    #withdraws homepage
    homepage_window.withdraw()
    global view_records_window

    #sets window to rootmm, updates title and centers it
    view_records_window = tk.Toplevel(root)
    view_records_window.title("View Records")
    center_window(view_records_window, 500, 400)

    #temporary label of information
    label = tk.Label(view_records_window, text="This is UPE Records")
    label.pack(pady=50)

    #button to move to add members windows
    btn_addmembers_window = ttk.Button(view_records_window, text="Add Members", command=lambda: open_add_members(root))
    btn_addmembers_window.pack(pady=10)

    #button to return to homepage
    btn_homepage_window = ttk.Button(view_records_window, text="Back to Homepage", command=lambda: [view_records_window.destroy(), homepage_window.deiconify()])
    btn_homepage_window.pack(pady=10)

#Window where user will input info to add member
def open_add_members(root):
    view_records_window.withdraw()
    global add_members_window
    add_members_window = tk.Toplevel(root)
    center_window(view_records_window, 500, 400)
