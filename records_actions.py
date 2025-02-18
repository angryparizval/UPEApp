# records_actions.py
import tkinter as tk
import sqlite3
from tkinter import ttk
from ttkthemes import ThemedTk
from utils import center_window



'''
---------------------------------
GENERAL USE FUNCTIONS
--------------------------------
'''


#global connection variable
conn = None

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
-------------------------------------
MAIN RECORDS ACTIONS WINDOW FUNCTIONS
--------------------------------------
'''

# Window to select which records and if the user wants to edit or view
def open_records_act(homepage_window, root):
    # Withdraws homepage
    homepage_window.withdraw()
    
    global records_act_window
    records_act_window = tk.Toplevel(root)
    records_act_window.title("Select Records Action")
    center_window(records_act_window, 800, 630)

    #Top title of records
    label = tk.Label(records_act_window, text="Records", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.place(relx=0.5, rely=0.1, anchor="center")

    #button positions (X-shape)
    #button to move to view records window
    btn_view_records_window = ttk.Button(records_act_window, text="View Records", command=lambda: open_view_records(root))
    btn_view_records_window.place(relx=0.5, rely=0.5, anchor="center")  # Center

    #button to move to add members windows
    btn_add_members_window = ttk.Button(records_act_window, text="Add Member", command=lambda: open_add_member(root))
    btn_add_members_window.place(relx=0.35, rely=0.4, anchor="center")  # Top-left

    #button to move to edit members window
    btn_edit_members_window = ttk.Button(records_act_window, text="Edit Member", command=lambda: open_edit_member(root))
    btn_edit_members_window.place(relx=0.35, rely=0.6, anchor="center")  # Bottom-left

    #button to move to add students window
    btn_add_student_window = ttk.Button(records_act_window, text="Add Student", command=lambda: open_add_student(root))
    btn_add_student_window.place(relx=0.65, rely=0.4, anchor="center")  # Top-right

    #button to move to edit students window
    btn_edit_students_window = ttk.Button(records_act_window, text="Edit Student", command=lambda: open_edit_student(root))
    btn_edit_students_window.place(relx=0.65, rely=0.6, anchor="center")  # Bottom-right

    #button to return to homepage
    btn_rtn_homepage_window = ttk.Button(records_act_window, text="Back to Homepage", command=lambda: [close_db_connection(), records_act_window.destroy(), homepage_window.deiconify()])
    btn_rtn_homepage_window.place(relx=0.05, rely=0.05, anchor="nw")  # Top-Left


'''
------------------------------
ADD MEMBER WINDOW FUNCTIONS
------------------------------
'''

#Window where user will input info to add member
def open_add_member(root):
    #withdraws records_act_window
    records_act_window.withdraw()
    #sets the window variable to global to avoid having to send it around
    global add_member_window

    #sets window to root,centers it and sets window title
    add_member_window = tk.Toplevel(root)
    center_window(add_member_window, 800, 630)
    add_member_window.title("Add Members")
    
    #temporary label of information
    label = tk.Label(add_member_window, text="Add Members", font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=50)

    #button to return back to records actions screen
    btn_rtn_recordsact_window = ttk.Button(add_member_window, text="Back to Records Actions", command=lambda: [add_member_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.pack()


'''
------------------------------
EDIT MEMBER WINDOW FUNCTIONS
------------------------------
'''

def open_edit_member(root):
    #withdraws records_act_window
    records_act_window.withdraw()
    #sets the window variable to global to avoid having to send it around
    global edit_member_window

    #sets window to root,centers it and sets window title
    edit_member_window = tk.Toplevel(root)
    center_window(edit_member_window, 800, 630)
    edit_member_window.title("Edit Members")
    
    #temporary label of information
    label = tk.Label(edit_member_window, text="Edit Members", font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=50)

    #button to return back to records actions screen
    btn_rtn_recordsact_window = ttk.Button(edit_member_window, text="Back to Records Actions", command=lambda: [edit_member_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.pack()


'''
------------------------------
ADD STUDENT WINDOW FUNCTIONS
------------------------------
'''


def open_add_student(root):
    #withdraws records_act_window
    records_act_window.withdraw()
    #sets the window variable to global to avoid having to send it around
    global add_student_window

    #sets window to root,centers it and sets window title
    add_student_window = tk.Toplevel(root)
    center_window(add_student_window, 800, 630)
    add_student_window.title("Add Student")
    
    #temporary label of information
    label = tk.Label(add_student_window, text="Add Student", font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=50)

    #button to return back to records actions screen
    btn_rtn_recordsact_window = ttk.Button(add_student_window, text="Back to Records Actions", command=lambda: [add_student_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.pack()



'''
------------------------------
EDIT STUDENT WINDOW FUNCTIONS
------------------------------
'''


def open_edit_student(root):
    #withdraws records_act_window
    records_act_window.withdraw()
    #sets the window variable to global to avoid having to send it around
    global edit_student_window

    #sets window to root,centers it and sets window title
    edit_student_window = tk.Toplevel(root)
    center_window(edit_student_window, 800, 630)
    edit_student_window.title("Edit Student")
    
    #temporary label of information
    label = tk.Label(edit_student_window, text="Edit Student", font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=50)

    #button to return back to records actions screen
    btn_rtn_recordsact_window = ttk.Button(edit_student_window, text="Back to Records Actions", command=lambda: [edit_student_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.pack()
      


'''
------------------------------
VIEW RECORDS WINDOW FUNCTIONS
------------------------------
'''




#function to update treeview with data from the selected table
def update_treeview(tree, table, filter_col=None, sort_col = None, sort_desc=False):
    
    #clears existing data in tree
    for item in tree.get_children():
        tree.delete(item)

    #Fetch data based on table
    if table == "Member":
        columns = ("MEM_ID", "STUD_ID", "MEM_DOB", "MEM_ENTRY_YR", "MEM_STATUS", "MEM_POS", "MEM_PST_POS", "MEM_PHO_NO", "MEM_ABROAD_ST", "MEM_COMMUTE_ST", "MEM_MEETING_MISD", "MEM_MEETING_MISD_DESC", "MEM_PREFR_NAME")
        data = fetch_member_data()
    elif table == "Student":
        columns = ("STUD_ID", "STUD_FST_NM", "STUD_LST_NM", "STUD_MID_NM", "STUD_EMAIL_ADD", "STUD_CLASS_LVL", "STUD_CURRICULUM", "STUD_DEG", "STUD_CUM_GPA", "STUD_TRANS_CRED", "STUD_EARNED_CRED", "STUD_TOTcs_CRED", "STUD_BEL_30_LR_CRED_IN", "STUD_BEL_3_GPA_IN", "STUD_INV_STATUS")
        data = fetch_student_data()
    else:
        print(f"Unknown table: {table}")
        return 
    
    #apply filter if specified
    if filter_col:
        data = [row for row in data if filter_col.lower() in str(row).lower()]

    #apply sorting if specified
    if sort_col is not None:
        column_index = columns.index(sort_col)
        data.sort(key=lambda x: x[column_index], reverse=sort_desc)

    #update treeview with data
    tree["columns"] = columns

    #update treeview with data
    for row in data:
        tree.insert("", tk.END, values = row)


    #configure column width
    for col in columns: 
        tree.column(col, anchor="center", width=120)


#function to switch tables
def switch_table(event, tree, table, filter_col, sort_col, sort_desc):
    #swtiches the table based on the drop down menu
    update_treeview(tree, table.get(), filter_col.get(), sort_col.get(), sort_desc.get())




#functoin that opens the view record window
def open_view_records(root):
    global view_records_window, current_sort_col, current_sort_desc, tree

    #Initialize the Tkinter root windo
    if not root:
        root = tk.Tk()
    
    #Set up global variables before calling them
    current_sort_col = None  # Initialize the sorting column variable
    current_sort_desc = tk.BooleanVar(value=False)  # Ascending order by default

    # Withdraw the current window before opening the next
    records_act_window.withdraw()

    #sets window to root,centers it and sets window title
    view_records_window = tk.Toplevel(root)
    center_window(view_records_window, 800, 630)
    view_records_window.title("View Records")
    
    #Window header
    label = tk.Label(view_records_window, text="View Records", font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=50)

    #create a dropdown menu
    table = tk.StringVar()
    table.set("Member") #default
    table_dropdown = ttk.Combobox(view_records_window, textvariable=table, values = ["Member", "Student"])
    table_dropdown.pack(pady=10)
    table_dropdown.bind("<<ComboboxSelected>>", lambda event: switch_table(event, tree, table, filter_col))

    #create a filter entry
    filter_col = tk.StringVar()
    filter_entry = ttk.Entry(view_records_window, textvariable=filter_col)
    filter_entry.pack(pady=10)

    #function to automatically filter when typing
    def on_filter_change(event):
        update_treeview(tree, table.get(), filter_col.get())
    filter_entry.bind("<KeyRelease>", on_filter_change)

    #create a table
    tree = ttk.Treeview(view_records_window)
    tree.pack(fill=tk.BOTH, expand=True)


    # Fetch data for the first table
    update_treeview(tree, table.get(), filter_col.get(), current_sort_col, current_sort_desc.get())


    #button to return back to records actions screen
    btn_rtn_recordsact_window = ttk.Button(view_records_window, text="Back to Records Actions", command=lambda: [view_records_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.pack()

