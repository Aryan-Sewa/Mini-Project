import mysql.connector
from db import get_db_connection
from werkzeug.security import check_password_hash


class Signin:
    def __init__(self):
        try:
            conn = get_db_connection()
            conn.close()
        except Exception as e:
            return Exception(f"An error occured in sign-in while connecting with DB: {e}")

    
    def check_signin(self, email, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
        # Check the users table
            cursor.execute("select password from user where email = %s", (email,))
            result = cursor.fetchone()
            if result:
                stored_password_hash = result[0]
                if check_password_hash(stored_password_hash, password):
                    return True, "Sign-in succesful. Welcome!!", "user"
                else:
                    return False, "Wrong password. Please enter the correct password!!", None
        #check the trusts table
            cursor.execute("select password from trusts where email = %s", (email,))
            result = cursor.fetchone()
            if result:
                stored_password_hash = result[0]
                if check_password_hash(stored_password_hash, password):
                    return True, "Sign-in successful. Welcome!!", "trust"
                else:
                    return False, "Wrong password. Please enter the correct password!!", None
            
            return False, "No such user found with this eamil!!", None
        
        except Exception as e:
            return False, f"An error occured while checking the sign-in credentials: {e}", None 
        finally:
            cursor.close()
            conn.close()
    
    def get_user_data_by_email(self, email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
        #again check the users table 
            cursor.execute("select username from users where email = %s", (email,))
            user = cursor.fetchone()
            if user:
                return {
                    "username": user.get("username", ""),
                    "profile_pic": "static/default.png",
                    "type": "user"
                }
            
        #similarly again check the trusts table also
            cursor.execute("select contact_person_name from trusts where email = %s", (email,))
            trust = cursor.fetchone()
            if trust:
                return {
                    "username": trust.get("contact_person_name",""),
                    "profile_pic": "static/default/png",
                    "type": "trust"
                }
        
            return None
    
        except Exception as e:
            print(f"Erro occured while updating the profile: {e}")
            return None
        finally:
            cursor.close()
            conn.close()


                    