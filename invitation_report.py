import tkinter as tk
import sqlite3
import os
from tkinter import ttk
from utils import center_window
import tkinter.messagebox as messagebox  # Import messagebox
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from tkcalendar import Calendar
from datetime import datetime
import sys
from utils import resource_path
icon_path = resource_path("Image/icon.ico") 


# Store selected students and search results
selected_students = []
# Dictionary to store search results
student_dict = {}

# Function to get the correct path to the database (works both in development and packaged form)
def get_db_path():
    if getattr(sys, 'frozen', False):
        # If running as a bundled executable, use the path relative to the executable
        return os.path.join(sys._MEIPASS, "UPEApp.db")
    else:
        # If running from source, use the local path
        return "UPEApp.db"

# Function to search students
def search_students(event):
    query = search_var.get()
    listbox.delete(0, tk.END)
    student_dict.clear()
    
    if query:
        db_path = get_db_path()  # Get the correct DB path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT STUD_FST_NM, STUD_LST_NM FROM Student WHERE (STUD_FST_NM LIKE ? OR STUD_LST_NM LIKE ?)AND STUD_ID NOT IN (SELECT STUD_ID FROM Member)", (f"%{query}%", f"%{query}%"))
        results = cursor.fetchall()
        conn.close()
        
        # Display search results in the listbox
        for index, student in enumerate(results):
            full_name = f"{student[0]} {student[1]}"
            # Store student tuple 
            student_dict[index] = student  
            listbox.insert(tk.END, full_name)

# Function to select a student
def select_student():
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        first_name, last_name = student_dict.get(index, ("", ""))
        full_name = f"{first_name} {last_name}"
        if full_name and full_name not in selected_students:
            selected_students.append(full_name)
            selected_students_listbox.insert(tk.END, full_name)

# Function to remove a selected student
def remove_selected_student():
    selected_index = selected_students_listbox.curselection()
    if selected_index:
        selected_students.pop(selected_index[0])
        selected_students_listbox.delete(selected_index[0])

# Function to get the selected date
def get_selected_date():
    global selected_date_str
    selected_date_str = cal.get_date()
    date_label.config(text=f"Selected Date: {selected_date_str}")  
    calendar_window.destroy()
    invitation_report_window.deiconify()

# Function to open the calendar
def open_calendar():
    global calendar_window, cal
    calendar_window = tk.Toplevel()
    calendar_window.iconbitmap(icon_path)
    calendar_window.title("Select a Date")
    center_window(calendar_window, 300, 320)

    # Create the calendar and get current date
    current_date = datetime.today().strftime('%m/%d/%Y')
    cal = Calendar(calendar_window, selectmode="day", year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)
    cal.pack(pady=20)

    # Button to select the date
    select_button = ttk.Button(calendar_window, text="Select Date", command= lambda: [get_selected_date (), calendar_window.destroy()])
    select_button.pack(pady=10)

