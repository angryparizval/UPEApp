# records_actions.py
import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from utils import center_window
from tkinter import Canvas
from PIL import Image, ImageTk
import datetime
import calendar
import re

'''
======================
GENERAL USE FUNCTIONS
======================
'''

#global variables
conn = None
selected_date_str = ""

#Function to get connection to db
def get_db_connection():
    #returns gloval database connection
    global conn
    if conn is None:
        conn = sqlite3.connect("UPEApp.db")
    return conn

#Function to close connection if open
def close_db_connection():
    global conn
    if conn:
        conn.close()
        conn = None

#function to grab data from Member table and return it
def fetch_member_data():
    #creates connection
    conn = get_db_connection()
    cursor = conn.cursor()
    #grabs all columns
    cursor.execute("SELECT MEM_ID, STUD_ID, MEM_DOB, MEM_ENTRY_YR, MEM_STATUS, MEM_POS, MEM_PST_POS, MEM_PHO_NO, MEM_ABROAD_ST, MEM_COMMUTE_ST, MEM_MEETING_MISD, MEM_MEETING_MISD_DESC, MEM_PREFR_NAME FROM Member")
    #grabs all rows from related columns and returns it
    rows = cursor.fetchall()
    return rows

#function to grab data from Student table and return it
def fetch_student_data():
    #creates connection
    conn = get_db_connection()
    cursor = conn.cursor()
    #grabs all columns
    cursor.execute("SELECT STUD_ID, STUD_FST_NM, STUD_LST_NM, STUD_MID_NM, STUD_EMAIL_ADD, STUD_CLASS_LVL, STUD_CURRICULUM, STUD_DEG, STUD_CUM_GPA, STUD_TRANS_CRED, STUD_EARNED_CRED, STUD_TOT_CRED, STUD_BEL_30_LR_CRED_IN, STUD_BEL_3_GPA_IN, STUD_INV_STATUS FROM Student")
    rows = cursor.fetchall()
    return rows










'''
======================================
MAIN RECORDS ACTIONS WINDOW FUNCTIONS
======================================
'''

# Window to select which records and if the user wants to edit or view
def open_records_act(homepage_window, root):

    # Withdraws homepage
    homepage_window.withdraw()
    
    global records_act_window
    records_act_window = tk.Toplevel(root)
    records_act_window.title("Select Records Action")
    center_window(records_act_window, 950,700)

    #sets background to maroon color
    records_act_window.configure(background="#52101a")

    #Top title of records
    label = tk.Label(records_act_window, text="Records", font=("Helvetica", 40, "bold"), bg="white", fg="black",bd=2, relief="solid", padx=10)
    label.pack(pady=50)

    #button to move to view records window
    btn_view_records_window = tk.Button(records_act_window, text="View Records", bg="black", fg="white", highlightcolor="gray", font=("Franklin Gothic URW", 20, "bold"),width=15, height=2, padx=1, pady=1, command=lambda: open_view_records(root))
    btn_view_records_window.pack(pady=15)
    #creates the hover over effect, turning the button grey when the mouse is over it, and back to black else
    btn_view_records_window.bind("<Enter>", lambda event : btn_view_records_window.config(bg="grey"))
    btn_view_records_window.bind("<Leave>", lambda event : btn_view_records_window.config(bg="black")) 

    #button to move to add members windows
    btn_add_members_window = tk.Button(records_act_window, text="Add Member", bg="black", fg="white", highlightbackground="gray", font=("Franklin Gothic URW", 20, "bold"),width=15, height=2, padx=1, pady=1, command=lambda: open_search_student(root))
    btn_add_members_window.pack(pady=15)
    #creates the hover over effect, turning the button grey when the mouse is over it, and back to black else
    btn_add_members_window.bind("<Enter>", lambda event : btn_add_members_window.config(bg="grey"))
    btn_add_members_window.bind("<Leave>", lambda event : btn_add_members_window.config(bg="black"))  

    #button to move to add students window
    btn_add_student_window = tk.Button(records_act_window, text="Add Student", bg="black", fg="white", highlightbackground="gray", font=("Franklin Gothic URW", 20, "bold"),width=15, height=2, padx=1, pady=1, command=lambda: open_add_student(root))
    btn_add_student_window.pack(pady=15)
    #creates the hover over effect, turning the button grey when the mouse is over it, and back to black else
    btn_add_student_window.bind("<Enter>", lambda event : btn_add_student_window.config(bg="grey"))
    btn_add_student_window.bind("<Leave>", lambda event : btn_add_student_window.config(bg="black")) 

    #button to return to homepage
    btn_rtn_homepage_window = tk.Button(records_act_window, text="Back to Homepage", bg="black", fg="white", width=17, height=3, highlightbackground="gray", font=("Franklin Gothic URW", 10, "bold"), command=lambda: [close_db_connection(), records_act_window.destroy(), homepage_window.deiconify()])
    btn_rtn_homepage_window.place(relx=0.05, rely=0.05, anchor="nw")  # Top-Left
    #creates the hover over effect, turning the button grey when the mouse is over it, and back to black else
    btn_rtn_homepage_window.bind("<Enter>", lambda event : btn_rtn_homepage_window.config(bg="grey"))
    btn_rtn_homepage_window.bind("<Leave>", lambda event : btn_rtn_homepage_window.config(bg="black")) 

    







'''
============================
ADD MEMBER WINDOW FUNCTIONS
============================
'''
#function to validate phone number against format
def validate_phone_number(phone_number):
    #regular expression to check for the format (xxx)xxx-xxxx
    pattern = r"^\(\d{3}\)\d{3}-\d{4}$"
    
    #if it matches returns true else false
    if re.match(pattern, phone_number):
        return True
    else:
        return False

