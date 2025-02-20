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
    label.pack(pady=50)

    #button to move to view records window
    btn_view_records_window = ttk.Button(records_act_window, text="View Records", command=lambda: open_view_records(root))
    btn_view_records_window.pack(pady=10) 

    #button to move to add members windows
    btn_add_members_window = ttk.Button(records_act_window, text="Add Member", command=lambda: open_add_member(root))
    btn_add_members_window.pack(pady=10)  

    #button to move to add students window
    btn_add_student_window = ttk.Button(records_act_window, text="Add Student", command=lambda: open_add_student(root))
    btn_add_student_window.pack(pady=10) 


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

    #set column and row amount based on actual row/column amount
    total_columns = 5
    total_rows = 5

    #sets window to root,centers it and sets window title
    add_member_window = tk.Toplevel(root)
    center_window(add_member_window, 800, 630)
    add_member_window.title("Add Members")
    
    #temporary label of information
    label = tk.Label(add_member_window, text="Add Members", font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.place(relx = .35, rely = .05, anchor="nw")

    #label for memberID
    lblMemID = tk.Text(add_member_window, height=1, width=15)
    lblMemID.grid(row=1, column=0, columnspan=1, pady=10)

    #textbox for member ID
    txtMemID = tk.Text(add_member_window, height=1, width=15)
    txtMemID.grid(row=1, column=0, columnspan=1, pady=10)

    #textbox for student ID
    txtMemStudID = tk.Text(add_member_window, height=1, width=15)
    txtMemStudID.grid(row=1, column=1, columnspan=1, pady=10)
    
    #textbox for member DOB
    txtMemDOB = tk.Text(add_member_window, height=1, width=15)
    txtMemDOB.grid(row=1, column=2, columnspan=1, pady=10)

    #textbox for member entry year
    txtEntryYr = tk.Text(add_member_window, height =1, width=15)
    txtEntryYr.grid(row = 2, column=0, columnspan=1, pady=10)

    for i in range(total_columns):  
        add_member_window.columnconfigure(i, weight=1)

    for i in range(total_rows):  
        add_member_window.rowconfigure(i, weight=1)

    #button to return back to records actions screen
    btn_rtn_recordsact_window = ttk.Button(add_member_window, text="Back to Records Actions", command=lambda: [add_member_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.grid(row=0, column=0, columnspan=1, pady=20, sticky="nw", padx=10)


'''
------------------------------
ADD STUDENT WINDOW FUNCTIONS
------------------------------
'''

#function to open add student window
def open_add_student(root):
    #withdraws records_act_window
    records_act_window.withdraw()
    #sets the window variable to global to avoid having to send it around
    global add_student_window

    
    #sets window to root,centers it and sets window title
    add_student_window = tk.Toplevel(root)
    center_window(add_student_window, 800, 630)
    add_student_window.title("Add Student")
    
    #top window header
    label = tk.Label(add_student_window, text="Add Student", font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.place(relx = .35, rely = .05, anchor="nw")

    #button to return back to records actions screen
    btn_rtn_recordsact_window = ttk.Button(add_student_window, text="Back to Records Actions", command=lambda: [add_student_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.pack()



'''
------------------------------
VIEW RECORDS WINDOW FUNCTIONS
------------------------------
'''


import tkinter as tk
from tkinter import ttk
import sqlite3

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
    conn.close()

#function to handle double-click on a treeview table cells
def on_double_click(event):
    global entry_widget

    #grabs cell row and column
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
    entry_widget = tk.Entry(tree)
    entry_widget.insert(0, current_value)
    entry_widget.focus()

    #get current cell position and places entry widget in that position
    x, y, width, height = tree.bbox(selected_item, column_index)
    entry_widget.place(x=x, y=y, width=width, height=height)

    #binds enter button to save the edited changes
    entry_widget.bind("<Return>", lambda event: save_edit(selected_item, column_index))


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
        tree.heading(col, text=col)
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
        columns = ("MEM_ID", "STUD_ID", "MEM_DOB", "MEM_ENTRY_YR", "MEM_STATUS", "MEM_POS", "MEM_PST_POS", "MEM_PHO_NO", 
                   "MEM_ABROAD_ST", "MEM_COMMUTE_ST", "MEM_MEETING_MISD", "MEM_MEETING_MISD_DESC", "MEM_PREFR_NAME")
    #sets columns if table is student
    elif table == "Student":
        columns = ("STUD_ID", "STUD_FST_NM", "STUD_LST_NM", "STUD_MID_NM", "STUD_EMAIL_ADD", "STUD_CLASS_LVL", 
                   "STUD_CURRICULUM", "STUD_DEG", "STUD_CUM_GPA", "STUD_TRANS_CRED", "STUD_EARNED_CRED", 
                   "STUD_TOTcs_CRED", "STUD_BEL_30_LR_CRED_IN", "STUD_BEL_3_GPA_IN", "STUD_INV_STATUS")
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

    #bind double-click event for editing cells
    tree.bind("<Double-1>", on_double_click)

    #binds combobox selection whenever user selects from dropdown
    table_dropdown.bind("<<ComboboxSelected>>", lambda event: switch_table(event, tree, table, listbox, filter_col))

    #button to return to records screen
    btn_rtn_recordsact_window = ttk.Button(view_records_window, text="Back to Records Actions", command=lambda: [view_records_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.place(relx=0.02, rely=0.05, anchor="nw")