# Function to generate the PDF report
def generate_pdf_report():
    # Ensure at least one student is selected
    if not selected_students:
        messagebox.showerror("Missing Information", "Please select at least one student.")
        return
    # Ensure the date is selected
    if not selected_date_str:
        messagebox.showerror("Missing Information", "Please select a date.")
        return
    form_link = link_entry.get().strip()
    # Ensure the form link is provided
    if not form_link:
        messagebox.showerror("Missing Information", "Please enter the form link.")
        return

    # Ensure the output directory exists
    os.makedirs("InvitationOutput", exist_ok=True)

    # Loop through selected students
    for student in selected_students:
        # Split the student name into first and last name
        first_name, last_name = student.split(" ", 1)
        # Define the PDF file path
        pdf_filename = os.path.join("InvitationOutput", first_name + '-' + last_name + "-Invitation_report.pdf")
        # Create the PDF document
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=12, leftMargin=12, topMargin=12, bottomMargin=6)
        document = []
        # Add the UPE banner image
        image_path = os.path.join("Image", "UPE-shortbanner.jpg")
        # Check if the image file exists
        if os.path.exists(image_path):
            document.append(Image(image_path, width=6.1 * inch, height=2.0 * inch, hAlign=TA_CENTER))
        else:
            print(f"Warning: Image file {image_path} not found.")

        # Add the content to the PDF
        document.append(Spacer(1, 20))
        styles = getSampleStyleSheet()
        document.append(Paragraph('To: '+ first_name, styles['Normal']))
        document.append(Spacer(1, 20))
        document.append(Paragraph('Dear ' + first_name + ' ' + last_name + ',', styles['Normal']))
        document.append(Spacer(1, 20))
        document.append(Paragraph('Congratulations! We are pleased to inform you that you have been selected for membership in the LRU Chapter of Upsilon Pi Epsilon, the International Honor Society for Computing and Information disciplines. As an undergraduate student in the computing and information disciplines at Lenoir-Rhyne University, your selection has been based upon your outstanding achievement and high scholarship rating.', styles['Normal']))
        document.append(Spacer(1, 20))
        document.append(Paragraph('The Upsilon Pi Epsilon Association was founded at Texas A&M University in 1967 for students and faculty who exhibit superior scholastic and professional achievement in the computing curriculum. It remains the only National Honor Society for the computing and information disciplines and is recognized as such by the Association for Computing Machinery (ACM) and IEEE Computer Society. In 1997, Upsilon Pi Epsilon was admitted as a member of the Association of College Honor Societies - the parent organization for all academic honor societies in North America. Lenoir-Rhyne University was chartered in 2022 as the sixth chapter of the state of North Carolina to the Association by the Executive Council of Upsilon Pi Epsilon. You can learn more about UPE from its website at https://www.acm.org/upe', styles['Normal']))
        document.append(Spacer(1, 20))
        document.append(Paragraph('Membership into Upsilon Pi Epsilon will be covered by the Donald and Helen Schort School of Mathematics and Computing Sciences Fund, this fee will go directly to the International Association and includes the cost of the lifetime membership fee. Each member will receive a membership certificate, a carat clad Recognition Key (lapel pin) to signify membership, and a UPE medallion for graduation ceremonies. Members will pay a $10 annual chapter fee that will go to the chapter treasurer for the charter group activities.', styles['Normal']))
        document.append(Spacer(1, 20))
        document.append(Paragraph('ACM now provides free ACM student memberships to active members of UPE for one year, which includes subscriptions to Communications of the ACM, ACMs Digital Library, and more.', styles['Normal']))
        document.append(Spacer(1, 20))
        document.append(Paragraph('An in-person initiation ceremony will be scheduled for a date to be determined in November. We will have an informal gathering and then the ceremony. Total this should last approximately 50 minutes. We will make plans to provide online access to the ceremony for alumni inductees unable to attend in person.', styles['Normal']))
        document.append(Spacer(1, 20))
        document.append(Paragraph('To accept your invitation into the Lenoir-Rhyne Chapter of Upsilon Pi Epsilon, please do complete this form no later than ', styles['Normal']))
        document.append(Paragraph(selected_date_str, styles['Heading2']))
        document.append(Spacer(1, 10))
        document.append(Paragraph('Visit this form ('+ link_entry.get() +') provide us with some information, including a picture of yourself to be used in the ceremony, the way you want your name to show on your membership certificate, phonetic pronunciation for your name as needed, and the name of your home town.', styles['Normal']))
        document.append(Spacer(1, 20))
        document.append(Paragraph('Once again, congratulations, and we hope you will accept this opportunity to become a member of this prestigious Honor Society for the computing and information disciplines. Should you have any problems or questions, feel free to contact me. (Students unable to attend the ceremony may choose to join now and be initiated at our next ceremony)', styles['Normal']))
        # Build the PDF document
        doc.build(document)
        # Print success message
        print(f"PDF generated successfully: {pdf_filename}")

# Function to generate the TXT report
def generate_txt_report():
    # Array to store missing fields
    if not selected_students:
        messagebox.showerror("Missing Information", "Please select at least one student.")
        return
    if not selected_date_str:
        messagebox.showerror("Missing Information", "Please select a date.")
        return
    form_link = link_entry.get().strip()
    if not form_link:
        messagebox.showerror("Missing Information", "Please enter the form link.")
        return

    # Ensure the output directory exists
    output_dir = "InvitationOutput"
    os.makedirs(output_dir, exist_ok=True)

    # Loop through selected students
    for student in selected_students:
        first_name, last_name = student.split(" ", 1)
        # Define the TXT file path
        txt_filename = os.path.join(output_dir, f"{first_name}-{last_name}-Invitation_report.txt")

        # Create the content
        content = f"""To: {first_name}

Dear {first_name} {last_name},

    Congratulations! We are pleased to inform you that you have been selected for membership in the LRU Chapter of Upsilon Pi Epsilon, the International Honor Society for Computing and Information disciplines. As an undergraduate student in the computing and information disciplines at Lenoir-Rhyne University, your selection has been based upon your outstanding achievement and high scholarship rating.

    The Upsilon Pi Epsilon Association was founded at Texas A&M University in 1967 for students and faculty who exhibit superior scholastic and professional achievement in the computing curriculum. It remains the only National Honor Society for the computing and information disciplines and is recognized as such by the Association for Computing Machinery (ACM) and IEEE Computer Society. In 1997, Upsilon Pi Epsilon was admitted as a member of the Association of College Honor Societies - the parent organization for all academic honor societies in North America. Lenoir-Rhyne University was chartered in 2022 as the sixth chapter of the state of North Carolina to the Association by the Executive Council of Upsilon Pi Epsilon. You can learn more about UPE from its website at https://www.acm.org/upe.

    Membership into Upsilon Pi Epsilon will be covered by the Donald and Helen Schort School of Mathematics and Computing Sciences Fund. This fee will go directly to the International Association and includes the cost of the lifetime membership fee. Each member will receive a membership certificate, a carat clad Recognition Key (lapel pin) to signify membership, and a UPE medallion for graduation ceremonies. Members will pay a $10 annual chapter fee that will go to the chapter treasurer for the charter group activities.

    ACM now provides free ACM student memberships to active members of UPE for one year, which includes subscriptions to Communications of the ACM, ACM's Digital Library, and more.

    An in-person initiation ceremony will be scheduled for a date to be determined in November. We will have an informal gathering and then the ceremony. This should last approximately 50 minutes. We will make plans to provide online access to the ceremony for alumni inductees unable to attend in person.

    To accept your invitation into the Lenoir-Rhyne Chapter of Upsilon Pi Epsilon, please complete this form no later than {selected_date_str}.

    Visit this form ({form_link}) to provide us with some information, including a picture of yourself to be used in the ceremony, the way you want your name to show on your membership certificate, phonetic pronunciation for your name as needed, and the name of your hometown.

    Once again, congratulations, and we hope you will accept this opportunity to become a member of this prestigious Honor Society for the computing and information disciplines. Should you have any problems or questions, feel free to contact me. (Students unable to attend the ceremony may choose to join now and be initiated at our next ceremony.)
        """

        # Write to the TXT file
        with open(txt_filename, "w", encoding="utf-8") as txt_file:
            txt_file.write(content)

        # Print success message
        print(f"TXT generated successfully: {txt_filename}")

