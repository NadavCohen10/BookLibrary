import tkinter as tk
from tkinter import messagebox
import auth_utils

class RegisterScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Register", font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Register", command=self.register_user).pack(pady=20)
        tk.Button(self, text="Back", command=lambda: master.show_frame("MainMenu")).pack()

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        result = auth_utils.register_user(username, password)
        messagebox.showinfo("Register", result)
