# upe_budget.py
import tkinter as tk
from tkinter import ttk
import sqlite3
from utils import center_window
from tkcalendar import Calendar
from tkinter import *
import tkinter.messagebox as messagebox
from datetime import datetime
import os, sys
from PIL import Image, ImageTk
from utils import resource_path
icon_path = resource_path("Image/icon.ico") 

'''
----------------------------------------
DATABASE CONNECTION/GENERAL FUNCTIONS
----------------------------------------
'''
# Global connection variable
conn = None
selected_date_str = "No Date"



#function to get project root
def get_project_root():
    #when running from pyinstaller .exe 
    if getattr(sys, 'frozen', False):
        #go up from dist/main to project root
        return os.path.abspath(os.path.join(os.path.dirname(sys.executable), '..', '..'))
    #when running from development source
    else:
        return os.path.dirname(os.path.abspath(__file__))

#Function to get connection to db
def get_db_connection():
    #returns gloval database connection
    global conn
    db_path = os.path.join(get_project_root(), "UPEApp.db")
    if conn is None:
        conn = sqlite3.connect(db_path)
    return conn

def close_db_connection():
    #Close the global connection
    global conn
    if conn:
        conn.close()
        conn = None

#function to grab budget data and return it
def fetch_budget_data():
    #creates connection
    conn = get_db_connection()
    cursor = conn.cursor()
    #grabs all columns from tables
    cursor.execute("SELECT * FROM BudgetRunningTotal")
    #grabs the related rows from columns and returns it
    rows = cursor.fetchall()
    return rows

# Function to get the selected date
def get_selected_date(cal, lblSelectedDate):  
    global selected_date_str  
    selected_date_str = cal.get_date()
    lblSelectedDate.config(text=f"Selected Date: {selected_date_str}")

entry_widget = None

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
    
    # Columns you don't want to allow editing
    uneditable_columns = ["Transaction No", "Running Total"]

    # Get actual column name from the treeview
    columns = tree["columns"]
    column_name = columns[column_index]

    if column_name in uneditable_columns:
        messagebox.showinfo("Error", f"Cannot edit '{column_name}' column")
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

    #CREATE VARIABLE THAT GRABS ALL COLUMNS
    columns = ("BDGET_TRNS_NO", "BDGET_TRNS_DT", "BDGET_TRNS_TYP", "BDGET_MEMO", "BDGET_TRNS_AM", "Running_Total")

    new_value = entry_widget.get()
    column_name = columns[column_index]  # Get column name

    #get the primary key value instead of assuming "id"
    primary_key_value = tree.item(selected_item, "values")[0]  # First column is assumed primary key

    #update database with correct primary key column
    update_database("Budget", column_name, new_value, primary_key_value)

    #update Treeview
    values = list(tree.item(selected_item, "values"))
    values[column_index] = new_value
    tree.item(selected_item, values=values)

    entry_widget.destroy()

#function to update treeview with selected table data
def update_treeview(tree, table, selected_columns, filter_col=None):
    global visible_columns, current_table
    current_table = "Budget"  #stores table name for later updates

    #clear all existing treeview data
    for item in tree.get_children():
        tree.delete(item)

    #fetch data from the selected table
    if table == "Budget":
        columns = ("BDGET_TRNS_NO", "BDGET_TRNS_DT", "BDGET_TRNS_TYP", "BDGET_MEMO", "BDGET_TRNS_AM", "Running_Total")
        data = fetch_member_data()
        return  
    
    #apply filter if user wants
    if filter_col:
        data = [row for row in data if filter_col.lower() in str(row).lower()]

    #filter columns based on selected filter
    visible_columns = [col for col in columns]

    #update Treeview columns
    tree["columns"] = visible_columns
    for col in visible_columns:
        tree.heading(col, text=f"{col} {'▲'}", command=lambda _col=col: treeview_sort_column(tree, _col, False))
        tree.column(col, anchor="center", width=120)

    #insert filtered data
    for row in data:
        filtered_row = [row[columns.index(col)] for col in visible_columns]
        tree.insert("", tk.END, values=filtered_row)

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

#function to grab data from Member table and return it
def fetch_member_data():
    #creates connection
    conn = get_db_connection()
    cursor = conn.cursor()
    #grabs all columns
    cursor.execute("BDGET_TRNS_NO", "BDGET_TRNS_DT", "BDGET_TRNS_TYP", "BDGET_MEMO", "BDGET_TRNS_AM", "Running_Total")
    #grabs all rows from related columns and returns it
    rows = cursor.fetchall()
    return rows

