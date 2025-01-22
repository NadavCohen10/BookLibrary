import tkinter as tk



def setup(title="Library"):
    root = tk.Tk()
    root.title(title)
    root.geometry("1000x600")
    root.configure(bg=f"#476e75")
    return root
