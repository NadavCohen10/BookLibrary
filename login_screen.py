import tkinter as tk
from tkinter import messagebox
import auth_utils

class LoginScreen(tk.Frame):
    def __init__(self, master):
        # Initialize login screen frame
        super().__init__(master)
        # Create login title
        tk.Label(self, text="Login", font=("Arial", 18)).pack(pady=20)

        # Username input field
        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # Password input field with masked input
        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Login and back buttons
        tk.Button(self, text="Login", command=self.login_user).pack(pady=20)
        tk.Button(self, text="Back", command=lambda: master.show_frame("MainMenu")).pack()


    def login_user(self):
        # Retrieve username and password from entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Load users from CSV file
        users_df = auth_utils.load_users('users.csv')
        # Authenticate user credentials
        if auth_utils.authenticate_user(username, password, users_df):
            # Successful login - show confirmation and navigate to dashboard
            messagebox.showinfo("Login", "Login successful!")
            self.master.show_frame("DashboardScreen")

        else:
            # Failed login - show error message
            messagebox.showerror("Login", "Invalid username or password.")
