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

#global variables
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


#function to sort column asc/desc
def treeview_sort_column(treeview, col, reverse):
    l = [(treeview.set(k, col), k) for k in treeview.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        treeview.move(k, '', index)

    # reverse sort next time
    treeview.heading(col, text=col, command=lambda _col=col: \
                 treeview_sort_column(treeview, _col, not reverse))
    
#function to update treeview with data from the selected table
def update_treeview(tree, table, selected_columns, filter_col=None):
    
    #clear existing data in tree
    for item in tree.get_children():
        tree.delete(item)

    #fetch data based on table selected
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

    #apply filter if given one by user
    if filter_col:
        data = [row for row in data if filter_col.lower() in str(row).lower()]

    #filter columns to display only selected ones
    visible_columns = [col for col in columns if col not in selected_columns]

    #update treeview with only visibl columns
    tree["columns"] = visible_columns

    #creates column heading
    for col in visible_columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    #inserts filtered data when filter applied
    for row in data:
        filtered_row = [row[columns.index(col)] for col in visible_columns]  # Keep only selected columns
        tree.insert("", tk.END, values=filtered_row)

#function to handle listbox selection and update treeview
def update_selected_columns(event, tree, table, listbox, filter_col):
    selected_columns = [listbox.get(i) for i in listbox.curselection()]
    update_treeview(tree, table.get(), selected_columns, filter_col.get())

#function to update listbox based on table selection
def update_listbox(listbox, table):
    listbox.delete(0, tk.END)
    if table == "Member":
        columns = ("MEM_ID", "STUD_ID", "MEM_DOB", "MEM_ENTRY_YR", "MEM_STATUS", "MEM_POS", "MEM_PST_POS", "MEM_PHO_NO", 
                   "MEM_ABROAD_ST", "MEM_COMMUTE_ST", "MEM_MEETING_MISD", "MEM_MEETING_MISD_DESC", "MEM_PREFR_NAME")
    elif table == "Student":
        columns = ("STUD_ID", "STUD_FST_NM", "STUD_LST_NM", "STUD_MID_NM", "STUD_EMAIL_ADD", "STUD_CLASS_LVL", 
                   "STUD_CURRICULUM", "STUD_DEG", "STUD_CUM_GPA", "STUD_TRANS_CRED", "STUD_EARNED_CRED", 
                   "STUD_TOTcs_CRED", "STUD_BEL_30_LR_CRED_IN", "STUD_BEL_3_GPA_IN", "STUD_INV_STATUS")
    else:
        return

    for col in columns:
        listbox.insert(tk.END, col)

#middle man function to allow for event press of selecting/switch table
def switch_table(event, tree, table, listbox, filter_col):
    update_listbox(listbox, table.get())
    update_treeview(tree, table.get(), [], filter_col.get())

#functoin that opens the view record window
def open_view_records(root):
    global view_records_window, tree

    #initialize the Tkinter root window
    if not root:
        root = tk.Tk()

    #withdraw the current window before opening the next
    records_act_window.withdraw()

    #create new window
    view_records_window = tk.Toplevel(root)
    center_window(view_records_window, 1500, 650)
    view_records_window.title("View Records")

    #window header
    label = tk.Label(view_records_window, text="View Records", font=("Helvetica", 20, "bold"))
    label.pack(pady=10)

    #dropdown to select table user wishes to see
    table = tk.StringVar()
    table_dropdown = ttk.Combobox(view_records_window, textvariable=table, values=["Member", "Student"], state="readonly")
    table_dropdown.set("Select Table")
    table_dropdown.pack(pady=10)

    #entrybox for user to input filter
    filter_col = tk.StringVar()
    filter_entry = ttk.Entry(view_records_window, textvariable=filter_col)
    filter_entry.pack(pady=10)
    #when key is released it updates the table
    filter_entry.bind("<KeyRelease>", lambda event: update_treeview(tree, table.get(), [], filter_col.get()))

    #create a listbox for column selection
    listbox_frame = tk.Frame(view_records_window)
    listbox_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

    #label for hide columns
    listbox_label = tk.Label(listbox_frame, text="Hide Columns:")
    listbox_label.pack()
    
    #label
    listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=10)
    listbox.pack()

    #button to update column visibility
    btn_update_columns = ttk.Button(listbox_frame, text="Apply Filter", command=lambda: update_selected_columns(None, tree, table, listbox, filter_col))
    btn_update_columns.pack(pady=5)

    #create a table with a frame
    tree_frame = tk.Frame(view_records_window)
    tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    tree = ttk.Treeview(tree_frame, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    #binds dropdown to update UI when a table is selected in box
    table_dropdown.bind("<<ComboboxSelected>>", lambda event: switch_table(event, tree, table, listbox, filter_col))

    #button to return back to records actions screen
    btn_rtn_recordsact_window = ttk.Button(view_records_window, text="Back to Records Actions", command=lambda: [view_records_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.place(relx=0.02, rely=0.05, anchor="nw")

