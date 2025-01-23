
import pandas as pd
import hashlib
from log_write import logger

# Function to create a hash of a password using SHA-256 encryption
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load user data from a CSV file into a DataFrame
def load_users(file_path):
    return pd.read_csv(file_path)

# Function to authenticate a user by checking username and password
def authenticate_user(username, password, users_df):
    # Hash the provided password
    password_hash = hash_password(password)

    # Check if username and hashed password match any user in the DataFrame
    user_match = users_df[(users_df['username'] == username) & (users_df['password'] == password_hash)]

    # Log authentication result and return boolean
    if user_match.empty:
        logger("logged in fail")
        return False
    logger("logged in successfully")
    return True

# Function to register a new user
def register_user(username, password):
    # Load existing users from CSV
    df = load_users('users.csv')
    users_df = df.iloc[:, 0].to_list()

    # Check if username already exists
    if username in users_df:
        logger("registered fail")
        return "Username already registered"
    else:
        # Hash the password and save new user to CSV
        hashed_password = hash_password(password)
        df = pd.DataFrame({'username': [str(username)],'password': [str(hashed_password)]})
        df.to_csv('users.csv', mode='a', index=False, header=False)
        logger("registered successfully")
        return "Registered successfully"