#function to update SQLite database after cell is edited
def update_database(table, column_name, new_value, primary_key_value):
    #connects to db
    conn = get_db_connection() 
    cursor = conn.cursor()

    #define primary key column per table
    primary_key_column = "BDGET_TRNS_NO"

    #sends sql query to db to update table with new info
    query = f"UPDATE {table} SET {column_name} = ? WHERE {primary_key_column} = ?"
    cursor.execute(query, (new_value, primary_key_value))
    
    conn.commit()

def add_transactionDB(date, type, amount, memo):
    #connects to db
    conn = get_db_connection()
    cursor = conn.cursor()

    #sends sql query to db to update table with new info
    query = "INSERT INTO budget (BDGET_TRNS_DT, BDGET_TRNS_TYP, BDGET_TRNS_AM, BDGET_MEMO) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (date, type, amount, memo))
    
    conn.commit()

    messagebox.showinfo("Success", "Transaction added successfully")
    
    
    

'''
---------------------------------
MAIN BUDGET WINDOW FUNCTIONS
-----------------------------------
'''
#function to open budget homepage
def open_upe_budget(homepage_window, root):
    #withdrawal homepage
    homepage_window.withdraw()

    #creates window, sets title and centers it
    global upe_budget_window
    upe_budget_window = tk.Toplevel(root)
    upe_budget_window.iconbitmap(icon_path)
    upe_budget_window.title("View Budget")
    center_window(upe_budget_window, 800, 630)

    #creates header
    label = tk.Label(upe_budget_window, text="Budget Home", bg="white", fg="black", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=50)
    

    #Make the background color red
    upe_budget_window.configure(bg="#52101a")

    #back to homepage button
    btn_rtn_homepage_window = tk.Button(upe_budget_window, text="Back", bg="black", fg="white", highlightcolor="gray", font=("Franklin Gothic URW", 15, "bold"),width=7, height=1, padx=1, pady=1, command=lambda: [close_db_connection(), upe_budget_window.destroy(), homepage_window.deiconify()])
    btn_rtn_homepage_window.pack(pady=15)
    btn_rtn_homepage_window.place(relx=0.05, rely=0.05, anchor="nw")
    #create highlight on hover
    btn_rtn_homepage_window.bind("<Enter>", lambda event : btn_rtn_homepage_window.config(bg="grey"))
    btn_rtn_homepage_window.bind("<Leave>", lambda event : btn_rtn_homepage_window.config(bg="black")) 


    #View history button
    btn_view_history = tk.Button(upe_budget_window, text="View Full History", bg="black", fg="white", highlightcolor="gray", font=("Franklin Gothic URW", 20, "bold"),width=15, height=2, padx=1, pady=1, command=lambda: [upe_budget_window.withdraw(), open_budget_history(upe_budget_window, root)])
    btn_view_history.pack(pady=15)
    btn_view_history.place(relx=0.285, rely=0.82, anchor="center")
    #change color on hover
    btn_view_history.bind("<Enter>", lambda event : btn_view_history.config(bg="grey"))
    btn_view_history.bind("<Leave>", lambda event : btn_view_history.config(bg="black")) 

    #add transaction button
    btn_transaction = tk.Button(upe_budget_window, text="Add Transaction", bg="black", fg="white", highlightcolor="gray", font=("Franklin Gothic URW", 20, "bold"),width=15, height=2, padx=1, pady=1, command=lambda: [upe_budget_window.withdraw(), open_add_transaction(upe_budget_window, root)])
    btn_transaction.pack(pady=15)
    btn_transaction.place(relx=0.715, rely=0.82, anchor="center")
    #change color on hover
    btn_transaction.bind("<Enter>", lambda event : btn_transaction.config(bg="grey"))
    btn_transaction.bind("<Leave>", lambda event : btn_transaction.config(bg="black")) 

    #add treeview with data from database
    #Table Frame
    frame = tk.Frame(upe_budget_window)
    
    frame.place(relx=0.5, rely=0.475, anchor="center")
    frame.configure(bg="white")

    #Define table columns
    columns = ("Transaction No", "Date", "Type", "Memo", "Amount", "Running Total")

    #Create Treeview widget
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Define column properties
    tree.column("Transaction No", width=120, anchor="center")
    tree.column("Date", width=100, anchor="center")
    tree.column("Type", width=150, anchor="center")
    tree.column("Memo", width=200, anchor="center")
    tree.column("Amount", width=100, anchor="center")
    tree.column("Running Total", width=100, anchor="center")

    # Define column headers
    for col in columns:
        tree.heading(col, text=col)

    #Insert data into table
    budget_data = fetch_budget_data()
    for row in budget_data:
        row = list(row)
        #format Amount and Running Total as currency
        try:
            row[4] = f"${float(row[4]):,.2f}"  #amount column
            row[5] = f"${float(row[5]):,.2f}"  #running Total column
        except (ValueError, IndexError):
            #in case there's bad/missing data
            pass

        tree.insert("", tk.END, values=row)

    #Add scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    

    #Pack widgets
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)



