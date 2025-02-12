# records_actions.py
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from utils import center_window

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
    btn_rtn_homepage_window = ttk.Button(records_act_window, text="Back to Homepage", command=lambda: [records_act_window.destroy(), homepage_window.deiconify()])
    btn_rtn_homepage_window.place(relx=0.05, rely=0.05, anchor="nw")  # Top-Left



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

def open_view_records(root):
    #withdraws records_act_window
    records_act_window.withdraw()
    #sets the window variable to global to avoid having to send it around
    global view_records_window

    #sets window to root,centers it and sets window title
    view_records_window = tk.Toplevel(root)
    center_window(view_records_window, 800, 630)
    view_records_window.title("View Records")
    
    #temporary label of information
    label = tk.Label(view_records_window, text="View Records", font=("Helvetica", 40, "bold"),bd=2, relief="solid", padx=10, pady=5)
    label.pack(pady=50)

    #button to return back to records actions screen
    btn_rtn_recordsact_window = ttk.Button(view_records_window, text="Back to Records Actions", command=lambda: [view_records_window.destroy(), records_act_window.deiconify()])
    btn_rtn_recordsact_window.pack()

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
      