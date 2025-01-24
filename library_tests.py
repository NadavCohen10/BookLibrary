import unittest
from Book import Book as bk
from library import Library

class TestLibraryMethods(unittest.TestCase):
    """
    Unit test class for testing the methods of the Library class.
    This class contains tests for adding books, borrowing, returning,
    removing books, and various other library functionalities.
    """

    def setUp(self):
        """
        Set up the necessary environment for the test.
        Initializes a Library instance and a few Book instances before each test.
        """
        self.library = Library()  # Create a new library instance
        self.library.set_book()  # Set up initial books in the library
        self.book1 = bk("Test Book", "Author", "No", 1, "Fiction", 2020)  # Create a test book instance
        self.book2 = bk("Another Book", "Another Author", "Yes", 1, "Non-Fiction", 2018)  # Another test book

    def test_add_book(self):
        """
        Test adding a book to the library.
        Verifies that the result contains 'Added' when a book is successfully added,
        and checks that the book can be removed afterward.
        """
        result = self.library.add_book(self.book1)  # Add the first book
        self.assertIn("Added", result)  # Assert that the book was added successfully
        self.library.remove_book(self.book1.get_title())  # Clean up by removing the book

    def test_add_to_wait_list(self):
        """
        Test adding a book to the waiting list.
        Verifies that a book can be added to the waiting list and removes it after testing.
        """
        result = self.library.add_to_wait_list("Test Book", "John Doe", "123456", "john@example.com")
        self.assertIn("added to waiting list", result)  # Check if the user was added to the wait list
        self.library.get_waiting_list()["Test Book"].popleft()  # Remove the user from the wait list
        self.library.update_waiting_list_file()  # Update the wait list file after modification

    def test_borrow_book(self):
        """
        Test borrowing a book from the library.
        Verifies successful borrowing, checking that a book can be borrowed and an error
        is returned when trying to borrow a non-existent or unavailable book.
        """
        self.library.add_book(self.book1)  # Add the first book to the library
        result = self.library.borrow_book("Test Book")  # Borrow the test book
        self.assertIn("has been borrowed", result)  # Check if the borrow was successful
        result = self.library.borrow_book("Test Book")  # Try to borrow the same book again
        self.assertIn("False", str(result))  # Should return false since it's already borrowed
        result = self.library.borrow_book("Test Book2")  # Try to borrow a non-existent book
        self.assertIn("No", result)  # Should return 'No' since the book does not exist
        self.library.return_book("Test Book")  # Return the borrowed book
        self.library.remove_book("Test Book")  # Clean up by removing the book

    def test_return_book(self):
        """
        Test returning a borrowed book to the library.
        Verifies that the book is successfully returned, and an appropriate error is returned
        when trying to return a book that was not borrowed.
        """
        self.library.add_book(self.book1)  # Add the first book to the library
        self.library.borrow_book("Test Book")  # Borrow the test book
        result = self.library.return_book("Test Book")  # Return the borrowed book
        self.assertIn("returned", result)  # Check if the book was successfully returned
        result = self.library.return_book("Test Book2")  # Try to return a book that was not borrowed
        self.assertIn("not", result)  # Should return 'not borrowed' for the non-existent book
        self.library.remove_book("Test Book")  # Clean up by removing the book

    def test_remove_book(self):
        """
        Test removing a book from the library.
        Verifies that a book can be removed successfully if not loaned,
        and an appropriate message is displayed if it is loaned out.
        """
        self.library.add_book(self.book1)  # Add the first book to the library
        self.library.borrow_book(self.book1.get_title())  # Borrow the test book
        result = self.library.remove_book("Test Book")  # Try to remove the borrowed book
        self.assertIn("loaned", result)  # Should indicate the book is loaned out and cannot be removed
        self.library.return_book(self.book1.get_title())  # Return the borrowed book
        result = self.library.remove_book("Test Book")  # Remove the book after returning it
        self.assertIn("removed", result)  # Should indicate the book was successfully removed
        result = self.library.remove_book("Test Book2")  # Try to remove a non-existent book
        self.assertIn("found", result)  # Should indicate that the book was not found

    def test_get_books(self):
        """
        Test getting all the books in the library.
        Verifies that the result is a list of books.
        """
        self.assertIsInstance(self.library.get_books(), list)  # Ensure the result is a list

    def test_get_available_books(self):
        """
        Test getting all available books in the library.
        Verifies that the result is a list of available books.
        """
        self.assertIsInstance(self.library.get_available_books(), list)  # Ensure the result is a list

    def test_get_loaned_books(self):
        """
        Test getting all loaned books in the library.
        Verifies that the result is a list of loaned books.
        """
        self.assertIsInstance(self.library.get_loaned_books(), list)  # Ensure the result is a list

    def test_get_waiting_list(self):
        """
        Test getting the waiting list for books.
        Verifies that the result is a dictionary containing waiting list information.
        """
        self.assertIsInstance(self.library.get_waiting_list(), dict)  # Ensure the result is a dictionary

    def test_popular_books(self):
        """
        Test getting the popular books in the library.
        Verifies that the result is a list with a length of at most 10.
        """
        popular_books = self.library.popular_books()  # Get the popular books
        self.assertIsInstance(popular_books, list)  # Ensure the result is a list
        self.assertLessEqual(len(popular_books), 10)  # Ensure there are at most 10 popular books

    def test_notify(self):
        """
        Test sending a notification for a book on the waiting list.
        Verifies that the notification message includes contact instructions.
        """
        notification = self.library.notify("Test Book", "John Doe", "123456", "john@example.com")
        self.assertIn("please contact by phone", notification)  # Ensure the message contains contact instructions

    def test_get_book(self):
        """
        Test getting a specific book from the library.
        Verifies that a valid book can be fetched based on its title.
        """
        self.library.add_book(self.book1)  # Add the first book to the library
        book = self.library.get_book("Test Book")  # Fetch the test book by title
        self.assertIsNotNone(book)  # Ensure the book is not None

if __name__ == '__main__':
    unittest.main()  # Run the test suite
