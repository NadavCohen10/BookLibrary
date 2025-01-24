import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from register_screen import RegisterScreen
from main import App


class TestRegisterScreen(unittest.TestCase):

    def setUp(self):
        """Set up the test environment by creating a Tkinter root and the RegisterScreen."""
        self.root = App()
        self.root.show_frame = MagicMock()  # Mocking the show_frame method
        self.register_screen = RegisterScreen(self.root)

    def tearDown(self):
        """Destroy the Tkinter root to clean up resources after each test."""
        self.root.destroy()

    @patch("auth_utils.register_user")
    def test_register_user_success(self, mock_register_user):
        """Test successful user registration."""
        # Mock the return value of the register function
        mock_register_user.return_value = "Registration successful."

        # Set input values
        self.register_screen.username_entry.insert(0, "testuser")
        self.register_screen.password_entry.insert(0, "securepassword")

        # Simulate the register button click
        with patch("tkinter.messagebox.showinfo") as mock_msgbox:
            self.register_screen.register_user()
            mock_register_user.assert_called_once_with("testuser", "securepassword")
            mock_msgbox.assert_called_once_with("Register", "Registration successful.")

    @patch("auth_utils.register_user")
    def test_register_user_failure(self, mock_register_user):
        """Test registration failure due to duplicate username or other issues."""
        mock_register_user.return_value = "Username already exists."

        # Set input values
        self.register_screen.username_entry.insert(0, "existinguser")
        self.register_screen.password_entry.insert(0, "password123")

        # Simulate the register button click
        with patch("tkinter.messagebox.showinfo") as mock_msgbox:
            self.register_screen.register_user()
            mock_register_user.assert_called_once_with("existinguser", "password123")
            mock_msgbox.assert_called_once_with("Register", "Username already exists.")

    def test_back_button_functionality(self):
        """Test if clicking 'Back' calls the show_frame method with 'MainMenu'."""
        self.register_screen.master.show_frame = MagicMock()
        self.register_screen.master.show_frame("MainMenu")
        self.register_screen.master.show_frame.assert_called_once_with("MainMenu")

    def test_ui_elements_exist(self):
        """Check if all UI elements (labels, entries, buttons) are created."""
        widgets = [child for child in self.register_screen.winfo_children()]

        # Check that expected widgets exist
        self.assertTrue(any(isinstance(w, tk.Label) and w.cget("text") == "Register" for w in widgets))
        self.assertTrue(any(isinstance(w, tk.Entry) for w in widgets))
        self.assertTrue(any(isinstance(w, tk.Button) and w.cget("text") == "Register" for w in widgets))
        self.assertTrue(any(isinstance(w, tk.Button) and w.cget("text") == "Back" for w in widgets))


if __name__ == '__main__':
    unittest.main()