#main window
def open_invitation_report_window(homepage_window, root):
    homepage_window.withdraw()
    global invitation_report_window, search_var, listbox, selected_students_listbox, date_label, link_entry, selected_date_str
    invitation_report_window = tk.Toplevel(root)
    invitation_report_window.iconbitmap(icon_path)
    invitation_report_window.title("Invitation Reporting")
    center_window(invitation_report_window, 800, 670)
    invitation_report_window.configure(background="#52101a")

    # Header label
    tk.Label(invitation_report_window, text="Invitation Report", font=("Helvetica", 30, "bold")).pack(pady=10)
    tk.Label(invitation_report_window, text="Search Student:",font=("Helvetica", 18), bg="#52101a", fg="white").pack(pady=5)

    #Entry for searching students
    search_var = tk.StringVar()
    student_entry = ttk.Entry(invitation_report_window, textvariable=search_var)
    student_entry.pack(pady=5)

    # Bind the search function to the entry
    student_entry.bind("<KeyRelease>", search_students)

    # Frame to hold both listboxes and buttons
    listbox_frame = tk.Frame(invitation_report_window)
    listbox_frame.pack(pady=10)

    # Listbox for search results
    listbox = tk.Listbox(listbox_frame, height=10, width=40)
    listbox.grid(row=0, column=0, padx=10, pady=(0, 5)) 

    # Listbox for selected students
    selected_students_listbox = tk.Listbox(listbox_frame, height=10, width=40)
    selected_students_listbox.grid(row=0, column=1, padx=10, pady=(0, 5))

    # Button to select a student (centered under the first listbox)
    select_button = ttk.Button(listbox_frame, text="Select Student", command=select_student)
    select_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    # Button to remove a student (centered under the second listbox)
    remove_button = ttk.Button(listbox_frame, text="Remove Selected", command=remove_selected_student)
    remove_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Ensure buttons stretch to match listbox width
    listbox_frame.columnconfigure(0, weight=1)
    listbox_frame.columnconfigure(1, weight=1)

    # Button to open the calendar
    ttk.Button(invitation_report_window, text="Select Reply by Date", command=open_calendar).pack(pady=10)
    date_label = tk.Label(invitation_report_window, text="No Date Selected", font=("Helvetica", 18, "bold"), bg="#52101a", fg="white")
    date_label.pack(pady=10)

    # Entry for form link
    tk.Label(invitation_report_window, text="Enter Form Link:",font=("Helvetica", 15), bg="#52101a", fg="white").pack()
    link_entry = ttk.Entry(invitation_report_window, width=50)
    link_entry.pack(pady=5)

    # Create a frame to hold the buttons
    button_frame = tk.Frame(invitation_report_window, bg="#52101a")
    button_frame.pack(pady=20)

    # Button to generate PDF report
    ttk.Button(button_frame, text="Generate .pdf Report", command=generate_pdf_report).pack(side=tk.LEFT, padx=10)

    # Button to generate TXT report
    ttk.Button(button_frame, text="Generate a .txt Report", command=generate_txt_report).pack(side=tk.RIGHT, padx=10)

    ttk.Button(invitation_report_window, text="Back to Homepage", command=lambda: [invitation_report_window.destroy(), homepage_window.deiconify()]).place(relx=0.02, rely=0.05)
