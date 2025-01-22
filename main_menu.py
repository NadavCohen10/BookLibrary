import tkinter as tk

class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Welcome to Library", font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Login", command=lambda: master.show_frame("LoginScreen")).pack(pady=10)
        tk.Button(self, text="Register", command=lambda: master.show_frame("RegisterScreen")).pack(pady=10)
