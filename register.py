import re
import mysql.connector
from werkzeug.security import generate_password_hash
from db import get_db_connection

#this is for users to create an account in the website
class Registration:
    def __init__(self):
        try:
            conn = get_db_connection()
            conn.close()
        except Exception as e:
            raise Exception(f"Database connection error: {e}")
    

    def validate_input(self, email, password):

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid E-mail format!!"
        
        if len(password) < 6:
            return False, "Password must be atleast 6 characters long!!"
        
        return True, "validation succesful :)"
    
    def user_exists(self, email):

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            return user is not None
        except Exception as e:
            print(f"Database error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
        
    def register_user(self, username, email, password, phone):

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
            "INSERT INTO users (username, email, password, phone) VALUES (%s, %s, %s, %s)",
            (username, email, generate_password_hash(password), phone)
            )

            conn.commit()
            return True, "Registration Successful!"
        
        except Exception as e:
            return False, f"Database error: {e}"
        
        finally:
            cursor.close()
            conn.close()

            