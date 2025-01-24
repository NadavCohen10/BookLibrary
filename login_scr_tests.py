import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from login_screen import LoginScreen
from main import App


class TestLoginScreen(unittest.TestCase):
    """
    Unit test class for testing the LoginScreen functionality.
    This class includes tests for the initial widget setup,
    successful login, and failed login attempts.
    """

    def setUp(self):
        """
        Set up the necessary environment for the test.
        Initializes the App instance and LoginScreen instance before each test.
        """
        self.root = App()  # Create the main application window
        self.login_screen = LoginScreen(self.root)  # Create the login screen instance

    def tearDown(self):
        """
        Tear down the environment after the test.
        Destroys the App instance to clean up resources.
        """
        self.root.destroy()

    def test_initial_widgets(self):
        """
        Test the initialization of the login screen widgets.
        Verifies that the username and password entries are created and that
        the password entry has the correct 'show' attribute for masking input.
        """
        self.assertIsInstance(self.login_screen.username_entry, tk.Entry)
        self.assertIsInstance(self.login_screen.password_entry, tk.Entry)
        self.assertEqual(self.login_screen.password_entry.cget('show'), '*')

    @patch('auth_utils.load_users')
    @patch('auth_utils.authenticate_user')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_login_user_success(self, mock_showerror, mock_showinfo, mock_authenticate, mock_load_users):
        """
        Test the login process for a successful login.
        Mocks the user authentication to return True and checks that the appropriate
        success message is displayed, and no error message is shown.
        """
        mock_load_users.return_value = MagicMock()  # Mock loading of users
        mock_authenticate.return_value = True  # Mock successful authentication
        self.login_screen.username_entry.insert(0, "user")  # Simulate user input for username
        self.login_screen.password_entry.insert(0, "name")  # Simulate user input for password

        self.login_screen.login_user()  # Attempt to login

        # Assert that the success message was shown and no error message was displayed
        mock_showinfo.assert_called_once_with("Login", "Login successful!")
        mock_showerror.assert_not_called()

    @patch('auth_utils.load_users')
    @patch('auth_utils.authenticate_user')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_login_user_failure(self, mock_showerror, mock_showinfo, mock_authenticate, mock_load_users):
        """
        Test the login process for a failed login.
        Mocks the user authentication to return False and checks that the appropriate
        error message is displayed, and no success message is shown.
        """
        mock_load_users.return_value = MagicMock()  # Mock loading of users
        mock_authenticate.return_value = False  # Mock failed authentication
        self.login_screen.username_entry.insert(0, 'invalid_user')  # Simulate invalid username input
        self.login_screen.password_entry.insert(0, 'wrong_pass')  # Simulate invalid password input

        self.login_screen.login_user()  # Attempt to login

        # Assert that the error message was shown and no success message was displayed
        mock_showerror.assert_called_once_with("Login", "Invalid username or password.")
        mock_showinfo.assert_not_called()


if __name__ == '__main__':
    unittest.main()  # Run the test suite
