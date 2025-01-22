import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

import tkinter as tk
from main_menu import MainMenu
from login_screen import LoginScreen
from register_screen import RegisterScreen
from dashboard_screen import DashboardScreen
from Book import Book
from library import Library


class MyTestCase(unittest.TestCase):
    def test_add_book(self):
        library = Library()
        b1 = Book('addtest','Talya and dotan','No',2,'Classic',2025)
        self.assertFalse(library.is_exist(b1.get_title()))
        self.assertTrue(library.add_book(b1))
        self.assertEqual(library.get_copies(b1),2)
        self.assertTrue(library.is_exist(b1.get_title()))
        self.assertTrue(library.add_book(b1))
        self.assertEqual(library.get_copies(b1),4)
        library.remove_book(b1)#remove him after we finished
    def test_remove_book(self):
        library = Library()
        b1 = Book("remove_test", "Talya and dotan", "No", 2, "Classic", 2025)
        self.assertFalse(library.is_exist(b1.get_title()))
        library.add_book(b1)
        library.remove_book(b1)
        self.assertFalse(library.is_exist(b1.get_title()))
        self.assertEqual(library.get_copies(b1),0)
    def test_borrow_or_return_nonexistent_book(self):
        L = Library()
        nonexistent_book = Book("oop", "Author", "No", 1, "Genre", 2020)
        self.assertFalse(L.is_exist(nonexistent_book.get_title()))
        result = L.borrow_book(nonexistent_book)
        self.assertFalse(result)
        result = L.return_book(nonexistent_book)
        self.assertFalse(result)
        L.remove_book(nonexistent_book)
    def test_add_book_with_waiting_list(self):
        L = Library()
        book = Book("Angry Bird", "author", "No", 3, "Fiction", 1951)
        L.add_book(book)
        self.assertFalse(L.add_to_waiting_list("Angry Bird", "example@gmail.com", "123456789", "david"))
        L.remove_book(book)
    def test_search_new_book(self):
        L = Library()
        book = Book("Divergent", "Author", "No", 1, "Genre", 2025)
        L.add_book(book)
        result = L.search('Title', "Divergent")
        self.assertTrue(result, "Failed to find Enigma")
        result = L.search('Title', "Diverge")
        self.assertTrue(result, "Failed to find new book")
        L.remove_book(book)
    def test_search_by_prefix(self):
        L = Library()
        book = Book("this_is_special_name", "secret", "No", 3, "Fiction", 1925)
        L.add_book(book)
        result = L.search('Title', "this_is")
        self.assertGreater(len(result), 0)
        L.remove_book(book)
    def test_popularity_update(self):
        L = Library()
        book = Book("Popular Book", "Famous Author", "No", 5, "Fiction", 2020)
        L.add_book(book)
        self.assertEqual(L.get_popularity(book), 0, "Popularity should be 0 initially")
        L.borrow_book(book)
        self.assertEqual(L.get_popularity(book), 1, "Popularity should be 1 initially")
        L.return_book(book)
        L.remove_book(book)
    def test_last_first_transfer_to_correct_file(self):
        L = Library()
        book = Book("Hamordim", "Doesnt metter", "No", 1, "Fiction", 1952)
        L.add_book(book)
        L.borrow_book(book)
        L.return_book(book)
        available_books = L.view_available()
        self.assertTrue(any(b.get_title() == "Hamordim" for b in available_books),
                        "Book not in available books after return")
        L.remove_book(book)
    def test_remove_loaned_or_nonexistent_book(self):
        L = Library()
        book = Book("Marry Poppins", "Marry", "No", 2, "Fiction", 1960)
        L.add_book(book)
        L.borrow_book(book)
        result = L.remove_book(book)
        self.assertFalse(result, "Failed to handle removing a loaned book")
        L.return_book(book)
        self.assertTrue(L.remove_book(book))
        nonexistent_book = Book("Nonexistent Book", "Author", "No", 1, "Genre", 2022)
        result = L.remove_book(nonexistent_book)
        self.assertFalse(result, "Failed to handle removing a non-existent book")
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    @patch('tkinter.messagebox.showerror')
    def test_register_existing_user(self, mock_error, mock_to_csv, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({'username': ['dotan'], 'password': ['talya']})
        username_entry = MagicMock()
        password_entry = MagicMock()
        username_entry.get.return_value = "dotan"
        password_entry.get.return_value = "talya"
        with patch('gui.username_entry', username_entry), \
                patch('gui.password_entry', password_entry):
            result = gui.login("Register")
        mock_error.assert_called_once_with("Error", "Username already exists")
        mock_to_csv.assert_not_called()
        self.assertEqual(result, "registered fail")
    @patch('pandas.read_csv')
    @patch('tkinter.messagebox.showerror')
    def test_login_nonexistent_user(self, mock_error, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({'username': ['user1'], 'password': ['hashed_pass1']})
        username_entry = MagicMock()
        password_entry = MagicMock()
        username_entry.get.return_value = "unknown_user"
        password_entry.get.return_value = "somepassword"
        with patch('gui.username_entry', username_entry), \
                patch('gui.password_entry', password_entry):
            result = gui.login("Login")
        mock_error.assert_called_once_with("Error", "username or password incorrect")
        self.assertEqual(result, "logged in fail")
if __name__ == '__main__':
    unittest.main()