import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import tkcalendar


class Attendance:
    def __init__(self):
        self.checkboxes = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}
        self.data = None
        # ---------------Initial Window-------#
        self.root = tk.Tk()
        # -----------variables for all the interface-------------#
        self.username_for_login_var = tk.StringVar()  # for login only
        self.password_for_login_var = tk.StringVar()  # for login only
        self.password_for_signup_var = tk.StringVar()  # for signup only
        # ----title-----#
        self.root.title("Attendance Management System")
        # ----geometry----#
        self.root.geometry('300x300')
        # -----resizeable----#
        self.root.resizable(False, False)
        # ----title of this program----#
        title_of_this_program = tk.Label(self.root, text="Attendance Management System", font=('sans serif', 10))
        title_of_this_program.place(x=60, y=10)
        # --------labels and titles for login------#
        username_login_label = tk.Label(self.root, text="Username")
        username_login_label.place(x=120, y=40)
        username_login_entry = ttk.Entry(self.root, textvariable=self.username_for_login_var)
        username_login_entry.place(x=90, y=60)
        username_login_entry.focus()
        # ------labels and entry for passwords-----#
        password_login_label = tk.Label(self.root, text="Password")
        password_login_label.place(x=120, y=90)
        password_login_entry = ttk.Entry(self.root, textvariable=self.password_for_login_var)
        password_login_entry.place(x=90, y=110)

        # ----------callback functions------#
        def login():
            self.logged_in(self.username_for_login_var.get(), self.password_for_login_var.get())

        # ------login_button----------#
        login_button = ttk.Button(self.root, text="Login", command=login)
        login_button.place(x=115, y=140)
        # ----------database connection-----------#
        try:
            self.connection = mysql.connector.connect(host="localhost", password="", username="root",
                                                      database="attendance")

        except:
            messagebox.showerror("Database not found", "Couldn't connect to database")
            self.root.destroy()
        self.root.mainloop()

    def logged_in(self, username, password):
        cursor = self.connection.cursor()
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror("Required", "Both Fields are Required")
        else:
            query = f"SELECT * FROM admins where username='{username}' and password='{password}'"
            try:
                cursor.execute(query)
                data = cursor.fetchone()
                if data[0] == username and data[1] == password:
                    messagebox.showinfo("Success", "Login Success")
                    self.login_success(data[0])
                else:
                    messagebox.showerror("Login Failed", "Please Check your Details Again")
            except:
                messagebox.showerror("Login Failed", "Your Account Doesn't exists")

    def signup(self):
        signup_interface = tk.Tk()
        self.username_for_signup_var = tk.StringVar()
        signup_interface.title("Create Account")
        signup_interface.geometry('300x300')
        signup_interface.resizable(False, False)
        username_for_signup_label = tk.Label(signup_interface, text="Define Username")
        username_for_signup_label.place(x=105, y=40)
        username_entry_for_signup = ttk.Entry(signup_interface, textvariable=self.username_for_signup_var)
        username_entry_for_signup.place(x=90, y=60)
        # ------------- Label for password and entry-----#
        password_for_signup_label = tk.Label(signup_interface, text="Define Password")
        password_for_signup_label.place(x=105, y=90)
        password_entry_for_signup = ttk.Entry(signup_interface, textvariable=self.password_for_signup_var)
        password_entry_for_signup.place(x=90, y=110)

        # ----callback function----#
        def create_account():
            self.create_account_with_us(username_entry_for_signup.get(), password_entry_for_signup.get())

        # -----create account button------#
        create_account_button = ttk.Button(signup_interface, text="Create Account", command=create_account)
        create_account_button.place(x=105, y=140)

        # create a method to run the signup interface
        def run_signup_interface():
            signup_interface.mainloop()

        # call the new method to run the signup interface
        run_signup_interface()

    def create_account_with_us(self, username, password):
        query = f"INSERT INTO admins values('{username}','{password}')"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            messagebox.showinfo("Account Created", "Account Created Success,Proceed towards login")
            self.connection.commit()
        except:
            messagebox.showerror("Username already in use", "This username is already in use choose another username")

    def login_success(self, username):
        self.root.destroy()
        login_success_interface = tk.Tk()
        # -------title--------#
        login_success_interface.title(f"Welcome {username}")
        # ----geometry-------#
        login_success_interface.geometry('450x450')
        login_success_interface.resizable(False, False)
        # ------select divisions-----#
        select_division = tk.Label(login_success_interface, text="Select Class")
        select_division.place(x=200, y=50)
        # ------divisions combobox-------#
        divisions_combobox = ttk.Combobox(login_success_interface, state="readonly", width=30)
        divisions_combobox['values'] = ("CE", "IT")
        divisions_combobox.current(0)
        divisions_combobox.place(x=140, y=80)

        # --------callback functions----#
        def get_details():
            cursor = self.connection.cursor()
            division_name = divisions_combobox.get()
            division_name = division_name.lower()
            query = f"SELECT enrollment, name FROM {division_name};"
            cursor.execute(query)
            self.data = cursor.fetchall()
            start = 180
            self.checkboxes = []  # create a list to store the checkboxes
            for enrollment, name in self.data:
                records_label = ttk.Label(login_success_interface, text=f"{enrollment} {name}")
                records_label.place(x=110, y=start)
                checkbox = ttk.Checkbutton(login_success_interface)
                checkbox.place(x=350, y=start)
                self.checkboxes.append(checkbox)  # add the checkbox to the list
                start += 20

        def update():
            try:
                final_check = []
                selected_date = date_entry.get_date()
                for checkbox in self.checkboxes:
                    value = checkbox.instate(['selected'])
                    final_check.append(value)
                details_with_status = list(zip(self.data, final_check))
                for details in details_with_status:
                    if False in details:
                        division = divisions_combobox.get()
                        try:
                            enrollment = details[0][0]
                            query = f"UPDATE {division} SET status='Absent',date_day='{selected_date}' where " \
                                    f"enrollment='{enrollment}'"
                            cursor = self.connection.cursor()
                            cursor.execute(query)
                            self.connection.commit()
                        except:
                            messagebox.showerror("Failed", "Failed to Update Attendance")
                    else:
                        division = divisions_combobox.get()
                        try:
                            enrollment = details[0][0]
                            query = f"UPDATE {division} SET status='Present',date_day='{selected_date}' where " \
                                    f"enrollment='{enrollment}'"
                            cursor = self.connection.cursor()
                            cursor.execute(query)
                            self.connection.commit()
                        except:
                            messagebox.showerror("Failed", "Failed to Update Attendance")
                else:
                    messagebox.showinfo("Success", "Attendance Updated Successfully")
            except:
                messagebox.showerror("Select Student", "Please Select Student and division to update attendance")

        # ------date entry------#
        date_entry = tkcalendar.DateEntry(login_success_interface, width=12, background='darkblue', foreground='white',
                                          borderwidth=2)
        date_entry.place(x=190, y=110)
        # -----student details-----#
        student_details_button = ttk.Button(login_success_interface, text="Get Students Details", command=get_details)
        student_details_button.place(x=10, y=110)
        update_attendance = ttk.Button(login_success_interface, text="Update Attendance", command=update)
        update_attendance.place(x=180, y=400)
        # -----------main loop-------#
        login_success_interface.mainloop()


if __name__ == "__main__":
    Attendance()
