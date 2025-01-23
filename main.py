import tkinter as tk
from main_menu import MainMenu
from login_screen import LoginScreen
from register_screen import RegisterScreen
from dashboard_screen import DashboardScreen


class App(tk.Tk):
    # Initialize main application window
    def __init__(self):
        super().__init__()
        self.title("Library")
        self.geometry("240x500")

        # Dictionary to store different application screens
        self.frames = {}

        # Create and store application screens
        self.frames["MainMenu"] = MainMenu(self)
        self.frames["LoginScreen"] = LoginScreen(self)
        self.frames["RegisterScreen"] = RegisterScreen(self)
        self.frames["DashboardScreen"] = DashboardScreen(self)

        # Position all frames in the grid
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        # Start with main menu screen
        self.show_frame("MainMenu")

    def show_frame(self, frame_name):
        """Raise the selected frame to the top of the window"""
        frame = self.frames[frame_name]
        frame.tkraise()




if __name__ == "__main__":
    # Create and run the application
    app = App()
    app.mainloop()
