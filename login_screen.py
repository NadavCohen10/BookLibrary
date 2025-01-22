import tkinter as tk
from tkinter import messagebox
import auth_utils

class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Login", font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login_user).pack(pady=20)
        tk.Button(self, text="Back", command=lambda: master.show_frame("MainMenu")).pack()

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users_df = auth_utils.load_users('users.csv')
        if auth_utils.authenticate_user(username, password, users_df):
            messagebox.showinfo("Login", "Login successful!")
            self.master.show_frame("DashboardScreen")  # מעבר למסך Dashboard אחרי התחברות מוצלחת
        else:
            messagebox.showerror("Login", "Invalid username or password.")
