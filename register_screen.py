import tkinter as tk
from tkinter import messagebox
import auth_utils

class RegisterScreen(tk.Frame):
    def __init__(self, master):
        # Initialize registration screen frame
        super().__init__(master)
        # Create registration title
        tk.Label(self, text="Register", font=("Arial", 18)).pack(pady=20)

        # Username input field
        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # Password input field with masked input
        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Register and back buttons
        tk.Button(self, text="Register", command=self.register_user).pack(pady=20)
        tk.Button(self, text="Back", command=lambda: master.show_frame("MainMenu")).pack()

    def register_user(self):
        # Retrieve username and password from entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Attempt to register user and show result
        result = auth_utils.register_user(username, password)
        messagebox.showinfo("Register", result)
