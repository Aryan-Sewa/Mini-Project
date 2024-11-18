import json
import os
from werkzeug.security import generate_password_hash, check_password_hash


class Signin:
    def __init__(self, json_file='users.json'):
        self.json_file = json_file
        print(f"Checking path: {self.json_file}")
        print(f"File exists: {os.path.exists(self.json_file)}")
        if not os.path.exists(self.json_file):
            raise FileNotFoundError(f"The file {self.json_file} does not exist.")
    
    def check_signin(self, email, password):
        with open(self.json_file, 'r') as file:
            users = json.load(file)
            for user in users:
                if user["email"] == email:
                    if check_password_hash(user["password"], password):
                        return True, "Welcome back!"
                    else:
                        return False, "Incorrect password."
            return False, "No such user found."

                    