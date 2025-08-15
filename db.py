# filepath: c:\Users\aryan\OneDrive\Desktop\GiveItForward1-main\db.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='flaskuser',
        password='JoJo',
        database='giveitforward'
    )
