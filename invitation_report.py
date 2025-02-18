# invitation_report.py
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

# Dictionary to store student names for selection retrieval
student_dict = {}

#function to search the students in the data base
def search_students(event):
    query = search_var.get()
    # Clear previous search results
    listbox.delete(0, tk.END)
    # Reset dictionary
    student_dict.clear() 

    if query:
        conn = sqlite3.connect("UPEAPP.db")
        cursor = conn.cursor()
        cursor.execute("SELECT STUD_FST_NM, STUD_LST_NM FROM Student WHERE STUD_FST_NM LIKE ? OR STUD_LST_NM LIKE ?", (f"%{query}%", f"%{query}%"))
        results = cursor.fetchall()
        conn.close()

        for index, student in enumerate(results):
            full_name = f"{student[0]} {student[1]}"
            # Store in dictionary
            student_dict[index] = student 
            listbox.insert(tk.END, full_name)

def get_selected_student(event):
    """Gets the first and last name of the selected student from the listbox."""
    global first_name, last_name  # Declare them as global so they update correctly
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        first_name, last_name = student_dict.get(index, ("", ""))
        print(f"Selected Student: {first_name} {last_name}")  # Debugging output



def get_selected_date():
    global selected_date_str  # Ensure this updates globally
    selected_date_str = cal.get_date()
    date_label.config(text=f"Selected Date: {selected_date_str}")  
    calendar_window.destroy()
    invitation_report_window.deiconify()



#function to open calender
def open_calendar():
    global calendar_window
    calendar_window = tk.Toplevel()
    calendar_window.title("Select a Date")
    center_window(calendar_window, 300, 250)

    global cal
    cal = Calendar(calendar_window, selectmode="day", year=2025, month=2, day=15)
    cal.pack(pady=20)

    select_button = ttk.Button(calendar_window, text="Select Date", command = get_selected_date)
    select_button.pack(pady=10)

#function to generate pdf report
def generate_pdf_report():
    #array to store missing fields
    missing_fields = []

    # Check if a student is selected
    if not first_name or not last_name:
        missing_fields.append("Selecting a student")

    # Check if a date is selected
    if not selected_date_str:
        missing_fields.append("Selecting a Date")

    # Check if a link is entered
    form_link = link_entry.get().strip()
    if not form_link:
        missing_fields.append("Providing a form Link")

    # If any fields are missing, show an error message and return
    if missing_fields:
        messagebox.showerror("Missing Information", f"Please complete the following fields before generating the PDF:\n- " + "\n- ".join(missing_fields))
        return
    

    pdf_filename = os.path.join("InvitationOutput",first_name + '-' + last_name + "-Invitation_report.pdf")
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=12, leftMargin=12, topMargin=12, bottomMargin=6)
    document = []
    image_path = os.path.join("Image", "UPE-shortbanner.jpg")
    if os.path.exists(image_path):
        document.append(Image(image_path, width=6.1 * inch, height=2.0 * inch, hAlign=TA_CENTER))
    else:
        print(f"Warning: Image file {image_path} not found.")

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
    doc.build(document)
    print(f"PDF generated successfully: {pdf_filename}")

#main function to open invitation report window
def open_invitation_report_window(homepage_window, root):
    homepage_window.withdraw()
    global invitation_report_window
    invitation_report_window = tk.Toplevel(root)
    invitation_report_window.title("Invitation Reporting")
    center_window(invitation_report_window, 800, 670)
    label = tk.Label(invitation_report_window, text="Invitation Report", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=10)

    label = tk.Label(invitation_report_window, text= "Select a Student and Date", font=("Arial", 16))
    label.pack(pady=20)

    # Initialized global variables
    global first_name 
    first_name = ""
    global last_name
    last_name = ""
    global selected_date_str
    selected_date_str = ""

    # Search student label
    tk.Label(invitation_report_window, text="Search Student:").pack(pady=5)
    
    global search_var, listbox
    search_var = tk.StringVar()
    
    #student search entry
    studentEntry = tk.Entry(invitation_report_window, textvariable=search_var)
    studentEntry.pack(pady=5)
    studentEntry.bind("<KeyRelease>", search_students)  # Bind to real-time search

    #student selecton listbox
    listbox = tk.Listbox(invitation_report_window, height=10, width=40)
    listbox.pack(pady=10)

    # Bind the listbox selection event
    listbox.bind("<<ListboxSelect>>", get_selected_student)

    #button to open calender
    ttk.Button(invitation_report_window,text="Open Calendar", command=open_calendar).pack(pady=20)

    #selecting date label
    global date_label
    date_label= tk.Label(invitation_report_window, text="No Date Selected", font=("Arial", 12, "bold"))
    date_label.pack(pady=10)

    #link entry
    link_var = tk.StringVar()

    #label for link entry
    tk.Label(invitation_report_window, text="Enter the form link Link:").pack(pady=5)
    global link_entry

    #initialization
    link_entry = ""
    #link entry
    link_entry = tk.Entry(invitation_report_window, textvariable=link_var, width=50)
    link_entry.pack(pady=5)

    #button to generate pdf report
    btn_report = ttk.Button(invitation_report_window, text="Generate PDF Report", command=generate_pdf_report)
    btn_report.pack(pady=20)

    #button to go back to homepage
    btn_homepage_window = ttk.Button(invitation_report_window, text="Back to Homepage", command=lambda: [invitation_report_window.destroy(), homepage_window.deiconify()])
    btn_homepage_window.place(relx=0.02, rely=0.05, anchor="nw")