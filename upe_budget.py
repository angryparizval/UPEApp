# upe_budget.py
import tkinter as tk
from tkinter import ttk
from utils import center_window

def open_upe_budget(homepage_window, root):
    #Withdraws homepage
    homepage_window.withdraw()

    #Create the page window
    upe_budget_window = tk.Toplevel(root)
    upe_budget_window.title("View Budget")
    center_window(upe_budget_window, 800, 630)

    #label = tk.Label(upe_budget_window, text="This is Window UPE BUDGET")
    #label.pack(pady=50)

    #Add the label and buttons
    label = tk.Label(upe_budget_window, text="Budget Home", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.place(relx=0.5, rely=0.1, anchor="center")
    label.pack(pady=50)

    #Return button
    btn_rtn_homepage_window = ttk.Button(upe_budget_window, text="Back to Homepage", command=lambda: [upe_budget_window.destroy(), homepage_window.deiconify()])
    btn_rtn_homepage_window.place(relx=0.05, rely=0.05, anchor="nw")

    #View history button: Open budget history window and withdraw budget home
    btn_view_history = ttk.Button(upe_budget_window, text="View History", command=lambda: [upe_budget_window.withdraw(), homepage_window.deiconify()])
    #btn_view_history = ttk.Button(upe_budget_window, text="View History", command=lambda: [upe_budget_window.withdraw(), open_budget_history(root)])
    btn_view_history.place(relx=0.5, rely=0.5, anchor="center")

    #Edit history button

    #Input transaction button


    