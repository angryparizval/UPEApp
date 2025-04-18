import tkinter as tk
from tkinter import ttk
import os
import subprocess
import sys
from utils import center_window
from PIL import Image, ImageTk
from utils import resource_path

icon_path = resource_path("Image/icon.ico")
banner_image_path = resource_path('Image/UPE-banner.png')

# Function to open files
def open_file(filename):
    # Exception handling for opening files
    try:
        # Windows
        if sys.platform.startswith("win"):
            os.startfile(filename)  
        # macOS
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", filename])
        # Linux
        else:
            subprocess.run(["xdg-open", filename])  
    # Exception handling for unknown OS
    except Exception as e:
        print(f"Error opening file: {e}")

# Function to open the UPE Information window
def open_upe_information(homepage_window, root):
    homepage_window.withdraw()
    
    # Create the UPE Information window
    upe_information_window = tk.Toplevel(root)
    upe_information_window.iconbitmap(icon_path)
    upe_information_window.title("UPE Information")
    center_window(upe_information_window, 1200, 750)
    upe_information_window.configure(background="#52101a")

    # Load the image using Pillow
    upe_information_window.image_ref = Image.open(banner_image_path)

    # Resize the image (scale it down to 1/3 of the original size)
    resized_image = upe_information_window.image_ref.resize((upe_information_window.image_ref.width // 3, upe_information_window.image_ref.height // 3))

    # Convert the resized image to a Tkinter-compatible format
    tk_image = ImageTk.PhotoImage(resized_image)

    # Create a label with the resized image
    image_label = tk.Label(upe_information_window, image=tk_image)
    image_label.image = tk_image  # Keep a reference to the image
    image_label.pack()

    # Header label
    label = tk.Label(upe_information_window, text="UPE Information",  font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=10)

    # Main frame to organize content (Grid Layout)
    main_frame = tk.Frame(upe_information_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Left frame for Faculty & Alumni
    left_frame = tk.Frame(main_frame)
    left_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=10)

    # Center frame for Undergraduate Students (2 columns)
    center_frame = tk.Frame(main_frame)
    center_frame.grid(row=0, column=1, sticky="n", padx=20, pady=10)

    # Right frame for Buttons (inside the same main frame)
    right_frame = tk.Frame(main_frame)
    right_frame.grid(row=0, column=2, sticky="ne", padx=20, pady=10)

    # Name lists
    charter_faculty = [
        "Dr. Bjarne Berg", "Dr. Sarah Caudill", "Dr. Ajay Kumara", "Dr. Shaun Williams"
    ]
    
    charter_alumni = [
        "Eric Boston", "Claire Cook (Neibergal)", "Nolan Garrett",
        "Sean Incardona", "Brett Vogelsang"
    ]
    
    charter_undergrad_students = [
        "Hunter Adkins", "Vanessa Bartolo", "Madeline Blackwell", "Christopher Drum",
        "Katelynn Grimes", "Joseph Hartness", "Nicholas Hudler", "Brian Kirkland",
        "James Maennle", "Ringo Nguyen", "Spencer Prather", "Aubrie Pressley",
        "Alexander Schlosser", "Monte Scott", "Jordan Shealey", "Kamron Sigmon",
        "Matthew Spivey", "Christian Thompson", "Logan Traxler"
    ]

    # Function to display names in a single column
    def display_names(title, names, parent):
        title_label = tk.Label(parent, text=title, font=("Helvetica", 17, "bold"))
        title_label.pack(anchor="w", padx=10, pady=2)
        for name in names:
            name_label = tk.Label(parent, text=name, font=("Helvetica", 15))
            name_label.pack(anchor="w", padx=30)

    # Function to display undergraduate students in two columns but keeping alphabetical order
    def display_names_two_columns(title, names, parent):
        title_label = tk.Label(parent, text=title, font=("Helvetica", 17, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=5)
       
        # First half
        col1 = names[:len(names)//2] 
        # Second half
        col2 = names[len(names)//2:]  
        
        for i, name in enumerate(col1):
            name_label = tk.Label(parent, text=name, font=("Helvetica", 15))
            name_label.grid(row=i+1, column=0, sticky="w", padx=20, pady=2)

        for i, name in enumerate(col2):
            name_label = tk.Label(parent, text=name, font=("Helvetica", 15))
            name_label.grid(row=i+1, column=1, sticky="w", padx=20, pady=2)

    # Display the lists in respective frames
    display_names("Charter Faculty:", charter_faculty, left_frame)
    display_names("Charter Alumni:", charter_alumni, left_frame)
    display_names_two_columns("Charter Undergraduate Students:", charter_undergrad_students, center_frame)

    # Buttons in the right frame
    ttk.Button(right_frame, text="Back to Homepage", command=lambda: [upe_information_window.destroy(), homepage_window.deiconify()]).pack(pady=5, fill="x")
    ttk.Button(right_frame, text="Open LRU bylaws PDF", command=lambda: open_file(resource_path("PDF/LRU_bylaws.pdf"))).pack(pady=5, fill="x")
    ttk.Button(right_frame, text="Open LRU Constitution PDF", command=lambda: open_file(resource_path("PDF/LRU_Constitution.pdf"))).pack(pady=5, fill="x")
    ttk.Button(right_frame, text="Open UPE Infographic PDF", command=lambda: open_file(resource_path("PDF/UPE_Infographic_2022.pdf"))).pack(pady=5, fill="x")
