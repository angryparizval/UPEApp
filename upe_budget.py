# upe_budget.py
import tkinter as tk
from tkinter import ttk
import sqlite3
from utils import center_window

def fetch_budget_data():
    #creates connection and returns data as tuple
    conn = sqlite3.connect("UPEAPP.db")
    cursor = conn.cursor()
    cursor.execute("SELECT BDGET_TRNS_NO, BDGET_TRNS_DT, BDGET_TRNS_TYP, BDGET_RUNNING_TOT, BDGET_MEMO FROM budget")
    rows = cursor.fetchall()
    conn.close()
    return rows

def open_upe_budget(homepage_window, root):
    #withdrawal homepage
    homepage_window.withdraw()

    #creates window, sets title and centers it
    upe_budget_window = tk.Toplevel(root)
    upe_budget_window.title("View Budget")
    center_window(upe_budget_window, 800, 630)

    #creates header
    label = tk.Label(upe_budget_window, text="Budget Home", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=50)

    #back to homepage button
    btn_rtn_homepage_window = ttk.Button(upe_budget_window, text="Back to Homepage", command=lambda: [upe_budget_window.destroy(), homepage_window.deiconify()])
    btn_rtn_homepage_window.place(relx=0.05, rely=0.05, anchor="nw")

    #View history button
    btn_view_history = ttk.Button(upe_budget_window, text="View History", command=lambda: [upe_budget_window.withdraw(), open_budget_history(upe_budget_window, root)])
    btn_view_history.place(relx=0.5, rely=0.4, anchor="center")

    #Edit History button
    btn_edit_history = ttk.Button(upe_budget_window, text="Edit History", command=lambda: [upe_budget_window.withdraw(), homepage_window.deiconify()])
    btn_edit_history.place(relx=0.5, rely=0.5, anchor="center")

    #Add transaction buton
    btn_transaction = ttk.Button(upe_budget_window, text="Add Transaction", command=lambda: [upe_budget_window.withdraw(), homepage_window.deiconify()])
    btn_transaction.place(relx=0.5, rely=0.6, anchor="center")

def open_budget_history(budget_home_window, root):
    #withdrawals budget home
    budget_home_window.withdraw()

    #creates history page, sets title and centers it
    upe_budget_history = tk.Toplevel(root)
    upe_budget_history.title("Budget History")
    center_window(upe_budget_history, 800, 630)

    #creates header
    label = tk.Label(upe_budget_history, text="Budget History", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=20)

    #Back to Budget Home button
    btn_rtn_budget_home = ttk.Button(upe_budget_history, text="Back to Budget Home",
                                     command=lambda: [upe_budget_history.destroy(), budget_home_window.deiconify()])
    btn_rtn_budget_home.place(relx=0.05, rely=0.05, anchor="nw")

    #Table Frame
    frame = tk.Frame(upe_budget_history)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    #Define table columns
    columns = ("Transaction No", "Date", "Type", "Running Total", "Memo")

    #Create Treeview widget
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Define column properties
    tree.column("Transaction No", width=120, anchor="center")
    tree.column("Date", width=100, anchor="center")
    tree.column("Type", width=150, anchor="center")
    tree.column("Running Total", width=120, anchor="center")
    tree.column("Memo", width=200, anchor="w")

    # Define column headers
    for col in columns:
        tree.heading(col, text=col)

    #Insert data into table
    budget_data = fetch_budget_data()
    for row in budget_data:
        tree.insert("", tk.END, values=row)

    #Add scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    #Pack widgets
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def open_edit_budget(root):
    #creates edit budget window, sets title and centers it
    upe_budget_window = tk.Toplevel(root)
    upe_budget_window.title("Edit Budget")
    center_window(upe_budget_window, 800, 630)
