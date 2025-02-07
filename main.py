#packages needed to run the application
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkinter import PhotoImage
from reportlab. lib. enums import TA_JUSTIFY, TA_CENTER 
from reportlab. lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image 
from reportlab. lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Function to center a window on your screen when oeining the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

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
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to open the homepage
def open_homepage():
    #global variables
    global homepage_window, homepage_image

    # Destroy the login window
    if login_window.winfo_exists():
        login_window.destroy()

    # Create the homepage window
    homepage_window = tk.Toplevel(root)
    homepage_window.title("Homepage")
    center_window(homepage_window, 550, 360)

    # Load the image and keep a reference to it
    homepage_image = PhotoImage(file="UPE-background.png")
    resized_image = homepage_image.subsample(2, 2)

    # Create a label with the resized image
    image_label = tk.Label(homepage_window, image=resized_image)
    # Keep a reference to avoid garbage collection
    image_label.image = resized_image
    image_label.pack()

    # Add buttons to open the upe budget window, view records window,and exit the application
    btn_upe_budget_window = ttk.Button(homepage_window, text="UPE Budget", command=open_upe_budget)
    btn_upe_budget_window.pack(pady=10)

    btn_open_view_records_window = ttk.Button(homepage_window, text="View Records", command=open_view_records)
    btn_open_view_records_window.pack(pady=10)

    btn_open_invitation_report_window = ttk.Button(homepage_window, text="Create Invitation", command=open_invitation_report_window)
    btn_open_invitation_report_window.pack(pady=10)

    btn_exit = ttk.Button(homepage_window, text="Exit Application", command=root.quit)
    btn_exit.pack(pady=10)

# opening UPE budget window
def open_upe_budget():
    # Hide the homepage window
    homepage_window.withdraw()
    upe_budget_window = tk.Toplevel(root)
    upe_budget_window.title("UPE Budget")
    center_window(upe_budget_window, 300, 200)

    #sample for rn
    label = tk.Label(upe_budget_window, text="This is Window UPE BUDGET")
    label.pack(pady=50)

    # Table view of the budget records

    #button or datafields to enter a transaction

    # Button to go back to the homepage
    btn_homepage_window = ttk.Button(upe_budget_window, text="Back to Homepage", command=lambda: [upe_budget_window.destroy(), homepage_window.deiconify()])
    btn_homepage_window.pack(pady=10)

def open_invitation_report_window():
    # Hide the homepage window
    homepage_window.withdraw()
    invitation_report_window = tk.Toplevel(root) 
    invitation_report_window.title("Invitation Report")
    center_window(invitation_report_window, 500, 300)
    label = tk.Label(invitation_report_window, text = "This is UPE Records")
    label.pack(pady=50)

    #search student to generate report and confirms selects report button

    #grabs the first name and last name from database and stores in variable for use
    #FirstName = 
    #LastName = 

    #button to generate the report and print it to a PDF
    btn_report = ttk.Button(invitation_report_window, text="Generate PDF Report", command=generate_pdf_report)
    btn_report.pack(pady=20)
    

    # Button to go back to the homepage
    btn_homepage_window = ttk.Button(invitation_report_window, text="Back to Homepage", command=lambda: [invitation_report_window.destroy(), homepage_window.deiconify()])
    btn_homepage_window.pack(pady=10)


def generate_pdf_report():
    # Create a PDF file
    pdf_filename = "Invitation_report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=12, leftMargin=12, topMargin=12, bottomMargin=6)
    
    # Create a list to hold the content
    document = []
    
    # Add the image
    image_path = "UPE-shortbanner.jpg"  # Ensure the image file exists in the same directory
    document.append(Image(image_path, width=6.1*inch, height=2.0*inch, hAlign=TA_CENTER))
    document.append(Spacer(1, 20))
    
    # Add paragraphs
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
    
    # Build the PDF
    doc.build(document)
    print(f"PDF generated successfully: {pdf_filename}")


def open_view_records():
    # Hide the homepage window
    homepage_window.withdraw()
    view_records_window = tk.Toplevel(root) 
    view_records_window.title("View Records")
    center_window(view_records_window, 300, 200)
    label = tk.Label(view_records_window, text="This is UPE Records")
    label.pack(pady=50)

    #filter combo box to filter the records by category (student, member, faculty)

    #filter out uneeded columns for a printout (specific information)

    #table view of the records

    #button to print out the records that are filtered

    # Button to go back to the homepage
    btn_homepage_window = ttk.Button(view_records_window, text="Back to Homepage", command=lambda: [view_records_window.destroy(), homepage_window.deiconify()])
    btn_homepage_window.pack(pady=10)


# Main application root window
# Create the main window using ThemedTk
root = ThemedTk()  # You can try other themes like "arc", "radiance", etc.

# Create a style object
style = ttk.Style()

# Configure the style for buttons
# background = border, active when hovered over, pressed is base color
# foreground = text, active when hovered over
style.configure('TButton', font=('Helvetica', 12), foreground='black')
style.map('TButton',background=[('active', 'black'), ('pressed', 'red')],foreground=[('active', 'red'), ('pressed', 'green')])

root.withdraw()  # Hide the root window initially

# Create the startup screen
startup_window = tk.Toplevel(root)
startup_window.title("Welcome to UPE")
center_window(startup_window, 480, 480)

# Load the image and keep a reference to it
startup_image = PhotoImage(file="UPE-opening.png")
resized_startup_image = startup_image.subsample(2, 2)

# Create a label with the resized image
image_label = tk.Label(startup_window, image=resized_startup_image)
image_label.image = resized_startup_image  # Keep a reference to avoid garbage collection
image_label.pack()

# Simulates a 4 second delay for the startup screen
startup_window.after(4000, lambda: [startup_window.destroy(), open_login_window()])

# Function to open the login window
def open_login_window():
    global login_window, entry_username, entry_password, login_image

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    center_window(login_window, 650, 450)

    # Load the image and keep a reference to it
    login_image = PhotoImage(file="UPE-logo.png")
    resized_login_image = login_image.subsample(5, 5)

    # Create a label with the resized image
    image_label = tk.Label(login_window, image=resized_login_image)
    image_label.image = resized_login_image  # Keep a reference to avoid garbage collection
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

# Start the main event loop
root.mainloop()