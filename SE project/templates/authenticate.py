# authenticate.py

import mysql.connector

def authenticate_user(username, password):
    try:
        # Database connection details
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Goog@0004',
            'database': 'billing'  # Use the name of your database
        }
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "SELECT * FROM accounts WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
