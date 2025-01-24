import tkinter as tk
from tkinter import messagebox


from library import Library  # ייבוא ספריית Library
from Book import Book as bk
from log_write import logger
from strategy_search import TitleSearchStrategy, AuthorSearchStrategy, YearSearchStrategy, SearchContext, \
    CategorySearchStrategy


class DashboardScreen(tk.Frame):
    # Initialize dashboard with library and UI elements
    def __init__(self, master):
        super().__init__(master)
        self.library = Library()    # Create library object
        self.library.set_book()     # Create library object

        # Create dashboard title
        tk.Label(self, text="Welcome to Library System", font=("Arial", 18)).pack(pady=20)

        # Create buttons for various library operations
        tk.Button(self, text="Add Book", command=self.add_book).pack(pady=10)
        tk.Button(self, text="Remove Book", command=self.remove_book).pack(pady=10)
        tk.Button(self, text="Search Book", command=self.search_book).pack(pady=10)
        tk.Button(self, text="View Books", command=self.view_books).pack(pady=10)
        tk.Button(self, text="Lend Book", command=self.lend_book).pack(pady=10)
        tk.Button(self, text="Return Book", command=self.return_book).pack(pady=10)
        tk.Button(self, text="Popular Books", command=self.popular_books).pack(pady=10)
        tk.Button(self, text="Logout", command=self.logout).pack(pady=10)


    def add_book(self):
        # Open window to add a new book to library
        window = tk.Toplevel(self)
        window.title("Add Book")

        # Create input fields for book details
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
            # Validation to ensure all fields are filled and valid
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

                # Create book object and add to library
                book = bk(title, author, "No", copies, genre, year)

                messagebox.showinfo("Add Book", self.library.add_book(book))
                window.destroy()

                # Check waiting list and process borrowing if book is available
                b = self.library.get_book(title)
                if title in self.library.get_waiting_list():
                    while len(self.library.get_waiting_list()[title]) > 0 and b.is_available():
                        messagebox.showinfo("borrowed from waiting list", self.library.pop_waiting_list(b))
                        messagebox.showinfo("borrowed from waiting list",self.library.borrow_book(title))



        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)

    # הסרת ספר
    def remove_book(self):
        # Open dialog to remove a book from the library by title
        window = tk.Toplevel(self)
        window.title("Remove Book")

        tk.Label(window, text="Enter Book Title to Remove:").pack(pady=5)
        title_entry = tk.Entry(window)
        title_entry.pack(pady=5)

        def submit():
            # Remove book and show result
            title = title_entry.get()
            if title != "":
                messagebox.showinfo("Remove Book", self.library.remove_book(title))
            else:
                 messagebox.showerror("Remove Book", "Book not found!")
            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)

    def search_book(self):
        # Open dialog to search books using different strategies
        window = tk.Toplevel(self)
        window.title("Search Book")

        # Radio buttons for search criteria selection
        tk.Label(window, text="Select search type:").pack(pady=5)
        search_type = tk.StringVar(value="title")
        tk.Radiobutton(window, text="Title", variable=search_type, value="title").pack()
        tk.Radiobutton(window, text="Author", variable=search_type, value="author").pack()
        tk.Radiobutton(window, text="Genre", variable=search_type, value="category").pack()
        tk.Radiobutton(window, text="Year", variable=search_type, value="year").pack()

        tk.Label(window, text="Enter search value:").pack(pady=5)
        search_entry = tk.Entry(window)
        search_entry.pack(pady=5)

        def submit():
            # Dynamically select search strategy based on user's choice
            value = search_entry.get()
            criteria = search_type.get()
            search_strategy = None

            # Select appropriate search strategy
            if criteria == "title":
                search_strategy = TitleSearchStrategy()

            elif criteria == "author":
                search_strategy = AuthorSearchStrategy()

            elif criteria == "category":
                search_strategy = CategorySearchStrategy()

            elif criteria == "year":
                search_strategy = YearSearchStrategy()

            # Perform search and display results
            search_context = SearchContext(search_strategy)
            found_books = search_context.search(self.library.get_books(), value)

            if found_books:
                logger(f"Search book {value} by {criteria} completed successfully")
                messagebox.showinfo("Search Results", f"Found books: {', '.join([book.get_title() for book in found_books])}")
            else:
                logger(f"Search book {value} by {criteria} fail")
                messagebox.showerror("Search Results", "No books found!")
            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)


    def view_books(self):
        # Open dialog to view books with different filtering options
        window = tk.Toplevel(self)
        window.title("View Book")

        # Radio buttons for book view type
        tk.Label(window, text="Select view type:").pack(pady=5)
        view_type = tk.StringVar(value="all books")
        tk.Radiobutton(window, text="All Books", variable=view_type, value="all books").pack()
        tk.Radiobutton(window, text="loaned Books", variable=view_type, value="loaned books").pack()
        tk.Radiobutton(window, text="Available Books", variable=view_type, value="Available books").pack()


        def submit():
            # Display books based on selected criteria
            criteria = view_type.get()
            message = ""

            if criteria == "all books":
                message = self.library.view_books(self.library.get_books())
            elif criteria == "loaned books":
                message = self.library.view_books(self.library.get_loaned_books())
            elif criteria == "Available books":
                    message = self.library.view_books(self.library.get_available_books())

            # Show results or error message
            if message != "":
                messagebox.showinfo("View Book", message)
                logger(f"Displayed {criteria} successfully")
            else:
                messagebox.showerror("View Book", "No books found!")
                logger(f"Displayed {criteria} fail")
            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)

    def lend_book(self):
        # Open dialog to lend a book
        window = tk.Toplevel(self)
        window.title("Lend Book")

        tk.Label(window, text="Enter Book Title to Lend:").pack(pady=5)
        title_entry = tk.Entry(window)
        title_entry.pack(pady=5)

        def submit():
            # Attempt to borrow book, add to waiting list if unavailable
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

        # Open dialog to add user to waiting list for unavailable book
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

            # Validate contact information before adding to waiting list
            if phone.isdigit() and "@" in email:
                messagebox.showinfo("Waiting liat",self.library.add_to_wait_list(title,name, phone, email))
                window.destroy()

            else:
                messagebox.showerror("Data Error", "Invalid Phone or Email.")
        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)



    def return_book(self):
        # Open dialog to return a book
        window = tk.Toplevel(self)
        window.title("Return Book")

        tk.Label(window, text="Enter Book Title to Return:").pack(pady=5)
        title_entry = tk.Entry(window)
        title_entry.pack(pady=5)

        def submit():
            # Process book return and check waiting list
            title = title_entry.get()
            if title !="":
                messagebox.showinfo("Return Book", self.library.return_book(title))
                b = self.library.get_book(title)
                if title in self.library.get_waiting_list():
                        messagebox.showinfo("Return Book", self.library.pop_waiting_list(b))
                        messagebox.showinfo("Return Book", self.library.borrow_book(title))

            else:
                messagebox.showerror("Return Book", "Book not found!")
            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)

    def logout(self):
        # Log out and return to main menu
        try:
            logger(f"log out successful")
            messagebox.showinfo("Logout", "You have logged out!")
            self.master.show_frame("MainMenu")  # חזרה למסך הראשי
        except:
            logger(f"log out fail")

    def popular_books(self):
        # Display most popular books in the library
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