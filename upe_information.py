# upe_information.py
import tkinter as tk
from tkinter import ttk
from utils import center_window

def open_upe_information(homepage_window, root):
    #Withdraws homepage
    homepage_window.withdraw()

    #Create the page window
    upe_information_window = tk.Toplevel(root)
    upe_information_window.title("View Budget")
    center_window(upe_information_window, 800, 630)

    #Add the label
    label = tk.Label(upe_information_window, text="UPE Information", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.place(relx=0.5, rely=0.1, anchor="center")
    label.pack(pady=50)

    #Return button
    btn_rtn_homepage_window = ttk.Button(upe_information_window, text="Back to Homepage", command=lambda: [upe_information_window.destroy(), homepage_window.deiconify()])
    btn_rtn_homepage_window.place(relx=0.05, rely=0.05, anchor="nw")
