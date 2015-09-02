__author__ = 'mullapudi'

import mysql.connector

def verify_from_database_admin(un,pwd):
    connection = mysql.connector.connect(user='admin_operations', password='raghu',host='127.0.0.1',database='tracking_system')
    try:
        cursor = connection.cursor()
        cursor.execute("select * from admin_table")

        for row in cursor.fetchall():
            if row[0] == un and row[1] == pwd:
                return True
        else:
            return False
    finally:
        connection.close()
