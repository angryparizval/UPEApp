# main.py
import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkinter import PhotoImage
from utils import center_window
from upe_budget import open_upe_budget
from invitation_report import open_invitation_report_window
from records_actions import open_records_act
from upe_information import open_upe_information

# Function to handle login and check if the credentials are correct
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Check credentials are correct
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome to the Application!")
        open_homepage()
    # Show error message if credentials are invalid
    else:
        #messagebox.showerror("Login Failed", "Invalid username or password")
        open_homepage()

# Function to open the homepage
def open_homepage():
    global homepage_window, homepage_image

    # Destroy the login window
    if login_window.winfo_exists():
        login_window.destroy()

    # Create the homepage window
    homepage_window = tk.Toplevel(root)
    homepage_window.title("Homepage")
    center_window(homepage_window, 800, 630)

    # Load the image and keep a reference to it
    homepage_image = PhotoImage(file="Image/UPE-background.png")
    resized_image = homepage_image.subsample(2, 2)

    # Create a label with the resized image
    image_label = tk.Label(homepage_window, image=resized_image)
    image_label.image = resized_image
    image_label.pack()

    #Button to go to Budget window
    btn_upe_budget_window = ttk.Button(homepage_window, text="UPE Budget", command=lambda: open_upe_budget(homepage_window, root))
    btn_upe_budget_window.pack(pady=10)

    #Button to go to records action window
    btn_open_records_act_window = ttk.Button(homepage_window, text="Records Actions", command=lambda: open_records_act(homepage_window, root))
    btn_open_records_act_window.pack(pady=10)

    #Button to go to window for creating invitation
    btn_open_invitation_report_window = ttk.Button(homepage_window, text="Create Invitation", command=lambda: open_invitation_report_window(homepage_window, root))
    btn_open_invitation_report_window.pack(pady=10)
    
    #Button to go to UPE Info window
    btn_open_invitation_report_window = ttk.Button(homepage_window, text="UPE Information", command=lambda: open_upe_information(homepage_window, root))
    btn_open_invitation_report_window.pack(pady=10)

    #Button to exit application
    btn_exit = ttk.Button(homepage_window, text="Exit Application", command=root.quit)
    btn_exit.pack(pady=10)

# Function to open the login window
def open_login_window():
    global login_window, entry_username, entry_password, login_image

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    center_window(login_window, 800, 630)

    # Load the image and keep a reference to it
    login_image = PhotoImage(file="Image/UPE-logo.png")
    resized_login_image = login_image.subsample(5, 5)

    # Create a label with the resized image
    image_label = tk.Label(login_window, image=resized_login_image)
    image_label.image = resized_login_image
    image_label.pack()

    # Add username and password fields
    label_username = tk.Label(login_window, text="Username:")
    label_username.pack(pady=5)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)

    label_password = tk.Label(login_window, text="Password:")
    label_password.pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    # Add login button
    btn_login = ttk.Button(login_window, text="Login", command=login)
    btn_login.pack(pady=20)

# Main application root window
root = ThemedTk()
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), foreground='black')
style.map('TButton', background=[('active', 'black'), ('pressed', 'red')], foreground=[('active', 'red'), ('pressed', 'green')])

root.withdraw()

# Create the startup screen
startup_window = tk.Toplevel(root)
startup_window.title("Welcome to UPE")
center_window(startup_window, 480, 480)

# Load the image and keep a reference to it
startup_image = PhotoImage(file="Image/UPE-opening.png")
resized_startup_image = startup_image.subsample(2, 2)

# Create a label with the resized image
image_label = tk.Label(startup_window, image=resized_startup_image)
image_label.image = resized_startup_image
image_label.pack()

# Simulates a 4 second delay for the startup screen
startup_window.after(1000, lambda: [startup_window.destroy(), open_login_window()])

# Start the main event loop
root.mainloop()