# invitation_report.py
import tkinter as tk
import sqlite3
import os
from tkinter import ttk
from utils import center_window
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from tkcalendar import Calendar

#searching student from databse
def search_students(event):
    query = search_var.get()
    listbox.delete(0, tk.END)  # Clear previous search results
    
    if query:
        #connecting to database
        conn = sqlite3.connect("UPEAPP.db")  # Change to your actual DB file
        cursor = conn.cursor()
        cursor.execute("SELECT STUD_FST_NM, STUD_LST_NM FROM Student WHERE STUD_FST_NM LIKE ? OR STUD_LST_NM LIKE ?", (f"%{query}%", f"%{query}%"))
        results = cursor.fetchall()
        conn.close()

        for student in results:
            listbox.insert(tk.END, f"{student[0]} {student[1]}")


#function to get selected date from calender
def get_selected_date():
    selected_date = cal.get_date()
    date_label.config(text=f"Selected Date: {selected_date}")
    open_calendar.withdraw()

#function to open calender
def open_calendar():
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
    pdf_filename = os.path.join("InvitationOutput", "Invitation_report.pdf")
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=12, leftMargin=12, topMargin=12, bottomMargin=6)
    document = []
    
    image_path = os.path.join("Image", "UPE-shortbanner.jpg")
    if os.path.exists(image_path):
        document.append(Image(image_path, width=6.1*inch, height=2.0*inch, hAlign=TA_CENTER))
    else:
        print(f"Warning: Image file {image_path} not found.")

    document.append(Spacer(1, 20))
    styles = getSampleStyleSheet()
    document.append(Paragraph('To: Eli', styles['Normal']))
    document.append(Spacer(1, 20))
    document.append(Paragraph('Dear Eli Ledford,', styles['Normal']))
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
    document.append(Paragraph('To accept your invitation into the Lenoir-Rhyne Chapter of Upsilon Pi Epsilon, please do complete this form no later than', styles['Normal']))
    document.append(Paragraph(' INSERT DATE HERE', styles['Heading2']))
    document.append(Spacer(1, 20))
    document.append(Paragraph('Visit this form (https://forms.gle/F4quFyTbvz3egvDs9) provide us with some information, including a picture of yourself to be used in the ceremony, the way you want your name to show on your membership certificate, phonetic pronunciation for your name as needed, and the name of your home town.', styles['Normal']))
    document.append(Spacer(1, 20))
    document.append(Paragraph('Once again, congratulations, and we hope you will accept this opportunity to become a member of this prestigious Honor Society for the computing and information disciplines. Should you have any problems or questions, feel free to contact me. (Students unable to attend the ceremony may choose to join now and be initiated at our next ceremony)', styles['Normal']))

    doc.build(document)
    print(f"PDF generated successfully: {pdf_filename}")

#main function to open invitation report window
def open_invitation_report_window(homepage_window, root):
    homepage_window.withdraw()
    invitation_report_window = tk.Toplevel(root)
    invitation_report_window.title("Invitation Report")
    center_window(invitation_report_window, 800, 630)
    label = tk.Label(invitation_report_window, text="This is UPE Records")
    label.pack(pady=50)

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

    #button to open calender
    ttk.Button(invitation_report_window,text="Open Calendar", command=open_calendar).pack(pady=20)

    #selecting date label
    global date_label
    date_label= tk.Label(invitation_report_window, text="No Date Selected", font=("Arial", 12))
    date_label.pack(pady=10)

    #link entry
    link_var = tk.StringVar()

    tk.Label(invitation_report_window, text="Enter a Link:").pack(pady=5)
    link_entry = tk.Entry(invitation_report_window, textvariable=link_var, width=50)
    link_entry.pack(pady=5)

    #button to generate pdf report
    btn_report = ttk.Button(invitation_report_window, text="Generate PDF Report", command=generate_pdf_report)
    btn_report.pack(pady=20)

    #button to go back to homepage
    btn_homepage_window = ttk.Button(invitation_report_window, text="Back to Homepage", command=lambda: [invitation_report_window.destroy(), homepage_window.deiconify()])
    btn_homepage_window.place(relx=0.05, rely=0.05, anchor="nw")