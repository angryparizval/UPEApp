import tkinter as tk
from tkinter import ttk
import os
import subprocess
import sys
from utils import center_window
from tkinter import PhotoImage

#Function is most needed when opening PDFs on different operating systems with specific file location
def open_upe_information(homepage_window, root):
    # Withdraw homepage
    homepage_window.withdraw()

    # Create new window
    upe_information_window = tk.Toplevel(root)
    upe_information_window.title("UPE Information")
    center_window(upe_information_window, 965, 630)

    # Load the image and store a reference
    upe_information_window.image_ref = PhotoImage(file="UPE-banner.png")
    resized_image = upe_information_window.image_ref.subsample(2, 2)

    # Create a Label with the image
    image_label = tk.Label(upe_information_window, image=resized_image)
    image_label.image = resized_image  # Keep reference
    image_label.pack()

    # Label
    label = tk.Label(upe_information_window, text="UPE Information", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=50)

    # Button to return to homepage
    btn_rtn_homepage_window = ttk.Button(upe_information_window, text="Back to Homepage", command=lambda: [upe_information_window.destroy(), homepage_window.deiconify()])
    btn_rtn_homepage_window.place(relx=0.05, rely=0.05, anchor="nw")

    # Button to LRU bylaws
    btn_open_doc = ttk.Button(upe_information_window, text="Open LRU bylaws PDF", command=lambda: open_file("LRU bylaws.pdf"))
    btn_open_doc.pack(pady=20)

    # Button to LRU Constitution
    btn_open_doc = ttk.Button(upe_information_window, text="Open LRU Constitution PDF", command=lambda: open_file("LRU Constitution.pdf"))
    btn_open_doc.pack(pady=20)

    # Button to UPE Infographic PDF
    btn_open_doc = ttk.Button(upe_information_window, text="Open UPE Infographic PDF", command=lambda: open_file("UPE-Infographic_2022.pdf"))
    btn_open_doc.pack(pady=20)

    # Print list of Charter Faculty
    # Print a list of Charter Alumni
    # Print a list of Undergraduate Students
