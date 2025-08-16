# filepath: c:\Users\aryan\OneDrive\Desktop\GiveItForward1-main\db.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='JoJo',
        database='giveitforward'
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    #create users table if it doesn't exist
    cursor.execute("""
                   create table if not exists users (
                   id int auto_increment primary key,
                   username varchar(255) not null,
                   email varchar(255) not null unique,
                   password varchar(255) not null
                   )""")
    
    #create trusts table if it doesn't exist
    cursor.execute("""
                   create table if not exists trusts (
                   id int auto_increment primary key,
                   organisation_name varchar(255) not null,
                   organisation_type varchar(255) not null,
                   tax_identification_number varchar(255) not null unique,
                   contact_person_name varchar(255) not null,
                   contact_person_email varchar(255) not null unique,
                   phone varchar(20),
                   address text,
                   password varchar(255) not null
                   )""")

    conn.commit()
    cursor.close()
    conn.close()
    
