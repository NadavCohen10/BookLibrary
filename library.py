from Book import Book as bk
import pandas as pd
from collections import deque
from log_write import logger



class Library():
    def __init__(self):
        # Variables to store different book collections
        self.__book_list = [] # All books in the library
        self.__waiting_list = {} # Waiting list for books
        self.__loaned_book_list = [] # Books currently loaned out
        self.__available_book_list = [] # Books available for borrowing
    
    # Load book data from CSV files
    def load_book_list(self):
        return pd.read_csv('books.csv')
    def load_loaned_book_list(self):
        return pd.read_csv('loaned_books.csv')
    def load_available_book_list(self):
        return pd.read_csv('available_books.csv')
    def load_waiting_list(self):
        return pd.read_csv('waiting_list.csv')


    def set_book(self):
        # Initialize books from CSV data
        books = self.load_book_list()
        for _, row in books.iterrows():
            # Create Book objects from CSV data
            book = bk(row["title"], row["author"], row["is_loaned"], row["copies"], row["genre"], row["year"])
            self.__book_list.append(book)

        # Categorize books into available and loaned lists
        for book in self.__book_list:
            """first initialization for the files"""
            # books = pd.DataFrame(book.get_dict())
            if book.is_available():
                """first initialization for the files"""
                #books.to_csv('available_books.csv', mode='a', index=False, header=False)
                self.__available_book_list.append(book)
            else:
                """first initialization for the files"""
               # books.to_csv('loaned_books.csv', mode='a', index=False, header=False)
                self.__loaned_book_list.append(book)

        # Handle books with changed loan status
        loaned_books = self.load_loaned_book_list()
        for _, row in loaned_books.iterrows():
            if row['is_loaned'] == "No":
                for book in self.__book_list:
                    if book.get_title() == row['title']:
                        book.reduce(row['copies'])
                        self.__loaned_book_list.append(book)

        # Populate waiting list
        waiting = self.load_waiting_list()
        for _, row in waiting.iterrows():
            if row['title'] not in self.__waiting_list:
                self.__waiting_list[row['title']] = deque()

            person = {'name': row['name'],'phone': row['phone'], 'email': row['email']}
            self.__waiting_list[row['title']].append(person)


    def add_book(self,book):
        # Process of adding a new book or increasing existing book copies
        avail_books = self.load_available_book_list()
        books = self.load_book_list()
        # Select books by title
        titles = books.iloc[:,0 ].tolist()
        if book.get_title() not in titles:
            # Add completely new book
            avail_books = pd.DataFrame(book.get_dict())
            avail_books.to_csv('available_books.csv', mode='a', index=False, header=False)
            avail_books.to_csv('books.csv', mode='a', index=False, header=False)

            self.__book_list.append(book)
            self.__available_book_list.append(book)

            logger('book added successfully')
            return f"Added {book.get_title()} to books list"

        else:
            # Handle existing book - update copies and availability
            titles = avail_books.iloc[:, 0].tolist()
            if book.get_title() not in titles:
                avail_books = pd.DataFrame(book.get_dict())
                avail_books.to_csv('available_books.csv', mode='a', index=False, header=False)


            else:
                # Increase book copies
                avail_books.loc[avail_books['title'] == book.get_title(), 'copies'] += book.get_copies()
                avail_books.to_csv('available_books.csv', index=False)

            # Update book information and loan status
            books.loc[books['title'] == book.get_title(), 'copies'] += book.get_copies()
            books.to_csv('books.csv', index=False)


            b = self.get_book(book.get_title())
            b.add_copies(str(book.get_copies()))
            if b.is_loaned() == "Yes":
                b.set_loaned("No")
                self.__available_book_list.append(b)

            books.loc[books['title'] == book.get_title(), 'is_loaned'] = "No"
            loaned_books = self.load_loaned_book_list()
            loaned_books.loc[loaned_books['title'] == book.get_title(), 'is_loaned'] = "No"

            # Save the updated DataFrame back to the CSV
            books.to_csv('books.csv', index=False)
            loaned_books.to_csv('loaned_books.csv', index=False)

            logger('book added successfully')
            return f"Added {book.get_copies()} copies to the book {book.get_title()}"



    def add_to_wait_list(self,book,name,phone,email):

        # Add a person to the waiting list for a specific book
        if book not in self.__waiting_list:
            self.__waiting_list[book] = deque()

        # Check if person is already in waiting list
        for _, person in enumerate(self.__waiting_list[book]):
            if str(person["phone"]) == str(phone):
                return "Person is already in waiting list"

        # Add person to waiting list
        self.__waiting_list[book].append({"name": name, "phone": phone, "email": email})
        self.update_waiting_list_file()
        return f"{name} has been added to waiting list of the book {book}"


    def update_waiting_list_file(self):
        # Synchronize waiting list data with CSV file
        waiting = self.load_waiting_list()

        if waiting is not None:
            # Reset waiting list file
            headers = ["title", "name", "phone", "email"]
            waiting = pd.DataFrame(columns=headers)
            waiting.to_csv('waiting_list.csv', index=False)

        # Rewrite waiting list data to CSV
        for title in self.__waiting_list:
            for person in self.__waiting_list[title]:
                data = {
                    'title': [title],
                    'name': [person["name"]],
                    'phone': [person["phone"]],
                    'email': [person["email"]]
                }
                data = pd.DataFrame(data)
                data.to_csv('waiting_list.csv', mode='a', index=False, header=False)


    def borrow_book(self,book):
        # Find the book in the library's book list
        for b in self.__book_list:
            if b.get_title() == book:
                # Check if book is available
                if b.is_available():
                    book = b
                else:
                    logger("book borrowed fail")
                    return False
                break
        else:
            logger("book borrowed fail")
            return "No book has been borrowed"

        # Reduce available copies of the book
        book.reduce_available()
        # Update available books CSV
        avail_books = self.load_available_book_list()
        avail_books.loc[avail_books['title'] == book.get_title(), 'copies'] -= 1
        avail_books.to_csv('available_books.csv', index=False)

        # Update loaned books CSV
        loaned_books = self.load_loaned_book_list()

        titles = loaned_books.iloc[:, 0].tolist()
        if book.get_title() not in titles:
            # Add book to loaned books if not already present
            loaned_books = pd.DataFrame(book.get_dict())
            loaned_books.loc[loaned_books['title'] == book.get_title(), 'copies'] = 0
            loaned_books.to_csv('loaned_books.csv', mode='a', index=False, header=False)
            self.__loaned_book_list.append(book)

        # Increase loaned copies
        loaned_books = self.load_loaned_book_list()
        loaned_books.loc[loaned_books['title'] == book.get_title(), 'copies'] += 1
        loaned_books.to_csv('loaned_books.csv', index=False)

        # Update book and list status when no copies are available
        if int(book.get_available()) == 0:
            self.__available_book_list.remove(book)
            book.set_loaned("Yes")

            # Update loan status in CSVs
            loaned_books.loc[loaned_books['title'] == book.get_title(), 'is_loaned'] = "Yes"
            loaned_books.to_csv('loaned_books.csv', index=False)

            books = self.load_book_list()
            books.loc[books['title'] == book.get_title(), 'is_loaned'] = "Yes"
            books.to_csv('books.csv', index=False)

            # Remove book from available books CSV
            first_col_name = avail_books.columns[0]
            df_filtered = avail_books[avail_books[first_col_name] != book.get_title()]
            df_filtered.to_csv("available_books.csv", index=False)


        logger("book borrowed successfully")
        return f"{book.get_title()} has been borrowed"


    
    def return_book(self,book):
        # Find the book in loaned book list
        for b in self.__loaned_book_list:
            if b.get_title() == book:
                book = b
                break
        else:
            logger("book returned fail")
            return f"book {book} not found"

        # Increase available copies
        book.increase_available()

        # Load book-related DataFrames
        books = self.load_book_list()
        available_books = self.load_available_book_list()
        loaned_books = self.load_loaned_book_list()

        # Update copies in available and loaned books
        available_books.loc[available_books['title'] == book.get_title(), 'copies'] = int(book.get_available())
        loaned_books.loc[loaned_books['title'] == book.get_title(), 'copies'] -= 1

        # Save updated DataFrames
        available_books.to_csv('available_books.csv', index=False)
        loaned_books.to_csv('loaned_books.csv', index=False)

        # Update loan status if book was previously loaned
        if book.is_loaned() == "Yes":
            book.set_loaned("No")

            # Update loan status in CSVs
            books.loc[books['title'] == book.get_title(), 'is_loaned'] = book.is_loaned()
            loaned_books.loc[loaned_books['title'] == book.get_title(), 'is_loaned'] = book.is_loaned()

            books.to_csv('books.csv', index=False)
            loaned_books.to_csv('loaned_books.csv', index=False)

            # Add book back to available books
            available_books = pd.DataFrame(book.get_dict())
            available_books.to_csv('available_books.csv', mode='a', index=False, header=False)

            available_books = self.load_available_book_list()
            available_books.loc[available_books['title'] == book.get_title(), 'copies'] = book.get_available()
            available_books.to_csv('available_books.csv', index=False)
            self.__available_book_list.append(book)

        # Remove from loaned books if fully available
        if book.fully_available():

            first_col_name = loaned_books.columns[0]  # Get the name of the first column
            df_filtered = loaned_books[loaned_books[first_col_name] != book.get_title()]
            # Save the updated DataFrame back to the file
            df_filtered.to_csv("loaned_books.csv", index=False)
            self.__loaned_book_list.remove(book)

        logger("book returned successfully")
        return f"book {book.get_title()} returned"

    # Getter methods to retrieve book lists
    def get_books(self):
        return self.__book_list

    def get_available_books(self):
        return self.__available_book_list

    def get_loaned_books(self):
        return self.__loaned_book_list

    def get_waiting_list(self):
        return self.__waiting_list

    def view_books(self,books):
        # Create a string of book titles
        message = ""
        for book in books:
            message += f"{book.get_title()}\n"
        return str(message)



    def remove_book(self,book):
        # Find the book in book list
        for b in self.__book_list:
            if b.get_title() == book:
                book = b
                break
        else:
            return "book not found"

        # Remove book only if fully available
        if book.fully_available():

            # Remove from library lists
            self.__book_list.remove(book)
            self.__available_book_list.remove(book)

            # Load book DataFrames
            books = self.load_book_list()
            available_books = self.load_available_book_list()

            # Filter out the book from CSVs
            books_title = books.columns[0]
            available_books_title = available_books.columns[0]
            books_title_filtered = books[books[books_title] != book.get_title()]
            available_books_title_filtered = available_books[available_books[available_books_title] != book.get_title()]

            # Save updated DataFrames
            books_title_filtered.to_csv('books.csv', index=False)
            available_books_title_filtered.to_csv('available_books.csv', index=False)
            return f"book {book.get_title()} removed"
        else:
            return f"Cant remove the Book {book.get_title()} because is loaned"



    def popular_books(self):
        # Calculate popularity based on loans and waiting list
        popular_books_arr = []

        for i in range(len(self.__book_list)):
            book = self.__book_list[i]
            waiting_count = 0
            if book.get_title() in self.__waiting_list:
                waiting_count =len(self.__waiting_list[book.get_title()])

            # Popularity = (copies loaned + waiting list)
            popular_books_arr.append((waiting_count + book.get_copies() - book.get_available(),book.get_title()))

        # Sort by popularity and get top 10
        popular_books_arr.sort(reverse=True)
        popular_books_arr = popular_books_arr[:10]
        for i in range(10):
            popular_books_arr[i] = f"{i+1}. {popular_books_arr[i][1]}"

        return popular_books_arr
    def pop_waiting_list(self,book):
        # Process waiting list for a book
        if len(self.__waiting_list[book.get_title()]) >0 and book.is_available():
            # Remove first person from waiting list
            first_person = self.__waiting_list[book.get_title()].popleft()
            self.update_waiting_list_file()
            return self.notify(book.get_title(), first_person['name'],first_person['phone'],first_person['email'])


    def notify(self,book_title, name, phone, email):
        # Create notification message for book availability
        return (f"the book {book_title} can borrowed to {name},"
                                     f" please contact by phone {phone} or contact by email {email}")

    def get_book(self,title):
        # Find a book by its title
        for book in self.__book_list:
            if book.get_title() == title:
                return book
        else:
            return None
