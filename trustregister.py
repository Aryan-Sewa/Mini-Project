import re
import mysql.connector
from db import get_db_connection
from werkzeug.security import generate_password_hash

#this is for the trust/organisations to regsiter into the website

class TrustRegistration:
    def __init__(self):
        
        try:
            conn = get_db_connection()
            conn.close()
        except Exception as e:
            raise Exception(f"Database connection error: {e}")


    def validate_trust(self, contact_person_email, password):

        if not re.match(r"[^@]+@[^@]+\.[^@]+", contact_person_email):
            return False, "Invalid E-mail format!!"
        
        if len(password) < 6:
            return False, "Password must be atleast 6 characters long!!"
        
        return True, "validation succesful :)"
    
    def trust_exists(self, contact_person_email):

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("select 1 from trusts where contact_person_email = %s", (contact_person_email,))
            trust = cursor.fetchone()
            return trust is not None
        except Exception as e:
            print(f"An error occured: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

        
    def register_trust(self, organisation_name, organisation_type, tax_identification_number, contact_person_name, contact_person_email, contact_person_phone, address, password):
         
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if self.trust_exists(contact_person_email):
            return False, "E-mail already registered."
        else:
            try:
                cursor.execute(
                "insert into trusts (organisation_name, organisation_type, tax_identification_number, contact_person_name, contact_person_email, phone, address, password) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                (organisation_name, organisation_type, tax_identification_number, contact_person_name, contact_person_email, contact_person_phone, address, hashed_password)
                )

                conn.commit()
                return True, f"registration successful!!"
            except Exception as e:
                raise Exception(f"An error occured while registering: {e}")
            finally:
                cursor.close()
                conn.close()

         
        

        


        

            