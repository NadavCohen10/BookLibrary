
import pandas as pd
import hashlib
from log_write import logger

# פונקציה ליצירת גיבוב של סיסמה
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# פונקציה לטעינת המשתמשים מקובץ CSV ל־DataFrame
def load_users(file_path):
    return pd.read_csv(file_path)

# פונקציה לאימות כניסת משתמש
def authenticate_user(username, password, users_df):
    password_hash = hash_password(password)
    # חיפוש התאמה לנתוני המשתמש
    print(f"username: {username}, password_hash: {password_hash}")
    user_match = users_df[(users_df['username'] == username) & (users_df['password'] == password_hash)]
    if user_match.empty:
        logger("logged in fail")
        return False
    logger("logged in successfully")
    return True


def register_user(username, password):
    df = load_users('users.csv')
    users_df = df.iloc[:, 0].to_list()

    if username in users_df:
        logger("registered fail")
        return "Username already registered"
    else:
        hashed_password = hash_password(password)
        df = pd.DataFrame({'username': [str(username)],'password': [str(hashed_password)]})
        df.to_csv('users.csv', mode='a', index=False, header=False)
        logger("registered successfully")
        return "Registered successfully"