#function to send data when the user hits submit
def send_member_data(txtMemStudID, dob_var, txtMemEntryYr, txtMemStatus, txtMemPos, phoNo_var, txtMemAbrStatus, txtMemComStatus, txtMemPreferNm, conn):
    
    cursor = conn.cursor()

    dob=datetime.date.today()

    #try-catch to find any invalid dates inputted
    try:
        #splits input into of date into year, month and day variables
        year, month, day = map(int, dob_var.get().split('-'))

        #check if month is between 1-12
        if month < 1 or month > 12:
            raise ValueError("Month should be between 1 and 12.")

        #check if day is valid for the given month and year
        days_in_month = calendar.monthrange(year, month)[1]
        if day < 1 or day > days_in_month:
            raise ValueError(f"{month}/{year} has only {days_in_month} days.")

        #if date makes it through checks create dob object
        dob = datetime.date(year, month, day)

    except ValueError as e:
        messagebox.showerror("Error", f"Invalid date: {str(e)}")
        return

    #check to see if date entered is in the future
    if dob > datetime.date.today():
        messagebox.showerror("Error", "Please input a valid birthdate (cannot be in the future).")
        return
    
    #checks to make sure phonenumber is correct number of values
    if(validate_phone_number(phoNo_var.get()) == False):
        messagebox.showerror("Error", "Invalid Phone Number")
        return

    #checks to make sure all fields have information inputted into them
    if(dob_var.get()== "YYYY-MM-DD" or phoNo_var.get() == "(xxx)xxx-xxxx" or txtMemStudID.get() == "Select Status" or txtMemEntryYr.get() == "Select Year" or txtMemStatus.get() == "Select Status" or txtMemPos.get() == "Select Position" or txtMemAbrStatus.get() == "Select Status" or txtMemComStatus.get() == "Select Status"):
        messagebox.showerror("Error", "All fields must be filled")
        return

    #finds the last mem_id value and adds one to it
    cursor.execute("SELECT COALESCE(MAX(MEM_ID), 0) + 1 FROM Member")
    memId = cursor.fetchone()[0]

    mem_prefer_nm = txtMemPreferNm.get()
    if(txtMemPreferNm.get() == ""):
        mem_prefer_nm = None

    #insert command to send data to db
    cursor.execute("""
        INSERT INTO Member (MEM_ID, STUD_ID, MEM_DOB, MEM_ENTRY_YR, MEM_STATUS, MEM_POS, MEM_PST_POS, MEM_PHO_NO, MEM_ABROAD_ST, MEM_COMMUTE_ST, MEM_MEETING_MISD, MEM_MEETING_MISD_DESC, MEM_PREFR_NAME) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        (memId, txtMemStudID.get(), dob_var.get(), txtMemEntryYr.get(), txtMemStatus.get(), txtMemPos.get(), None, phoNo_var.get(), txtMemAbrStatus.get(), txtMemComStatus.get(), None, None, mem_prefer_nm))

    #commit changes
    conn.commit()
    
    #sends message to let user know if everything worked correctly
    messagebox.showinfo("Success","Member Succesfully Added")
    records_act_window.deiconify

#function to get the selected date
def get_selected_date(cal, lblSelectedDate):
    selected_date_str = "No Date Selected"
    selected_date_str = cal.get_date()
    lblSelectedDate.config(text=f"Selected Date: {selected_date_str}")

#function to run search query in database
def search_students():
    query = search_var.get()
    
    #gets connection to DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT STUD_ID, STUD_FST_NM, STUD_LST_NM FROM Student WHERE STUD_ID LIKE ? OR STUD_FST_NM LIKE ? OR STUD_LST_NM LIKE ?", 
                   (f"%{query}%", f"%{query}%", f"%{query}%"))
    #fetches all results
    results = cursor.fetchall()

    #deletes previous results
    student_listbox.delete(0, tk.END)
    #inserts all matching student information from query
    for student in results:
        student_listbox.insert(tk.END, f"{student[0]} {student[1]} {student[2]}")

#function for when user selects student
def select_student(root):
    #grabs active selected student
    selected = student_listbox.get(tk.ACTIVE)
    #if something is selected split the student_
    if selected:
        #extracts all 3 parts from query so they can be sent to next window
        student_id = selected.split()[0]  
        student_first = selected.split()[1]
        student_last = selected.split()[2]

        #gets connection to DB
        conn = get_db_connection()
        cursor = conn.cursor()

        #checks to make sure that a member with the selected student id doesnt exist already
        #searchs for a member with a matching stud_id, if it finds it returns 1
        cursor.execute("SELECT 1 FROM Member WHERE STUD_ID = ?", (student_id,))
        exists = cursor.fetchone()
        #if member already exists gives error message and doesnt move forward
        if exists:
            messagebox.showerror("Error", "Member with that student ID already exists")
            return

        records_act_window.withdraw()
        #opens add member window
        open_add_member(root, student_id, student_first, student_last, conn)
        

#function to open search student window
def open_search_student(root):
    global search_window, search_var, student_listbox
    
    #creates window, centers it and gives it a title
    search_window = tk.Toplevel(root)
    center_window(search_window, 600, 400)
    search_window.title("Search Students")
    search_window.configure(background="#52101a")

    #header for top of page
    label = tk.Label(search_window, text="Find Student", font=("Helvetica", 20, "bold"),bd=2, relief="solid", padx=10)
    label.pack(pady=10)

    #creates the serach box that allows string input
    search_var = tk.StringVar()
    #based on entry send to search window
    search_entry = ttk.Entry(search_window, textvariable=search_var, width=40)
    search_entry.pack(pady=5)
    #send to search window each time a button is released
    search_entry.bind("<KeyRelease>", lambda event: search_students())

    #creates a listbox for results of search
    student_listbox = tk.Listbox(search_window, width=50, height=10)
    student_listbox.pack(pady=5)

    #select button that moves to next page with selected student info
    select_button = tk.Button(search_window, text="Select",  bg="black", fg="white", highlightcolor="gray", font=("Franklin Gothic URW", 15, "bold"), command= lambda: [select_student(root)] )
    select_button.pack()
    #creates the hover over effect, turning the button grey when the mouse is over it, and back to black else
    select_button.bind("<Enter>", lambda event : select_button.config(bg="grey"))
    select_button.bind("<Leave>", lambda event : select_button.config(bg="black")) 
    
    #button to return to records screen
    btn_rtn_recordsact_window = tk.Button(search_window, text="Back",  bg="black", fg="white", highlightcolor="gray", font=("Franklin Gothic URW", 15, "bold"), command=lambda: [search_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.place(relx=0.02, rely=0.05, anchor="nw")
    btn_rtn_recordsact_window.bind("<Enter>", lambda event : btn_rtn_recordsact_window.config(bg="grey"))
    btn_rtn_recordsact_window.bind("<Leave>", lambda event : btn_rtn_recordsact_window.config(bg="black"))
    

#function to op window where user will input info to add member
def open_add_member(root, student_id, student_first, student_last, conn):
    global add_member_window, txtMemStudID
    #withdraws search student window
    search_window.withdraw()

    conn = get_db_connection()

    #set column and row amount based on actual row/column amount
    total_columns = 6
    total_rows = 6

    #sets window to root,centers it and sets window title
    add_member_window = tk.Toplevel(root)
    center_window(add_member_window, 950,700)
    add_member_window.title("Add Members")

    
    #top header
    label = tk.Label(add_member_window, text="Add Members", font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.place(relx = .30, rely = .05, anchor="nw")

    #label for student id
    lblStudId = tk.Label(add_member_window, text="Student ID:", height=1, width=15)
    lblStudId.grid(row=1, column=0, pady=10, padx=(10, 5), sticky = "w")
    #student id textbox that is prefilled using search student returned stud_id
    txtMemStudID = tk.Entry(add_member_window, width=20)
    txtMemStudID.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="w")
    #inserts id into box
    txtMemStudID.insert(0, student_id)
    #makes it readonly so stud_id is not messed with by user
    txtMemStudID.config(state="readonly")  

    #label for student first name
    lblMemFName = tk.Label(add_member_window, text="First Name:", height=1, width=15)
    lblMemFName.grid(row=1, column=2, pady=10, padx=(10, 5), sticky = "w")
    #member first name entry field
    txtMemFName = tk.Entry(add_member_window, width=20)
    txtMemFName.grid(row=1, column=3, padx=(5, 10), pady=10, sticky="w")
    #inserts first name into box
    txtMemFName.insert(0, student_first)
    #makes box readonly so first name is not messed with by user
    txtMemFName.config(state="readonly")

    #label for student last name
    lblMemLName = tk.Label(add_member_window, text="Last Name:", height=1, width=15 )
    lblMemLName.grid(row=1, column = 4, pady=10, padx=(10, 5), sticky = "w")
    #member last name entry field
    txtMemLName = tk.Entry(add_member_window, width=20)
    txtMemLName.grid(row=1, column=5, padx=(5, 10), pady=10, sticky="w")
    #inserts last name into box
    txtMemLName.insert(0, student_last)
    #makes box readonly so first name is not messed with by user
    txtMemLName.config(state="readonly")

    #label for member dob
    lblMemDob = tk.Label(add_member_window, text="*Birthdate:", height=1, width=15)
    lblMemDob.grid(row=2, column=0, padx=(10,5), pady=10, sticky="w")
    #function for date entry that formats it with YYYY/MM/DD and auto moves cursor
    def on_dob_entry_change(*args):
        current_text = dob_var.get()
        
        #remove any non-digit characters except slashes
        numbers = [char for char in current_text if char.isdigit()]
        
        #format as YYYY/MM/DD as that is sql default date format
        formatted_text = ""
        if len(numbers) > 0:
            formatted_text += "".join(numbers[0:4]) #MM
        if len(numbers) > 4:
            formatted_text += "-" + "".join(numbers[4:6])  #/DD
        if len(numbers) > 6:
            formatted_text += "-" + "".join(numbers[6:8])  #/YYYY

        #prevent infinite loop by checking if formatted text is different
        if formatted_text != current_text:
            dob_var.set(formatted_text)

        #moves the cursor to the correct position after each numbner
        txtMemDOB.after(1, lambda: txtMemDOB.icursor(len(dob_var.get())))
    
    #stringVar to hold the date
    dob_var = tk.StringVar()
    #sets default text in the box
    dob_var.set("YYYY-MM-DD")  
    dob_var.trace_add("write", on_dob_entry_change)
    #member date of birth entry field
    txtMemDOB = tk.Entry(add_member_window, text=dob_var, width=20)
    txtMemDOB.grid(row=2, column=1, padx=(5, 10), pady=10, sticky="w")

    #label for member entry year
    lblMemEntryYr = tk.Label(add_member_window, text="*Entry Year:", height=1, width=15)
    lblMemEntryYr.grid(row=2, column=2, padx=(10,5), pady=10, sticky="w")
    #member entry year entry field
    txtMemEntryYr = tk.StringVar()
    #creates a dropdown with year options from 1900-current year
    entryYr_dropdown = ttk.Combobox(add_member_window, textvariable=txtMemEntryYr, values=list(range(datetime.datetime.now().year + 1, 1900)), state="readonly", width=20)
    #sets default text to select status
    entryYr_dropdown.set("Select Year")
    entryYr_dropdown.grid(row=2, column=3, padx=(5, 10), pady=10, sticky="w")
    
    #label for member status
    lblMemStatus = tk.Label(add_member_window, text="*Member Status:", height=1, width=15)
    lblMemStatus.grid(row=2, column=4, padx=(10,5), pady=10, sticky="w")
    #creates dropdown for status selection
    txtMemStatus = tk.StringVar()
    status_dropdown = ttk.Combobox(add_member_window, textvariable=txtMemStatus, values=["Active", "Inactive", "Alumni"], state="readonly", width=20)
    #sets default text to select status
    status_dropdown.set("Select Status")
    status_dropdown.grid(row=2, column=5, padx=(5, 10), pady=10, sticky="w")

    #label for member position
    lblMemPos = tk.Label(add_member_window, text="*Position:", height=1, width=15)
    lblMemPos.grid(row=3, column=0, padx=(10, 5), pady=10, sticky="w")
    #creates dropdown for position selection
    txtMemPos = tk.StringVar()
    pos_dropdown = ttk.Combobox(add_member_window, textvariable=txtMemPos, values=["President", "Vice President", "Secretary", "Member"], state="readonly", width=20)
    #sets default text to select status
    pos_dropdown.set("Select Position")
    pos_dropdown.grid(row=3, column=1, padx=(5, 10), pady=10, sticky="w")

    #label for member phone number
    lblMemPhoNo = tk.Label(add_member_window, text="Phone Number:", height=1, width=15)
    lblMemPhoNo.grid(row=3, column=2, padx=(10,5), pady=10, sticky="w")
    #function for date entry that formats it with YYYY/MM/DD and auto moves cursor
    def on_phoNo_entry_change(*args):
        current_text1 = phoNo_var.get()
        
        #remove any non-digit characters except slashes
        numbers1 = [char1 for char1 in current_text1 if char1.isdigit()]
        
        #format as (xxx)xxx-xxxx 
        formatted_text1 = "("
        if len(numbers1) > 0:
            formatted_text1 += "".join(numbers1[0:3]) #(xxx)
        if len(numbers1) > 2:
            formatted_text1 += ")" + "".join(numbers1[3:6])  #xxx
        if len(numbers1) > 5:
            formatted_text1 += "-" + "".join(numbers1[6:10])  #-xxxx

        #prevent infinite loop by checking if formatted text is different
        if formatted_text1 != current_text1:
            phoNo_var.set(formatted_text1)

        #moves the cursor to the correct position after each numbner
        txtMemPhoNo.after(1, lambda: txtMemPhoNo.icursor(len(phoNo_var.get())))
    
    #stringVar to hold the phhonenumber
    phoNo_var = tk.StringVar()
    #sets default text in the box
    phoNo_var.set("(xxx)xxx-xxxx")  
    phoNo_var.trace_add("write", on_phoNo_entry_change)
    #entry box for member phone number
    txtMemPhoNo = tk.Entry(add_member_window,text=phoNo_var, width=20)
    txtMemPhoNo.grid(row=3, column=3, padx=(5,10), pady=10, sticky="w")

    #label for member abroad status
    lblMemAbrStatus = tk.Label(add_member_window, text="*Abroad Status:", height=1, width=15)
    lblMemAbrStatus.grid(row=3, column=4, padx=(10,5), pady=10, sticky="w")
    #creates dropdown for abroad status selection
    txtMemAbrStatus = tk.StringVar()
    abrStatus_dropdown = ttk.Combobox(add_member_window, textvariable=txtMemAbrStatus, values=["Y","N"], state="readonly", width=20)
    #sets default text to select status
    abrStatus_dropdown.set("Select Status")
    abrStatus_dropdown.grid(row=3, column=5, padx=(5, 10), pady=10, sticky="w")

    #label for member commuter status
    lblMemComStatus = tk.Label(add_member_window, text="*Commute Status:", height=1, width=15)
    lblMemComStatus.grid(row=4, column=0, padx=(10,5), pady=10, sticky="w")
    #creates dropdown for commuter status selection
    txtMemComStatus = tk.StringVar()
    comStatus_dropdown = ttk.Combobox(add_member_window, textvariable=txtMemComStatus, values=["Y","N"], state="readonly", width=20)
    #sets default text to select status
    comStatus_dropdown.set("Select Status")
    comStatus_dropdown.grid(row=4, column=1, padx=(5, 10), pady=10, sticky="w")

    #label for member prefer name
    lblMemPreferNm = tk.Label(add_member_window, text="Preferred Name:", height=1, width=15)
    lblMemPreferNm.grid(row=4, column=2, padx=(10,5), pady=10, sticky="w")
    #entry box for member phone number
    txtMemPreferNm = tk.Entry(add_member_window, width=20)
    txtMemPreferNm.grid(row=4, column=3, padx=(5,10), pady=10, sticky="w")
    
    #configures column spacing
    for i in range(total_columns):  
        add_member_window.columnconfigure(i, weight=0)
    for i in range(total_rows):  
        add_member_window.rowconfigure(i, weight=1)

    #button to submit all data
    btn_submit_member = ttk.Button(add_member_window, text="Submit", command=lambda: [send_member_data(txtMemStudID, dob_var, txtMemEntryYr, txtMemStatus, txtMemPos, phoNo_var, txtMemAbrStatus, txtMemComStatus, txtMemPreferNm, conn)])
    btn_submit_member.place(relx=0.88, rely=0.92, anchor="se")

    #button to return to records screen
    btn_rtn_recordsact_window = ttk.Button(add_member_window, text="Back", command=lambda: [add_member_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.place(relx=0.02, rely=0.05, anchor="nw")








'''
=============================
ADD STUDENT WINDOW FUNCTIONS
=============================
'''

def send_student_data(txtStudID, txtStudFstNm, txtStudMinit, txtStudLstNm, txtStudEmail, txtStudClassLvl, txtStudCurr, txtStudDegree, txtStudCumGPA,txtStudTransCred, txtStudEarnedCred, txtStudTotalCred, txtStudBelow30LrCred, txtStudBel3GPA, txtStudInvStatus, conn):
    cursor = conn.cursor()
    
    #patterns to check for correct formatting
    emailPattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    namePattern = r"^[a-zA-Z\s-]*$"
    gpaPattern = r"^\d\.\d{2}$"
    
    #checks first name formatting pops up error if wrong
    if(re.match(namePattern, txtStudFstNm.get()) == False or txtStudFstNm.get() == ""):
        messagebox.showerror("Error", "Please enter a valid first name")
        return
    
    #checks middle intial name formatting pops up error if wrong
    if(re.match(namePattern, txtStudMinit.get()) == False):
        messagebox.showerror("Error", "Please enter a valid middle intial (Ex: I. )")
        return

    #checks last name formatting pops up error if wrong
    if(re.match(namePattern, txtStudLstNm.get()) == False):
        messagebox.showerror("Error", "Please enter a valid last name")
        return

    #checks email formatting pops up error if wrong
    if(re.match(emailPattern, txtStudEmail.get()) == False):
        messagebox.showerror("Error", "Please enter a valid email")
        return
    
    # Validate cumulative GPA
    try:
        gpa = float(txtStudCumGPA.get())  # Convert to float
        if not re.match(gpaPattern, txtStudCumGPA.get()) or gpa < 0 or gpa > 4:
            messagebox.showerror("Error", "Please enter a valid GPA (Ex: 3.90)")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid GPA (Ex: 3.90)")
        return

    # Validate transfer credits
    try:
        trans_cred = int(txtStudTransCred.get())  # Convert to int
        if trans_cred < 0 or trans_cred > 200:
            messagebox.showerror("Error", "Please enter a valid transfer credits amount (0-200)")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid transfer credits amount (0-200)")
        return

    # Validate earned credits
    try:
        earned_cred = int(txtStudEarnedCred.get())  # Convert to int
        if earned_cred < 0 or earned_cred > 200:
            messagebox.showerror("Error", "Please enter a valid earned credits amount (0-200)")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid earned credits amount (0-200)")
        return

    # Validate total credits
    try:
        total_cred = int(txtStudTotalCred.get())  # Convert to int
        if total_cred < 0 or total_cred > 200:
            messagebox.showerror("Error", "Please enter a valid total credits amount (0-200)")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid total credits amount (0-200)")
        return

    #sets formatting of invstatus to None as that is the NULL name for sqllite
    invStatus = txtStudInvStatus.get()
    if invStatus == "N/A":
        invStatus = None

    #checks to make sure all fields have information inputted into them
    if(txtStudClassLvl.get()== "Select Class Level" or txtStudCurr.get() == "Select Curriculum" or txtStudDegree.get() == "Select Degree" or txtStudBelow30LrCred.get() == "Select Y/N" or txtStudBel3GPA.get() == "Select Y/N" or txtStudInvStatus.get() == "Select Status"):
        messagebox.showerror("Error", "All fields must be filled")
        return
    
    cursor.execute("""
                    INSERT INTO Student (STUD_ID, STUD_FST_NM, STUD_LST_NM, STUD_MID_NM, STUD_EMAIL_ADD, STUD_CLASS_LVL, STUD_CURRICULUM, STUD_DEG, STUD_CUM_GPA, STUD_TRANS_CRED, STUD_EARNED_CRED, STUD_TOT_CRED, STUD_BEL_30_LR_CRED_IN, STUD_BEL_3_GPA_IN, STUD_INV_STATUS )
                    Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (txtStudID.get(), txtStudFstNm.get(), txtStudMinit.get(), txtStudLstNm.get(), txtStudEmail.get(), txtStudClassLvl.get(), txtStudCurr.get(), txtStudDegree.get(), txtStudCumGPA.get(),txtStudTransCred.get(), txtStudEarnedCred.get(), txtStudTotalCred.get(), txtStudBelow30LrCred.get(), txtStudBel3GPA.get(), invStatus))

    conn.commit()

