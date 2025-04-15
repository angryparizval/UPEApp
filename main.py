import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow for better image handling
from utils import center_window
from upe_budget import open_upe_budget
from invitation_report import open_invitation_report_window
from records_actions import open_records_act
from upe_information import open_upe_information
from utils import resource_path


#build the path to the images
background_image_path = resource_path('Image/UPE-background.png')
opening_image_path = resource_path('Image/UPE-opening.png')
banner_image_path = resource_path('Image/UPE-banner.png')
logo_image_path = resource_path('Image/UPE-logo.png')
shortbanner_image_path = resource_path('Image/UPE-shortbanner.jpg')
icon_path = resource_path("Image/icon.ico") 


# Function to handle login and check if the credentials are correct
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Check credentials are correct
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome to the Application!")
        open_homepage()
    else:
        messagebox.showinfo("Login Failed!", "Username or Password was incorrect! Please try again!")

# Function to open the homepage
def open_homepage():
    global homepage_window, homepage_image

    # Destroy the login window if it exists
    if login_window.winfo_exists():
        login_window.destroy()

    # Create the homepage window
    homepage_window = tk.Toplevel(root)
    homepage_window.title("Homepage")
    homepage_window.iconbitmap(icon_path)
    center_window(homepage_window, 950, 700)

    # Load the image using PIL
    homepage_image = Image.open(background_image_path)
    resized_image = homepage_image.resize((1150, 700))  # Resize if needed

    # Convert the image to a Tkinter-compatible format
    tk_homepage_image = ImageTk.PhotoImage(resized_image)

    # Create a label with the resized image
    image_label = tk.Label(homepage_window, image=tk_homepage_image)
    image_label.image = tk_homepage_image
    image_label.pack()

    # Place buttons and other elements
    btn_upe_budget_window = ttk.Button(homepage_window, text="UPE Budget", command=lambda: open_upe_budget(homepage_window, root))
    btn_upe_budget_window.pack(pady=10)
    btn_upe_budget_window.place(relx=0.14, rely=.5)

    btn_open_records_act_window = ttk.Button(homepage_window, text="Records Actions", command=lambda: open_records_act(homepage_window, root))
    btn_open_records_act_window.pack(pady=10)
    btn_open_records_act_window.place(relx=0.13, rely=.6)

    btn_open_invitation_report_window = ttk.Button(homepage_window, text="Create Invitation", command=lambda: open_invitation_report_window(homepage_window, root))
    btn_open_invitation_report_window.pack(pady=10)
    btn_open_invitation_report_window.place(relx=0.75, rely=.5)

    btn_open_upe_information_window = ttk.Button(homepage_window, text="UPE Information", command=lambda: open_upe_information(homepage_window, root))
    btn_open_upe_information_window.pack(pady=10)
    btn_open_upe_information_window.place(relx=0.75, rely=.6)

    btn_exit = ttk.Button(homepage_window, text="Exit Application", command=root.quit)
    btn_exit.pack(pady=10)
    btn_exit.place(relx=0.428, rely=.91)

# Function to open the login window
def open_login_window():
    global login_window, entry_username, entry_password, login_image

    # Create the login window
    login_window = tk.Toplevel(root)
    login_window.iconbitmap(icon_path)
    login_window.title("Login")
    center_window(login_window, 800, 630)

    # Load the image using PIL
    login_image = Image.open(logo_image_path)
    resized_login_image = login_image.resize((105, 100)) 

    # Convert the image to a Tkinter-compatible format
    tk_login_image = ImageTk.PhotoImage(resized_login_image)

    # Create a label with the resized image
    image_label = tk.Label(login_window, image=tk_login_image)
    image_label.image = tk_login_image
    image_label.pack()

    # Add username and password fields
    label_username = tk.Label(login_window, text="Username:", font=("Helvetica", 12))
    label_username.pack(pady=5)
    entry_username = ttk.Entry(login_window)
    entry_username.pack(pady=5)

    label_password = tk.Label(login_window, text="Password:", font=("Helvetica", 12))
    label_password.pack(pady=5)
    entry_password = ttk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    # Add login button
    btn_login = ttk.Button(login_window, text="Login", command=login)
    btn_login.pack(pady=20)

    
    login_window.bind("<Return>", lambda event: login())

# Main application root window
root = ThemedTk()

 
root.iconbitmap(icon_path)

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 15), foreground='black')
style.map('TButton', background=[('active', 'black'), ('pressed', 'red')], foreground=[('active', 'red'), ('pressed', 'green')])
style.configure('TEntry', foreground='black', fieldbackground='white')

root.withdraw()

# Create the startup screen window
startup_window = tk.Toplevel(root)
startup_window.iconbitmap(icon_path)
startup_window.title("Welcome to UPE")
center_window(startup_window, 480, 480)

# Load the image using PIL
startup_image = Image.open(opening_image_path)
resized_startup_image = startup_image.resize((480, 480))  # Resize if needed

# Convert the image to a Tkinter-compatible format
tk_startup_image = ImageTk.PhotoImage(resized_startup_image)

# Create a label with the resized image
image_label = tk.Label(startup_window, image=tk_startup_image)
image_label.image = tk_startup_image
image_label.pack()

# Simulate a 4-second delay for the startup screen
startup_window.after(1000, lambda: [startup_window.destroy(), open_login_window()])

# Start the main event loop
root.mainloop()
