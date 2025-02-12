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

    #Add the label
    label = tk.Label(upe_budget_window, text="Budget Home", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.place(relx=0.5, rely=0.1, anchor="center")
    label.pack(pady=50)

    #Return button
    btn_rtn_homepage_window = ttk.Button(upe_budget_window, text="Back to Homepage", command=lambda: [upe_budget_window.destroy(), homepage_window.deiconify()])
    btn_rtn_homepage_window.place(relx=0.05, rely=0.05, anchor="nw")

    #View history button: Open budget history window and withdraw budget home ---- CONNECT WITH BUDGET PAGES WHEN READY --------v
    btn_view_history = ttk.Button(upe_budget_window, text="View History", command=lambda: [upe_budget_window.withdraw(), open_budget_history(root)])
    btn_view_history.place(relx=0.5, rely=0.4, anchor="center")

    #Edit history button: Open budget edit window and withdraw budget home ------- CONNECT WITH BUDGET PAGES WHEN READY --------v
    btn_edit_history = ttk.Button(upe_budget_window, text="Edit History", command=lambda: [upe_budget_window.withdraw(), homepage_window.deiconify()])
    btn_edit_history.place(relx=0.5, rely=0.5, anchor="center")

    #Input transaction button ---------------------------------------------------- CONNECT WITH BUDGET PAGES WHEN READY --------v
    btn_transaction = ttk.Button(upe_budget_window, text="Add Transaction", command=lambda: [upe_budget_window.withdraw(), homepage_window.deiconify()])
    btn_transaction.place(relx=0.5, rely=0.6, anchor="center")

    
def open_budget_history(root):
    #Create the page window
    upe_budget_history = tk.Toplevel(root)
    upe_budget_history.title("View Budget")
    center_window(upe_budget_history, 800, 630)

    #Add the label
    label = tk.Label(upe_budget_history, text="Budget History", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.place(relx=0.5, rely=0.1, anchor="center")
    label.pack(pady=50)

    #Return button ------- UNABLE TO GET BACK TO THE BUDGET HOME, "'function' object has no attribute 'deiconify'" ERROR --------v
    btn_rtn_budget_home = ttk.Button(upe_budget_history, text="Back to Budget Home", command=lambda: [upe_budget_history.destroy(), open_upe_budget.deiconify()])
    btn_rtn_budget_home.place(relx=0.05, rely=0.05, anchor="nw")

def open_edit_budget(root):
    #Create the page window
    upe_budget_window = tk.Toplevel(root)
    upe_budget_window.title("Edit Budget")
    center_window(upe_budget_window, 800, 630)

