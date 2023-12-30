# db_connection.py
import mysql.connector

def establish_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123@Sanjay',
            database='pin_code_store'
        )
        return connection
    except mysql.connector.Error as error:
        print("Error connecting to MySQL:", error)
        return None
