# upe_budget.py
import tkinter as tk
from tkinter import ttk
from utils import center_window

def open_upe_budget(homepage_window, root):
    homepage_window.withdraw()
    upe_budget_window = tk.Toplevel(root)
    upe_budget_window.title("UPE Budget")
    center_window(upe_budget_window, 300, 200)

    label = tk.Label(upe_budget_window, text="This is Window UPE BUDGET")
    label.pack(pady=50)

    btn_homepage_window = ttk.Button(upe_budget_window, text="Back to Homepage", command=lambda: [upe_budget_window.destroy(), homepage_window.deiconify()])
    btn_homepage_window.pack(pady=10)