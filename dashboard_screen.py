import email
import tkinter as tk
from tkinter import messagebox
from unicodedata import digit

from library import Library  # ייבוא ספריית Library
from Book import Book as bk
from log_write import logger
from strategy_search import TitleSearchStrategy, AuthorSearchStrategy, YearSearchStrategy, SearchContext, \
    CategorySearchStrategy


class DashboardScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.library = Library()  # יצירת אובייקט ספרייה
        self.library.set_book()

        # תווית כותרת
        tk.Label(self, text="Welcome to Library System", font=("Arial", 18)).pack(pady=20)

        # כפתורים עבור כל פעולה
        tk.Button(self, text="Add Book", command=self.add_book).pack(pady=10)
        tk.Button(self, text="Remove Book", command=self.remove_book).pack(pady=10)
        tk.Button(self, text="Search Book", command=self.search_book).pack(pady=10)
        tk.Button(self, text="View Books", command=self.view_books).pack(pady=10)
        tk.Button(self, text="Lend Book", command=self.lend_book).pack(pady=10)
        tk.Button(self, text="Return Book", command=self.return_book).pack(pady=10)
        tk.Button(self, text="Popular Books", command=self.popular_books).pack(pady=10)
        tk.Button(self, text="Logout", command=self.logout).pack(pady=10)

    # הוספת ספר חדש
    def add_book(self):
        # יצירת חלון חדש לקבלת פרטי הספר
        window = tk.Toplevel(self)
        window.title("Add Book")

        tk.Label(window, text="Enter Book Title:").pack(pady=5)
        title_entry = tk.Entry(window)
        title_entry.pack(pady=5)

        tk.Label(window, text="Enter Author:").pack(pady=5)
        author_entry = tk.Entry(window)
        author_entry.pack(pady=5)

        tk.Label(window, text="Enter Number of Copies:").pack(pady=5)
        copies_entry = tk.Entry(window)
        copies_entry.pack(pady=5)

        tk.Label(window, text="Enter Genre:").pack(pady=5)
        genre_entry = tk.Entry(window)
        genre_entry.pack(pady=5)

        tk.Label(window, text="Enter Year:").pack(pady=5)
        year_entry = tk.Entry(window)
        year_entry.pack(pady=5)

        def submit():
            # קבלת הנתונים שהוזנו
            if (title_entry.get() == "" or author_entry.get() == "" or copies_entry.get() == ""
                    or genre_entry.get() == "" or year_entry.get() == ""
            or copies_entry.get().isdigit() == False or year_entry.get().isdigit()== False
                    or int(copies_entry.get()) <= 0):
                messagebox.showinfo("Add Book" ,"Invalid data, try again")
            else:
                title = title_entry.get()
                author = author_entry.get()
                copies = int(copies_entry.get())
                genre = genre_entry.get()
                year = int(year_entry.get())


                book = bk(title, author, "No", copies, genre, year)

                messagebox.showinfo("Add Book", self.library.add_book(book))
                window.destroy()
                b = self.library.get_book(title)
                if title in self.library.waiting_list:
                    while len(self.library.waiting_list[title]) > 0 and b.is_available():
                        messagebox.showinfo("borrowed from waiting list", self.library.pop_waiting_list(b))
                        messagebox.showinfo("borrowed from waiting list",self.library.borrow_book(title))



        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)

    # הסרת ספר
    def remove_book(self):
        # יצירת חלון חדש לקבלת פרטי הספר להסרה
        window = tk.Toplevel(self)
        window.title("Remove Book")

        tk.Label(window, text="Enter Book Title to Remove:").pack(pady=5)
        title_entry = tk.Entry(window)
        title_entry.pack(pady=5)

        def submit():
            title = title_entry.get()

            if title != "":
                messagebox.showinfo("Remove Book", self.library.remove_book(title))
            else:
                 messagebox.showerror("Remove Book", "Book not found!")
            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)

    def search_book(self):
        window = tk.Toplevel(self)
        window.title("Search Book")

        tk.Label(window, text="Select search type:").pack(pady=5)
        search_type = tk.StringVar(value="Title")
        tk.Radiobutton(window, text="Title", variable=search_type, value="Title").pack()
        tk.Radiobutton(window, text="Author", variable=search_type, value="Author").pack()
        tk.Radiobutton(window, text="Genre", variable=search_type, value="Genre").pack()
        tk.Radiobutton(window, text="Year", variable=search_type, value="Year").pack()

        tk.Label(window, text="Enter search value:").pack(pady=5)
        search_entry = tk.Entry(window)
        search_entry.pack(pady=5)

        def submit():
            value = search_entry.get()
            criteria = search_type.get()
            search_strategy = None

            if criteria == "Title":
                try:
                    search_strategy = TitleSearchStrategy()
                    logger(f"Search book {value} by name completed successfully")
                except:
                    logger(f"Search book {value} by name fail")
            elif criteria == "Author":
                try:
                    search_strategy = AuthorSearchStrategy()
                    logger(f"Search book {value} by author completed successfully")
                except:
                    logger(f"Search book {value} by author fail")
            elif criteria == "Genre":
                try:
                    search_strategy = CategorySearchStrategy()
                    logger("Displayed book by category successfully")
                except:
                    logger("Displayed book by category fail")

            elif criteria == "Year":
                try:
                    search_strategy = YearSearchStrategy()
                    logger(f"Search book {value} by year completed successfully")
                except:
                    logger(f"Search book {value} by year fail")

            search_context = SearchContext(search_strategy)
            found_books = search_context.search(self.library.get_books(), value)

            if found_books:
                messagebox.showinfo("Search Results", f"Found books: {', '.join([book.get_title() for book in found_books])}")
            else:
                messagebox.showerror("Search Results", "No books found!")
            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)


    # הצגת כל הספרים
    def view_books(self):

        window = tk.Toplevel(self)
        window.title("View Book")

        tk.Label(window, text="Select view type:").pack(pady=5)
        view_type = tk.StringVar(value="all books")
        tk.Radiobutton(window, text="All Books", variable=view_type, value="all books").pack()
        tk.Radiobutton(window, text="loaned Books", variable=view_type, value="loaned books").pack()
        tk.Radiobutton(window, text="Available Books", variable=view_type, value="Available books").pack()


        def submit():

            criteria = view_type.get()
            message = ""

            if criteria == "all books":
                try:
                    message = self.library.view_books(self.library.get_books())
                    logger(f"Displayed all books successfully")
                except:
                    logger(f"Displayed all books fail")
            elif criteria == "loaned books":
                try:
                    message = self.library.view_books(self.library.get_loaned_books())
                    logger(f"Displayed loaned books successfully")
                except:
                    logger(f"Displayed loaned books fail")
            elif criteria == "Available books":
                try:
                    message = self.library.view_books(self.library.get_available_books())
                    logger(f"Displayed available books successfully")
                except:
                    logger(f"Displayed available books fail")

            if message != "":
                messagebox.showinfo("View Book", message)
                #logger(f"Displayed {criteria} successfully")
            else:
                messagebox.showerror("View Book", "No books found!")
                #logger(f"Displayed {criteria} fail")
            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)

    # השאלת ספר
    def lend_book(self):
        # יצירת חלון חדש לקבלת פרטי הספר להשאלה
        window = tk.Toplevel(self)
        window.title("Lend Book")

        tk.Label(window, text="Enter Book Title to Lend:").pack(pady=5)
        title_entry = tk.Entry(window)
        title_entry.pack(pady=5)

        def submit():
            title = title_entry.get()

            if title !="":
                result = self.library.borrow_book(title)
                if result is not False:
                    messagebox.showinfo("Lend Book",result)
                else:
                    messagebox.showerror("Lend Book", f"Book {title} is not available \n please add your information")
                    self.waiting_list(title)
            else:
                messagebox.showerror("Lend Book", "Book not found!")
            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)

    def waiting_list(self,title):
        window = tk.Toplevel(self)
        window.title("Waiting List")
        tk.Label(window, text="Enter Name:").pack(pady=5)
        name_entry = tk.Entry(window)
        name_entry.pack(pady=5)
        tk.Label(window, text="Enter Phone:").pack(pady=5)
        phone_entry = tk.Entry(window)
        phone_entry.pack(pady=5)
        tk.Label(window, text="Enter Email:").pack(pady=5)
        email_entry = tk.Entry(window)
        email_entry.pack(pady=5)
        def submit():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()

            if phone.isdigit() and "@" in email:
                messagebox.showinfo("Waiting liat",self.library.add_to_wait_list(title,name, phone, email))
                window.destroy()

            else:
                messagebox.showerror("Data Error", "Invalid Phone or Email.")
        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)



    # החזרת ספר
    def return_book(self):
        # יצירת חלון חדש לקבלת פרטי הספר להחזרה
        window = tk.Toplevel(self)
        window.title("Return Book")

        tk.Label(window, text="Enter Book Title to Return:").pack(pady=5)
        title_entry = tk.Entry(window)
        title_entry.pack(pady=5)

        def submit():
            title = title_entry.get()

            if title !="":

                messagebox.showinfo("Return Book", self.library.return_book(title))
                b = self.library.get_book(title)
                if title in self.library.waiting_list:
                        messagebox.showinfo("Return Book", self.library.pop_waiting_list(b))
                        messagebox.showinfo("Return Book", self.library.borrow_book(title))

            else:
                messagebox.showerror("Return Book", "Book not found!")
            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)

    # חזרה למסך הראשי
    def logout(self):
        try:
            logger(f"log out successful")
            messagebox.showinfo("Logout", "You have logged out!")
            self.master.show_frame("MainMenu")  # חזרה למסך הראשי
        except:
            logger(f"log out fail")

    # הצגת ספרים פופולריים
    def popular_books(self):


        books = self.library.popular_books()
        if books:
            message = "Popular Books in library:"
            for book in books:
                message += f"\n{book}"

            messagebox.showinfo("Popular Books", f"{message}")
            logger("displayed successfully")
        else:
            messagebox.showerror("Popular Books", "No Popular Books in library:")
            logger("displayed fail")