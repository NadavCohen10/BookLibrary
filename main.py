import tkinter as tk
from main_menu import MainMenu
from login_screen import LoginScreen
from register_screen import RegisterScreen
from dashboard_screen import DashboardScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library")
        self.geometry("240x500")


        self.frames = {}

        # loading screens
        self.frames["MainMenu"] = MainMenu(self)
        self.frames["LoginScreen"] = LoginScreen(self)
        self.frames["RegisterScreen"] = RegisterScreen(self)
        self.frames["DashboardScreen"] = DashboardScreen(self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, frame_name):
        """shoes the chosen frame"""
        frame = self.frames[frame_name]
        frame.tkraise()




if __name__ == "__main__":
    app = App()
    app.mainloop()
