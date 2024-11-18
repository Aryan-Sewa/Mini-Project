import re
import json
from werkzeug.security import generate_password_hash, check_password_hash
from os.path import exists

class TrustRegistration:
    def __init__(self, json_file='trusts.json'):
        
        self.json_file = json_file
        if not exists(self.json_file):
            with open(self.json_file, 'w') as file:
                json.dump([], file)

    def validate_trust(self, contact_person_email, password):

        if not re.match(r"[^@]+@[^@]+\.[^@]+", contact_person_email):
            return False, "Invalid E-mail format!!"
        
        if len(password) < 6:
            return False, "Password must be atleast 6 characters long!!"
        
        return True, "validation succesful :)"
    
    def trust_exists(self, contact_person_email):

        with open(self.json_file, 'r') as file:
            trusts = json.load(file)
            return any(trust['contact_person_email'] == contact_person_email for trust in trusts)
        
    def register_trust(self, organisation_name, organisation_type, tax_identification_number, contact_person_name, contact_person_email, contact_person_phone, address, password):
         
         if self.trust_exists(contact_person_email):
             return False, "E-mail already registered."
         
         hasshed_password = generate_password_hash(password)

         new_trust = {
             "organisation_name": organisation_name,
             "organisation_type": organisation_type,
             "tax_identification_number": tax_identification_number,
             "contact_person_name": contact_person_name,
             "contact_person_email": contact_person_email,
             "phone": contact_person_phone,
             "address": address,
             "password": hasshed_password
         }

         try:
            with open(self.json_file, 'r') as file:
                 trusts = json.load(file)
            trusts.append(new_trust)

            with open(self.json_file, 'w') as file:
                json.dump(trusts, file, indent=4)
            
            return True, "Trust Registered Successfully :)"
         except Exception as e:
             return False, f"Registration Failed: {e}"

            