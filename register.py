import re
import json
from werkzeug.security import generate_password_hash, check_password_hash
from os.path import exists

class Registration:
    def __init__(self, json_file='users.json'):
        
        self.json_file = json_file
        if not exists(self.json_file):
            with open(self.json_file, 'w') as file:
                json.dump([], file)

    def validate_input(self, email, password):

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid E-mail format!!"
        
        if len(password) < 6:
            return False, "Password must be atleast 6 characters long!!"
        
        return True, "validation succesful :)"
    
    def user_exists(self, email):

        with open(self.json_file, 'r') as file:
            users = json.load(file)
            return any(user['email'] == email for user in users)
        
    def register_user(self, username, email, password, phone):
         
         if self.user_exists(email):
             return False, "E-mail already registered."
         
         hasshed_password = generate_password_hash(password)

         new_user = {
             "username": username,
             "email": email,
             "password": hasshed_password,
             "phone": phone
         }

         try:
            with open(self.json_file, 'r') as file:
                 users = json.load(file)
            users.append(new_user)

            with open(self.json_file, 'w') as file:
                json.dump(users, file, indent=4)
            
            return True, "Users Registered Successfully :)"
         except Exception as e:
             return False, f"Registration Failed: {e}"

            