'''
--------------------------------
BUDGET HISTORY WINDOW FUNCTIONS
--------------------------------
'''
#function to open budget history window
def open_budget_history(budget_home_window, root):
    global tree
    #withdraws budget home
    budget_home_window.withdraw()

    #creates history page, sets title and centers it
    upe_budget_history = tk.Toplevel(root)
    upe_budget_history.iconbitmap(icon_path)
    upe_budget_history.title("Budget History")
    center_window(upe_budget_history, 850, 630)

    #creates header
    label = tk.Label(upe_budget_history, text="Budget History", bg="white", fg="black",font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=50)
    #Make the background color red
    upe_budget_history.configure(bg="#52101a")

    #back to homepage button
    btn_rtn_budget_home = tk.Button(upe_budget_history, text="Back", bg="black", fg="white", highlightcolor="gray", font=("Franklin Gothic URW", 15, "bold"),width=7, height=1, padx=1, pady=1, command=lambda: [close_db_connection(), upe_budget_history.destroy(), budget_home_window.deiconify()])
    btn_rtn_budget_home.pack(pady=15)
    btn_rtn_budget_home.place(relx=0.05, rely=0.05, anchor="nw")
    #create highlight on hover
    btn_rtn_budget_home.bind("<Enter>", lambda event : btn_rtn_budget_home.config(bg="grey"))
    btn_rtn_budget_home.bind("<Leave>", lambda event : btn_rtn_budget_home.config(bg="black")) 

    #Table Frame
    frame = tk.Frame(upe_budget_history)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    #Define table columns
    columns = ("Transaction No", "Date", "Type", "Memo", "Amount", "Running Total")

    #Create Treeview widget
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Define column properties
    tree.column("Transaction No", width=120, anchor="center")
    tree.column("Date", width=100, anchor="center")
    tree.column("Type", width=150, anchor="center")
    tree.column("Memo", width=200, anchor="center")
    tree.column("Amount", width=100, anchor="center")
    tree.column("Running Total", width=100, anchor="center")

    # Define column headers
    for col in columns:
        tree.heading(col, text=col)

    #Insert data into table
    budget_data = fetch_budget_data()
    for row in budget_data:
        row = list(row)
        #format Amount and Running Total as currency
        try:
            row[4] = f"${float(row[4]):,.2f}"  #amount column
            row[5] = f"${float(row[5]):,.2f}"  #running Total column
        except (ValueError, IndexError):
            #in case there's bad/missing data
            pass

        tree.insert("", tk.END, values=row)

    #Add scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    #Pack widgets
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #bind double-click event for editing cells
    tree.bind("<Double-1>", on_double_click)