#function to open add student window
def open_add_student(root):
    #withdraws records_act_window
    records_act_window.withdraw()
    #sets the window variable to global to avoid having to send it around
    global add_student_window

    conn = get_db_connection()
    cursor = conn.cursor()
    
    #sets window to root,centers it and sets window title
    add_student_window = tk.Toplevel(root)
    center_window(add_student_window, 950,700)
    add_student_window.title("Add Student")
    
    
    #top window header
    label = tk.Label(add_student_window, text="Add Student", font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.place(relx = .35, rely = .05, anchor="nw")


    #set column and row amount based on actual row/column amount
    total_columns = 6
    total_rows = 10

    #finds the last mem_id value and adds one to it
    cursor.execute("SELECT COALESCE(MAX(STUD_ID), 0) + 1 FROM Student")
    stud_id = cursor.fetchone()[0]

    #label for studentid
    lblStudID = tk.Label(add_student_window, text="Student ID:", height=1, width=15)
    lblStudID.grid(row=3, column=0, padx=(10,5), pady=10, sticky="w")
    #textbox for studid
    txtStudID = tk.Entry(add_student_window, width=20)
    txtStudID.grid(row=3, column=1, padx=(5,10), pady=10, sticky="w")
    txtStudID.insert(0, stud_id)
    txtStudID.config(state="readonly")
    
    #label for student first name
    lblStudFstNm = tk.Label(add_student_window, text="*First Name:", height=1, width=15)
    lblStudFstNm.grid(row=4, column=0, padx=(10,5), pady=10, sticky="w")
    #entry field for student first name
    txtStudFstNm = tk.Entry(add_student_window, width=20)
    txtStudFstNm.grid(row=4, column=1, padx=(5,10), pady=10, sticky="w")

    #label for student middle intial
    lblStudMInit = tk.Label(add_student_window, text="*Middle Name:", height=1, width=15)
    lblStudMInit.grid(row=5, column=0, padx=(10,5), pady=10, sticky="w")
    #entry field for student middle intial
    txtStudMinit = tk.Entry(add_student_window, width=20)
    txtStudMinit.grid(row=5, column=1, padx=(5,10), pady=10, sticky="w")

    #label for student last name
    lblStudLstNm = tk.Label(add_student_window, text="*Last Name:", height=1, width=15)
    lblStudLstNm.grid(row=6, column=0, padx=(10,5), pady=10, sticky="w")
    #entry field for student first name
    txtStudLstNm = tk.Entry(add_student_window, width=20)
    txtStudLstNm.grid(row=6, column=1, padx=(5,10), pady=10, sticky="w")

    #label for student email address
    lblStudEmail = tk.Label(add_student_window, text="*Email Address:", height=1, width=15)
    lblStudEmail.grid(row=7, column=0, padx=(10,5), pady=10, sticky="w")
    #entry field for student email address
    txtStudEmail = tk.Entry(add_student_window, width=20)
    txtStudEmail.grid(row=7, column=1, padx=(5,10), pady=10, sticky="w")

    #label for student class level
    lblStudClassLvl = tk.Label(add_student_window, text="*Class Level:", height=1, width=15)
    lblStudClassLvl.grid(row=3, column=2, padx=(10,5), pady=10, sticky="w")
    #creates dropdown for class level selection
    txtStudClassLvl = tk.StringVar()
    classLvl_dropdown = ttk.Combobox(add_student_window, textvariable=txtStudClassLvl, values=["Freshman", "Sophomore", "Junior", "Senior", "Senior+"], state="readonly", width=20)
    #sets default text to select class level
    classLvl_dropdown.set("Select Class Level")
    classLvl_dropdown.grid(row=3, column=3, padx=(5, 10), pady=10, sticky="w")

    #label for student curriculum
    lblStudCurr = tk.Label(add_student_window, text="*Curriculum:", height=1, width=15)
    lblStudCurr.grid(row=4, column=2, padx=(10,5), pady=10, sticky="w")
    #creates dropdown for curriculum selection
    txtStudCurr = tk.StringVar()
    curr_dropdown = ttk.Combobox(add_student_window, textvariable=txtStudCurr, values=["BA", "BS"], state="readonly", width=20)
    #sets default text to select curriculum
    curr_dropdown.set("Select Curriculum")
    curr_dropdown.grid(row=4, column=3, padx=(5, 10), pady=10, sticky="w")

    #label for student degree
    lblStudDegree = tk.Label(add_student_window, text="*Degree:", height=1, width=15)
    lblStudDegree.grid(row=5, column=2, padx=(10,5), pady=10, sticky="w")
    #creates dropdown for degree selection
    txtStudDegree = tk.StringVar()
    degree_dropdown = ttk.Combobox(add_student_window, textvariable=txtStudDegree, values=["Computer Science", "Information Technology", "Cybersecurity"], state="readonly", width=20)
    #sets default text to select degree
    degree_dropdown.set("Select Degree")
    degree_dropdown.grid(row=5, column=3, padx=(5, 10), pady=10, sticky="w")

    #label for student cumulative gpa
    lblStudCumGPA = tk.Label(add_student_window, text="*Cumulative GPA:", height=1, width=15)
    lblStudCumGPA.grid(row=6, column=2, padx=(10,5), pady=10, sticky="w")
    #entry field for student email address
    txtStudCumGPA = tk.Entry(add_student_window, width=20)
    txtStudCumGPA.grid(row=6, column=3, padx=(5,10), pady=10, sticky="w")

    #label for student Transfer Credits
    lblStudTransCred = tk.Label(add_student_window, text="*Transfer Credits:", height=1, width=15)
    lblStudTransCred.grid(row=7, column=2, padx=(10,5), pady=10, sticky="w")
    #entry field for student transfer credits
    txtStudTransCred = tk.Entry(add_student_window, width=20)
    txtStudTransCred.grid(row=7, column=3, padx=(5,10), pady=10, sticky="w")

    #label for student earned Credits
    lblStudEarnedCred = tk.Label(add_student_window, text="*Earned Credits:", height=1, width=15)
    lblStudEarnedCred.grid(row=3, column=4, padx=(10,5), pady=10, sticky="w")
    #entry field for student transfer credits
    txtStudEarnedCred = tk.Entry(add_student_window, width=20)
    txtStudEarnedCred.grid(row=3, column=5, padx=(5,10), pady=10, sticky="w")

    #label for student Total Credits
    lblStudTotalCred = tk.Label(add_student_window, text="*Total Credits:", height=1, width=15)
    lblStudTotalCred.grid(row=4, column=4, padx=(10,5), pady=10, sticky="w")
    #entry field for student total credits
    txtStudTotalCred = tk.Entry(add_student_window, width=20)
    txtStudTotalCred.grid(row=4, column=5, padx=(5,10), pady=10, sticky="w")

    #label for below 30 lr credits indicator
    lblStudBelow30LrCred = tk.Label(add_student_window, text="*Below 30 LR Credits?:", height=1, width=15)
    lblStudBelow30LrCred.grid(row=5, column=4, padx=(10,5), pady=10, sticky="w")
    #creates dropdown for below 30 indicator selection
    txtStudBelow30LrCred = tk.StringVar()
    belowcred_dropdown = ttk.Combobox(add_student_window, textvariable=txtStudBelow30LrCred, values=["Y", "N"], state="readonly", width=20)
    #sets default text to select Y/N
    belowcred_dropdown.set("Select Y/N")
    belowcred_dropdown.grid(row=5, column=5, padx=(5, 10), pady=10, sticky="w")

    #label for below 3.0 GPA indicator
    lblStudBel3GPA = tk.Label(add_student_window, text="*Below 3.0 GPA?:", height=1, width=15)
    lblStudBel3GPA.grid(row=6, column=4, padx=(10,5), pady=10, sticky="w")
    #creates dropdown for below 3.0 GPA indicator selection
    txtStudBel3GPA = tk.StringVar()
    belowgpa_dropdown = ttk.Combobox(add_student_window, textvariable=txtStudBel3GPA, values=["Y", "N"], state="readonly", width=20)
    #sets default text to select degree
    belowgpa_dropdown.set("Select Y/N")
    belowgpa_dropdown.grid(row=6, column=5, padx=(5, 10), pady=10, sticky="w")

    #label for student invite status
    lblStudInvStatus = tk.Label(add_student_window, text="*Invite Status:", height=1, width=15)
    lblStudInvStatus.grid(row=7, column=4, padx=(10,5), pady=10, sticky="w")
    #creates dropdown for invite status selection
    txtStudInvStatus = tk.StringVar()
    invstatus_dropdown = ttk.Combobox(add_student_window, textvariable=txtStudInvStatus, values=["N/A", "Invited", "Accepted", "Declined"], state="readonly", width=20)
    #sets default text to select status
    invstatus_dropdown.set("Select Status")
    invstatus_dropdown.grid(row=7, column=5, padx=(5, 10), pady=10, sticky="w")
    
    #configures column spacing
    for i in range(total_columns):  
        add_student_window.columnconfigure(i, weight=0)
    for i in range(total_rows):  
        add_student_window.rowconfigure(i, weight=1)

    btn_submit = ttk.Button(add_student_window, text="Submit", command=lambda: [send_student_data(txtStudID, txtStudFstNm, txtStudMinit, txtStudLstNm, txtStudEmail, txtStudClassLvl, txtStudCurr, txtStudDegree, txtStudCumGPA,txtStudTransCred, txtStudEarnedCred, txtStudTotalCred, txtStudBelow30LrCred, txtStudBel3GPA, txtStudInvStatus, conn)])
    btn_submit.place(relx=0.869, rely=0.92, anchor="se")

    #button to return back to records actions screen
    btn_rtn_recordsact_window = ttk.Button(add_student_window, text="Back to Records Actions", command=lambda: [add_student_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.place(relx=0.02, rely=0.05, anchor="nw")










'''
==============================
VIEW RECORDS WINDOW FUNCTIONS
==============================
'''

entry_widget = None

#function to allow sort column by ascending or descending based on column chose
def treeview_sort_column(treeview, col, reverse):
    #gets data from tree view
    l = [(treeview.set(k, col), k) for k in treeview.get_children('')]
    l.sort(reverse=reverse, key=lambda x: (float(x[0]) if x[0].replace('.', '', 1).isdigit() else x[0].lower()))

    #rearrange cells in other columns in sorted positions
    for index, (_, k) in enumerate(l):
        treeview.move(k, '', index)

    #update column header with sorting order indicator
    treeview.heading(col, text=f"{col} {'▲' if not reverse else '▼'}", 
                        command=lambda _col=col: treeview_sort_column(treeview, _col, not reverse))


#function to update SQLite database after cell is edited
def update_database(table, column_name, new_value, primary_key_value):
    #connects to db
    conn = sqlite3.connect("UPEApp.db")  
    cursor = conn.cursor()

    #define primary key column per table
    primary_key_column = "MEM_ID" if table == "Member" else "STUD_ID"

    #sends sql query to db to update table with new info
    query = f"UPDATE {table} SET {column_name} = ? WHERE {primary_key_column} = ?"
    cursor.execute(query, (new_value, primary_key_value))
    
    conn.commit()

#function to handle double-click on a treeview table cells
def on_double_click(event):
    global entry_widget

    if entry_widget:
        entry_widget.destroy()

    #grabs cell row and column
    selected_items = tree.selection()
    if not selected_items:
        return 
    selected_item = tree.selection()[0]  
    column_id = tree.identify_column(event.x)  
    column_index = int(column_id[1:]) - 1  #convert from '#1' to index 0
    column_name = visible_columns[column_index]

    #prevent editing the primary key columns
    if column_name in ["MEM_ID", "STUD_ID"]:
        return  
    
    #get cells current value
    current_value = tree.item(selected_item, "values")[column_index]

    #create an entry widget that will allow editing cell
    entry_widget = ttk.Entry(tree)
    entry_widget.insert(0, current_value)
    entry_widget.focus()

    #get current clicked cell position and place keyboard entry widget in that position
    bbox = tree.bbox(selected_item, column_index)
    #prevents error if the column header is clicked
    if not bbox:
        return  
    x, y, width, height = bbox
    entry_widget.place(x=x, y=y, width=width, height=height)

    #binds enter button to save the edited changes
    entry_widget.bind("<Return>", lambda event: save_edit(selected_item, column_index))
    entry_widget.bind("<Escape>", lambda event: entry_widget.destroy())

#function to save edit to tree before calling update database
def save_edit(selected_item, column_index):
    global entry_widget

    new_value = entry_widget.get()
    column_name = visible_columns[column_index]  # Get column name

    #get the primary key value instead of assuming "id"
    primary_key_value = tree.item(selected_item, "values")[0]  # First column is assumed primary key

    #update database with correct primary key column
    update_database(current_table, column_name, new_value, primary_key_value)

    #update Treeview
    values = list(tree.item(selected_item, "values"))
    values[column_index] = new_value
    tree.item(selected_item, values=values)

    entry_widget.destroy()

#function to update treeview with selected table data
def update_treeview(tree, table, selected_columns, filter_col=None):
    global visible_columns, current_table
    current_table = table  #stores table name for later updates

    #clear all existing treeview data
    for item in tree.get_children():
        tree.delete(item)

    #fetch data from the selected table
    if table == "Member":
        columns = ("MEM_ID", "STUD_ID", "MEM_DOB", "MEM_ENTRY_YR", "MEM_STATUS", "MEM_POS", "MEM_PST_POS", "MEM_PHO_NO", 
                   "MEM_ABROAD_ST", "MEM_COMMUTE_ST", "MEM_MEETING_MISD", "MEM_MEETING_MISD_DESC", "MEM_PREFR_NAME")
        data = fetch_member_data()
    elif table == "Student":
        columns = ("STUD_ID", "STUD_FST_NM", "STUD_LST_NM", "STUD_MID_NM", "STUD_EMAIL_ADD", "STUD_CLASS_LVL", 
                   "STUD_CURRICULUM", "STUD_DEG", "STUD_CUM_GPA", "STUD_TRANS_CRED", "STUD_EARNED_CRED", 
                   "STUD_TOTcs_CRED", "STUD_BEL_30_LR_CRED_IN", "STUD_BEL_3_GPA_IN", "STUD_INV_STATUS")
        data = fetch_student_data()
    else:
        return  

    #apply filter if user wants
    if filter_col:
        data = [row for row in data if filter_col.lower() in str(row).lower()]

    #filter columns based on selected filter
    visible_columns = [col for col in columns if col not in selected_columns]

    #update Treeview columns
    tree["columns"] = visible_columns
    for col in visible_columns:
        tree.heading(col, text=f"{col} {'▲'}", command=lambda _col=col: treeview_sort_column(tree, _col, False))
        tree.column(col, anchor="center", width=120)

    #insert filtered data
    for row in data:
        filtered_row = [row[columns.index(col)] for col in visible_columns]
        tree.insert("", tk.END, values=filtered_row)

#middleman function to handle column selection and update Treeview
def update_selected_columns(event, tree, table, listbox, filter_col):
    selected_columns = [listbox.get(i) for i in listbox.curselection()]
    update_treeview(tree, table.get(), selected_columns, filter_col.get())

#function to update listbox based on table selection
def update_listbox(listbox, table):
    listbox.delete(0, tk.END)
    #sets columns if table is member
    if table == "Member":
        columns = ("Member ID", "Student ID", "Birthdate", "Entry Year", "Member Status", "Position", "Past Positions", "Phone Number", 
                   "Abroad Status", "Commute Status", "Meeting Missed Count", "Meeting Missed Desc.", "Preferred Name")
    #sets columns if table is student
    elif table == "Student":
        columns = ("Student ID", "First Name", "Last Name", "Middle Name", "Email Address", "Class Level", 
                   "Curriculum", "Degree", "Cumulative GPA", "Transfer Credits", "Earned Credits", 
                   "Total Credits", "Below 30 LR Credits", "Below 3.0 GPA", "Invite Status")
    #else do nothing
    else:
        return

    #insert listbox options
    for col in columns:
        listbox.insert(tk.END, col)

#function to switch tables after dropdown box selection
def switch_table(event, tree, table, listbox, filter_col):
    update_listbox(listbox, table.get())
    update_treeview(tree, table.get(), [], filter_col.get())

#function to open the View Records window
def open_view_records(root):
    global view_records_window, tree

    #sets window to root if not
    if not root:
        root = tk.Tk()

    #withdraws previous window
    records_act_window.withdraw()

    #sets records window as root
    view_records_window = tk.Toplevel(root)
    center_window(view_records_window, 1500, 650)
    view_records_window.title("View Records")
    view_records_window.configure(background="#52101a")

    #top label for window
    label = tk.Label(view_records_window, text="View Records", font=("Helvetica", 20, "bold"))
    label.pack(pady=10)

    #creates dropdown for table selection
    table = tk.StringVar()
    table_dropdown = ttk.Combobox(view_records_window, textvariable=table, values=["Member", "Student"], state="readonly")
    table_dropdown.set("Select Table")
    table_dropdown.pack(pady=10)

    #user entry box for filtering
    filter_col = tk.StringVar()
    filter_entry = ttk.Entry(view_records_window, textvariable=filter_col)
    filter_entry.pack(pady=10)
    #updates table each time user releases key
    filter_entry.bind("<KeyRelease>", lambda event: update_treeview(tree, table.get(), [], filter_col.get()))

    #listbox for column selection to apply filter
    listbox_frame = tk.Frame(view_records_window)
    listbox_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

    #label for hide columns
    listbox_label = tk.Label(listbox_frame, text="Hide Columns:")
    listbox_label.pack()

    #creates listbox
    listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=10)
    listbox.pack()

    #button to apply filtered columns selected by user
    btn_update_columns = ttk.Button(listbox_frame, text="Apply Filter", command=lambda: update_selected_columns(None, tree, table, listbox, filter_col))
    btn_update_columns.pack(pady=5)

    #creates treeview in frame form
    tree_frame = tk.Frame(view_records_window)
    tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    tree = ttk.Treeview(tree_frame, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    #Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    #Pack widgets
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #bind double-click event for editing cells
    tree.bind("<Double-1>", on_double_click)

    #binds combobox selection whenever user selects from dropdown
    table_dropdown.bind("<<ComboboxSelected>>", lambda event: switch_table(event, tree, table, listbox, filter_col))

    #button to return to records screen
    btn_rtn_recordsact_window = ttk.Button(view_records_window, text="Back to Records Actions", command=lambda: [view_records_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.place(relx=0.02, rely=0.05, anchor="nw")