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

    #View budget button: Open budget history window and withdraw budget home 
    btn_view_history = ttk.Button(upe_budget_window, text="View Budget", command=lambda: [upe_budget_window.withdraw(), open_view_budget(upe_budget_window, root)])
    btn_view_history.place(relx=0.5, rely=0.4, anchor="center")

    #Edit history button: Open budget edit window and withdraw budget home
    btn_edit_history = ttk.Button(upe_budget_window, text="Edit History", command=lambda: [upe_budget_window.withdraw(), open_edit_budget(upe_budget_window, root)])
    btn_edit_history.place(relx=0.5, rely=0.5, anchor="center")

    #Input transaction button: Open add transaction window and withdraw budget home
    btn_transaction = ttk.Button(upe_budget_window, text="Add Transaction", command=lambda: [upe_budget_window.withdraw(), open_add_transaction(upe_budget_window, root)])
    btn_transaction.place(relx=0.5, rely=0.6, anchor="center")

    
def open_view_budget(upe_budget_window, root):
    #Create the page window
    upe_view_budget = tk.Toplevel(root)
    upe_view_budget.title("View Budget")
    center_window(upe_view_budget, 800, 630)

    #Add the label
    label = tk.Label(upe_view_budget, text="View Budget", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.place(relx=0.5, rely=0.02, anchor="center")
    label.pack(pady=50)

    #Return button
    btn_rtn_budget_home = ttk.Button(upe_view_budget, text="Back", command=lambda: [upe_view_budget.destroy(), upe_budget_window.deiconify()])
    btn_rtn_budget_home.place(relx=0.02, rely=0.05, anchor="nw")

    #Add transaction button
    btn_new_transaction = ttk.Button(upe_view_budget, text="Add Transaction", command=lambda: [upe_view_budget.destroy(), open_add_transaction(upe_budget_window, root)])
    btn_new_transaction.place(relx=0.825, rely=0.95, anchor="sw")

def open_edit_budget(upe_budget_window, root):
    #Create the page window
    upe_edit_budget = tk.Toplevel(root)
    upe_edit_budget.title("Edit Budget")
    center_window(upe_edit_budget, 800, 630)

    #Add the label
    label = tk.Label(upe_edit_budget, text="Edit Budget", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.place(relx=0.5, rely=0.02, anchor="center")
    label.pack(pady=50)

    #Return button
    btn_rtn_budget_home = ttk.Button(upe_edit_budget, text="Back", command=lambda: [upe_edit_budget.destroy(), upe_budget_window.deiconify()])
    btn_rtn_budget_home.place(relx=0.02, rely=0.05, anchor="nw")

    #Add table that will display all past transactions and allow the user to sort by date, amount, and withdrawal/deposit
    


def open_add_transaction(upe_budget_window, root):
    #Create the page window
    upe_add_trans = tk.Toplevel(root)
    upe_add_trans.title("Add Transaction")
    center_window(upe_add_trans, 800, 630)

    #Add the label
    label = tk.Label(upe_add_trans, text="Add Transaction", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.place(relx=0.5, rely=0.02, anchor="center")
    label.pack(pady=50)

    #Return button
    btn_rtn_budget_home = ttk.Button(upe_add_trans, text="Back", command=lambda: [upe_add_trans.destroy(), upe_budget_window.deiconify()])
    btn_rtn_budget_home.place(relx=0.02, rely=0.05, anchor="nw")