'''
-------------------------------
ADD TRANSACTION WINDOW FUNCTIONS
-------------------------------
'''
#function to open edit budget window
def open_add_transaction(budget_home_window, root):

    #BRING IN RUNNING TOTAL
    #RADIO BUTTON RUNNING TOTAL

    #call in global variables
    global date_label
    global selected_date_str
    global budget_add_transaction

    #creates edit budget window, sets title and centers it
    budget_add_transaction = tk.Toplevel(root)
    budget_add_transaction.iconbitmap(icon_path)
    budget_add_transaction.title("Add Transaction")
    center_window(budget_add_transaction, 850, 630)

    #creates labels; Header and textbox labels
    lblHeader = tk.Label(budget_add_transaction, text="Add Transaction", bg="white", fg="black", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    lblHeader.pack(pady=20)

    #Make the background color red
    budget_add_transaction.configure(bg="#52101a")

    lblDate = tk.Label(budget_add_transaction, text="* Transaction Date", font=("Helvetica", 12, "bold"), bd=2, padx=5, pady=5)
    lblDate.pack(pady=5)
    lblDate.place(relx=0.1, rely=0.22)
    lblDate.configure(bg="#52101a", fg="white")

    lblType = tk.Label(budget_add_transaction, text="* Type", font=("Helvetica", 12, "bold"), bd=2, padx=5, pady=5)
    lblType.pack(pady=5)
    lblType.place(relx=0.45, rely=0.22)
    lblType.configure(bg="#52101a", fg="white")

    lblAmount = tk.Label(budget_add_transaction, text="* Amount", font=("Helvetica", 12, "bold"), bd=2,  padx=5, pady=5)
    lblAmount.pack(pady=5)
    lblAmount.place(relx=0.7, rely=0.22)
    lblAmount.configure(bg="#52101a", fg="white")

    lblMemo = tk.Label(budget_add_transaction, text="* Memo", font=("Helvetica", 12, "bold"), bd=2, padx=5, pady=5)
    lblMemo.pack(pady=5)
    lblMemo.place(relx=0.45, rely=0.42)
    lblMemo.configure(bg="#52101a", fg="white")
    

    #Radio Buttons for type
    transaction_type = tk.StringVar(value="Withdrawal")
    rdWithdrawal = tk.Radiobutton(budget_add_transaction, text="Withdrawal", variable=transaction_type, value="Withdrawal", disabledforeground="white", background="#52101a", activebackground="#52101a", activeforeground="white", foreground="white", selectcolor="#52101a", indicatoron=True)
    rdWithdrawal.place(relx=0.45, rely=0.27)
    rdDeposit = tk.Radiobutton(budget_add_transaction, text="Deposit", variable=transaction_type, value="Deposit", disabledforeground="white", background="#52101a", activebackground="#52101a", activeforeground="white", foreground="white", selectcolor="#52101a", indicatoron=True)
    rdDeposit.place(relx=0.45, rely=0.32)

    #Text boxes for amount and memo
    txtAmount = tk.Text(budget_add_transaction, height=1, width=15)
    txtAmount.place(relx=0.7, rely=0.27)

    #when in txtamount, enter key submits the transaction
    txtAmount.bind("<Return>", "break")
    txtAmount.bind("<Tab>", "break")
   

    txtMemo = tk.Text(budget_add_transaction, height=5, width=30)
    txtMemo.place(relx=0.45, rely=0.47)

    #Back to Budget Home button and submit button
    btn_rtn_budget_home = tk.Button(budget_add_transaction, text="Back", bg="black", fg="white", highlightcolor="gray", font=("Franklin Gothic URW", 15, "bold"), width=8, command=lambda: [budget_add_transaction.destroy(), budget_home_window.deiconify()])
    btn_rtn_budget_home.place(relx=0.02, rely=0.07, anchor="nw")
    btn_rtn_budget_home.bind("<Enter>", lambda event : btn_rtn_budget_home.config(bg="grey"))
    btn_rtn_budget_home.bind("<Leave>", lambda event : btn_rtn_budget_home.config(bg="black")) 

    # Create the calendar and get current date
    current_date = datetime.today().strftime('%m/%d/%Y')
    cal = Calendar(budget_add_transaction, selectmode="day", year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)
    cal.pack(pady=20)
    cal.place(relx=0.05, rely=0.27)

    lblSelectedDate = tk.Label(budget_add_transaction, text="No Date Selected", font=("Arial", 12, "bold"))
    lblSelectedDate.pack(pady=10)
    lblSelectedDate.place(relx=0.087, rely=0.57)
    lblSelectedDate.configure(bg="#52101a", fg="white")

    # Button to select the date
    select_button = tk.Button(budget_add_transaction, text="Update Date", bg="black", fg="white", highlightcolor="gray", font=("Franklin Gothic URW", 12, "bold"), width=12, command= lambda: [get_selected_date(cal, lblSelectedDate)])
    select_button.pack(pady=10)
    select_button.place(relx=0.115, rely=0.62)
    select_button.bind("<Enter>", lambda event : select_button.config(bg="grey"))
    select_button.bind("<Leave>", lambda event : select_button.config(bg="black")) 
    lblSelectedDate.config(text=f"Selected Date: {selected_date_str}")

    btnSubmit = tk.Button(budget_add_transaction, bg="black", fg="white", highlightcolor="gray", font=("Franklin Gothic URW", 15, "bold"), text="Submit", width=8,command=lambda: submit_transaction(txtMemo, txtAmount, transaction_type, selected_date_str))
    btnSubmit.place(relx=0.8, rely=0.95, anchor="sw")
    btnSubmit.bind("<Return>", lambda event: submit_transaction(txtMemo, txtAmount, transaction_type, selected_date_str))
    btnSubmit.bind("<Enter>", lambda event : btnSubmit.config(bg="grey"))
    btnSubmit.bind("<Leave>", lambda event : btnSubmit.config(bg="black")) 

    #bind enter key to submit transaction
    budget_add_transaction.bind("<Return>", lambda event: submit_transaction(txtMemo, txtAmount, transaction_type, selected_date_str))

    


'''
-------------------------------
EDIT TRANSACTION WINDOW FUNCTIONS
-------------------------------
'''

# DATA VALIDATION FOR EDITING


#edit transaction window
def edit_transaction(budget_home_window, root):
    #creates edit budget window, sets title
    budget_edit_transaction = tk.Toplevel(root)
    budget_edit_transaction.iconbitmap(icon_path)
    budget_edit_transaction.title("Edit Transaction")
    center_window(budget_edit_transaction, 800, 630)

    #create back button
    btn_rtn_budget_home = ttk.Button(budget_edit_transaction, text="Back to Budget",command=lambda: [budget_edit_transaction.destroy(), budget_home_window.deiconify()])
    btn_rtn_budget_home.place(relx=0.02, rely=0.05, anchor="nw")

    #creates labels; Header and textbox labels
    lblHeader = tk.Label(budget_edit_transaction, text="Edit Transaction", font=("Helvetica", 40, "bold"), bd=2, relief="solid", padx=10, pady=5)
    lblHeader.pack(pady=20)

    lblDate = tk.Label(budget_edit_transaction, text="Transaction Date", font=("Helvetica", 12), bd=2, padx=5, pady=5)
    lblDate.pack(pady=5)
    lblDate.place(relx=0.1, rely=0.2)

    lblType = tk.Label(budget_edit_transaction, text="Type", font=("Helvetica", 12), bd=2, padx=5, pady=5)
    lblType.pack(pady=5)
    lblType.place(relx=0.45, rely=0.2)

    lblAmount = tk.Label(budget_edit_transaction, text="Amount", font=("Helvetica", 12), bd=2,  padx=5, pady=5)
    lblAmount.pack(pady=5)
    lblAmount.place(relx=0.7, rely=0.2)

    lblMemo = tk.Label(budget_edit_transaction, text="Memo", font=("Helvetica", 12), bd=2, padx=5, pady=5)
    lblMemo.pack(pady=5)
    lblMemo.place(relx=0.45, rely=0.4)

    lblNum = tk.Label(budget_edit_transaction, text="Transaction Number", font=("Helvetica", 12), bd=2, padx=5, pady=5)
    lblNum.pack(pady=5)
    lblNum.place(relx=0.1, rely=0.4)



def submit_transaction(txtMemo, txtAmount, transaction_type, lblSelectedDate):
    #max transaction amount
    MAX_AMOUNT = 1000000

    #verify that a date is selected
    if lblSelectedDate == "No Date":
        messagebox.showerror("Error", "Please select a date for the transaction")
        return
    pass

    #check if radio button is selected
    if transaction_type.get() == "":
        messagebox.showerror("Error", "Please select a transaction type")
        return
    
    #make sure txtamount is not blank
    if len(txtAmount.get("0.0", "end-1c")) == 0:
        messagebox.showerror("Error", "Please enter a transaction amount")
        return
    
    #verify that txtamount is a number. If the number has a decimal verify it is two decimals. If the number does not, add two decimals
    if not txtAmount.get("0.0", "end-1c").replace('.', '', 1).isdigit():
        messagebox.showerror("Error", "Amount must be a number")
        return
    elif '.' in txtAmount.get("0.0", "end-1c"):
        if len(txtAmount.get("0.0", "end-1c").split('.')[1]) != 2:
            messagebox.showerror("Error", "Amount must have two decimal places")
            return
    else:
        txtAmount.insert("end", ".00")
    
    #Limit memo characters to 100
    if len(txtMemo.get("0.0", "end-1c")) > 100 or len(txtMemo.get("0.0", "end-1c")) == 0:
        messagebox.showerror("Error", "Memo is empty or exceeds 100 characters")
        return

    #if type is withdrawal, make the amount negative
    if transaction_type.get() == "Withdrawal":
        fltAmount = float(txtAmount.get("0.0", "end-1c"))
        fltAmount = -fltAmount
    else:
        fltAmount = float(txtAmount.get("0.0", "end-1c"))

    add_transactionDB(lblSelectedDate, transaction_type.get(), fltAmount, txtMemo.get("0.0", "end-1c"))
