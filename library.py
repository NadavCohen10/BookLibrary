from pyexpat.errors import messages

from Book import Book as bk
import csv
import pandas as pd
from collections import deque
from log_write import logger
from strategy_search import SearchContext, TitleSearchStrategy, YearSearchStrategy


class Library():
    book_list = []
    waiting_list = {}
    loaned_book_list = []
    available_book_list = []
    notifications = []

    def load_book_list(self):
        return pd.read_csv('books.csv')
    def load_loaned_book_list(self):
        return pd.read_csv('loaned_books.csv')
    def load_available_book_list(self):
        return pd.read_csv('available_books.csv')
    def load_waiting_list(self):
        return pd.read_csv('waiting_list.csv')


    def set_book(self):
        books = self.load_book_list()
        for _, row in books.iterrows():
            book = bk(row["title"], row["author"], row["is_loaned"], row["copies"], row["genre"], row["year"])
            Library.book_list.append(book)

        for book in Library.book_list:
            books = pd.DataFrame(book.get_dict())
            if book.is_available():
                #books.to_csv('available_books.csv', mode='a', index=False, header=False)
                Library.available_book_list.append(book)
            else:
               # books.to_csv('loaned_books.csv', mode='a', index=False, header=False)
                Library.loaned_book_list.append(book)


        loaned_books = self.load_loaned_book_list()
        for _, row in loaned_books.iterrows():
            if row['is_loaned'] == "No":
                for book in Library.book_list:
                    if book.get_title() == row['title']:
                        book.reduce(row['copies'])
                        Library.loaned_book_list.append(book)

        waiting = self.load_waiting_list()
        for _, row in waiting.iterrows():
            if row['title'] not in Library.waiting_list:
                Library.waiting_list[row['title']] = deque()

            person = {'name': row['name'],'phone': row['phone'], 'email': row['email']}
            Library.waiting_list[row['title']].append(person)


    def add_book(self,book):
        avail_books = self.load_available_book_list()
        books = self.load_book_list()
        # Select only the first column (by index)
        titles = books.iloc[:,0 ]  # Select the first column by index
        titles = titles.tolist()
        if book.get_title() not in titles:

            avail_books = pd.DataFrame(book.get_dict())

            avail_books.to_csv('available_books.csv', mode='a', index=False, header=False)
            avail_books.to_csv('books.csv', mode='a', index=False, header=False)

            Library.book_list.append(book)
            Library.available_book_list.append(book)

            logger('book added successfully')
            return f"Added {book.get_title()} to books list"

        else:

            titles = avail_books.iloc[:, 0].tolist()
            if book.get_title() not in titles:
                avail_books = pd.DataFrame(book.get_dict())
                avail_books.to_csv('available_books.csv', mode='a', index=False, header=False)


            else:
                avail_books.loc[avail_books['title'] == book.get_title(), 'copies'] += book.get_copies()
                avail_books.to_csv('available_books.csv', index=False)


            books.loc[books['title'] == book.get_title(), 'copies'] += book.get_copies()
            # Save the updated DataFrame back to the CSV
            books.to_csv('books.csv', index=False)


            b = self.get_book(book.get_title())


            b.add_copies(str(book.get_copies()))
            if b.is_loaned() == "Yes":
                b.set_loaned("No")
                Library.available_book_list.append(b)

            books.loc[books['title'] == book.get_title(), 'is_loaned'] = "No"
            loaned_books = self.load_loaned_book_list()
            loaned_books.loc[loaned_books['title'] == book.get_title(), 'is_loaned'] = "No"

                # Save the updated DataFrame back to the CSV
            books.to_csv('books.csv', index=False)
            loaned_books.to_csv('loaned_books.csv', index=False)

            logger('book added successfully')
            return f"Added {book.get_copies()} copies to the book {book.get_title()}"

            # if book.get_title() in Library.waiting_list:
            #     while len(Library.waiting_list[book.get_title()]) > 0 and b.is_available():
            #         first_person = Library.waiting_list[book.get_title()].popleft()
            #         self.update_waiting_list_file()
            #         self.notify(book.get_title(), first_person['name'], first_person['phone'],
            #                     first_person['email'])
            #         print(self.borrow_book(book.get_title()))



    def add_to_wait_list(self,book,name,phone,email):


        if book not in Library.waiting_list:
            Library.waiting_list[book] = deque()

        for _, person in enumerate(Library.waiting_list[book]):
            if str(person["phone"]) == str(phone):
                return "Person is already in waiting list"

        Library.waiting_list[book].append({"name": name, "phone": phone, "email": email})
        self.update_waiting_list_file()
        return f"{name} has been added to waiting list of the book {book}"


    def update_waiting_list_file(self):
        waiting = self.load_waiting_list()


        if waiting is not None:
            headers = ["title", "name", "phone", "email"]
            waiting = pd.DataFrame(columns=headers)
            waiting.to_csv('waiting_list.csv', index=False)

        for title in Library.waiting_list:
            for person in Library.waiting_list[title]:
                data = {
                    'title': [title],
                    'name': [person["name"]],
                    'phone': [person["phone"]],
                    'email': [person["email"]]
                }
                data = pd.DataFrame(data)
                data.to_csv('waiting_list.csv', mode='a', index=False, header=False)


    def borrow_book(self,book):
        for b in Library.book_list:
            if b.get_title() == book:
                if b.is_available():
                    book = b
                else:
                    logger("book borrowed fail")
                    return False
                    #return self.add_to_wait_list(b)
                break
        else:
            logger("book borrowed fail")
            return "No book has been borrowed"

        book.reduce_available()
        # reduce avail' copies
        avail_books = self.load_available_book_list()
        avail_books.loc[avail_books['title'] == book.get_title(), 'copies'] -= 1
        avail_books.to_csv('available_books.csv', index=False)

        # increace loaned copies
        loaned_books = self.load_loaned_book_list()

        titles = loaned_books.iloc[:, 0].tolist()
        if book.get_title() not in titles:

            loaned_books = pd.DataFrame(book.get_dict())
            loaned_books.loc[loaned_books['title'] == book.get_title(), 'copies'] = 0
            loaned_books.to_csv('loaned_books.csv', mode='a', index=False, header=False)
            Library.loaned_book_list.append(book)

        loaned_books = self.load_loaned_book_list()
        loaned_books.loc[loaned_books['title'] == book.get_title(), 'copies'] += 1
        loaned_books.to_csv('loaned_books.csv', index=False)


        if int(book.get_available()) == 0:

            Library.available_book_list.remove(book)
            book.set_loaned("Yes")
            loaned_books.loc[loaned_books['title'] == book.get_title(), 'is_loaned'] = "Yes"
            loaned_books.to_csv('loaned_books.csv', index=False)

            books = self.load_book_list()
            books.loc[books['title'] == book.get_title(), 'is_loaned'] = "Yes"
            books.to_csv('books.csv', index=False)

            first_col_name = avail_books.columns[0]  # Get the name of the first column
            df_filtered = avail_books[avail_books[first_col_name] != book.get_title()]
            df_filtered.to_csv("available_books.csv", index=False)


        logger("book borrowed successfully")
        return f"{book.get_title()} has been borrowed"


    
    def return_book(self,book):
        for b in Library.loaned_book_list:
            if b.get_title() == book:
                book = b
                break
        else:
            logger("book returned fail")
            return f"book {book} not found"

        book.increase_available()


        books = self.load_book_list()
        available_books = self.load_available_book_list()
        loaned_books = self.load_loaned_book_list()

        available_books.loc[available_books['title'] == book.get_title(), 'copies'] = int(book.get_available())
        loaned_books.loc[loaned_books['title'] == book.get_title(), 'copies'] -= 1


        available_books.to_csv('available_books.csv', index=False)
        loaned_books.to_csv('loaned_books.csv', index=False)


        if book.is_loaned() == "Yes":

            book.set_loaned("No")

            books.loc[books['title'] == book.get_title(), 'is_loaned'] = book.is_loaned()
            loaned_books.loc[loaned_books['title'] == book.get_title(), 'is_loaned'] = book.is_loaned()


            books.to_csv('books.csv', index=False)
            loaned_books.to_csv('loaned_books.csv', index=False)

            available_books = pd.DataFrame(book.get_dict())
            available_books.to_csv('available_books.csv', mode='a', index=False, header=False)

            available_books = self.load_available_book_list()
            available_books.loc[available_books['title'] == book.get_title(), 'copies'] = book.get_available()
            available_books.to_csv('available_books.csv', index=False)
            Library.available_book_list.append(book)

            # if book.get_title() in Library.waiting_list:
            #     if len(Library.waiting_list[book.get_title()]) > 0:
            #         first_person = Library.waiting_list[book.get_title()].popleft()
            #         self.update_waiting_list_file()
            #         self.notify(book.get_title(), first_person['name'],first_person['phone'],first_person['email'])
            #         print(self.borrow_book(book.get_title()))


        if book.fully_available():

            first_col_name = loaned_books.columns[0]  # Get the name of the first column
            df_filtered = loaned_books[loaned_books[first_col_name] != book.get_title()]
            # Save the updated DataFrame back to the file
            df_filtered.to_csv("loaned_books.csv", index=False)
            Library.loaned_book_list.remove(book)

        logger("book returned successfully")
        return f"book {book.get_title()} returned"


    def get_books(self):
        return Library.book_list

    def get_available_books(self):
        return Library.available_book_list

    def get_loaned_books(self):
        return Library.loaned_book_list

    def view_books(self,books):
        message = ""
        for book in books:
            message += f"{book.get_title()}\n"
        return str(message)



    def remove_book(self,book):
        for b in Library.book_list:
            if b.get_title() == book:
                book = b
                break
        else:
            return "book not found"

        if book.fully_available():
            Library.book_list.remove(book)
            Library.available_book_list.remove(book)
            books = self.load_book_list()
            available_books = self.load_available_book_list()

            books_title = books.columns[0]
            available_books_title = available_books.columns[0]
            books_title_filtered = books[books[books_title] != book.get_title()]
            available_books_title_filtered = available_books[available_books[available_books_title] != book.get_title()]
            books_title_filtered.to_csv('books.csv', index=False)
            available_books_title_filtered.to_csv('available_books.csv', index=False)
            return f"book {book.get_title()} removed"
        else:
            return f"Cant remove the Book {book.get_title()} because is loaned"



    def popular_books(self):
        popular_books_arr = []


        for i in range(len(Library.book_list)):
            book = Library.book_list[i]
            waiting_count = 0
            if book.get_title() in Library.waiting_list:
                waiting_count =len(Library.waiting_list[book.get_title()])

            popular_books_arr.append((waiting_count + book.get_copies() - book.get_available(),book.get_title()))

        popular_books_arr.sort(reverse=True)

        popular_books_arr = popular_books_arr[:10]
        for i in range(10):
            popular_books_arr[i] = f"{i+1}. {popular_books_arr[i][1]}"

        return popular_books_arr
    def pop_waiting_list(self,book):
        if len(Library.waiting_list[book.get_title()]) >0 and book.is_available():
            first_person = Library.waiting_list[book.get_title()].popleft()
            self.update_waiting_list_file()
            return self.notify(book, first_person['name'],first_person['phone'],first_person['email'])


    def notify(self,book_title, name, phone, email):
        # Library.notifications.append(f"the book {book_title} can borrowed to {name},"
        #                               f" please contact by phone {phone} or contact by email {email}")
        return (f"the book {book_title} can borrowed to {name},"
                                     f" please contact by phone {phone} or contact by email {email}")

    def get_book(self,title):
        for book in Library.book_list:
            if book.get_title() == title:
                return book
        else:
            return None


if __name__ == '__main__':
    book = bk("bbb", "ggg", "No", 2,"Fiction",1990 )
    boo1k = bk("bbbbb", "ggg", "No", 2, "Fiction", 1990)
    c = Library()
    c.set_book()
    #c.add_book(book)
   #
   #  #print(c.add_to_wait_list(book))
   #  #print(c.add_to_wait_list(book))
   #  #c.print_books()
   #  print("________________________________")
   #  for i in range(7):
    #context = SearchContext(YearSearchStrategy())

    #print(context.search(c.book_list, "1990"))

    #
    print(c.return_book(book))
    if len(c.notifications) != 0:
         print(c.notifications.pop())
    #print(c.borrow_book(book))
    #print(c.return_book(book))
    #c.popular_books()
    #print(c.borrow_book1(book))
    #print(c.borrow_book1(book))
    #print(c.borrow_book1(book))
    #print(c.remove_book1(book))
   #  #c.add_book(book)
   #  print(c.borrow_book(book))
   #  #c.print_books()
   #  print("\n\n")
   #  print(book)
   #  for i in range(7):
   #      print(c.return_book(book))
   #  c.print_books()
   #  #print(book)
   #
   # #  c.remove_book(Library.book_list[-2])
   #



