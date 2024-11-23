import json
import os
from werkzeug.security import generate_password_hash, check_password_hash


class Signin:
    def __init__(self, json_file='users.json', json_file2='trust.json'):
        self.json_file = json_file
        self.json_file2 = json_file2
        print(f"Checking path: {self.json_file}")
        print(f"Checking path: {self.json_file2}")
        print(f"File exists: {os.path.exists(self.json_file)}")
        print(f"File exists: {os.path.exists(self.json_file2)}")
        if not os.path.exists(self.json_file):
            raise FileNotFoundError(f"The file {self.json_file} does not exist.")
        
        if not os.path.exists(self.json_file2):
            raise FileNotFoundError(f"The file {self.json_file2} does not exist.")
    
    def check_signin(self, email, password):
        with open(self.json_file, 'r') as file:
            users = json.load(file)
            for user in users:
                if user["email"] == email:
                    if check_password_hash(user["password"], password):
                        return True, "Welcome back!"
                    else:
                        with open(self.json_file2, 'r') as file2:
                            trusts = json.load(file2)
                            for trust in trusts:
                                if trust["contact_person_email"] == email:
                                    if check_password_hash(trust["password"], password):
                                        return True, "welcome back!"
                                    else:
                                        return False, "Incorrect password."
                                else:
                                    return False, "No such user found."

                    