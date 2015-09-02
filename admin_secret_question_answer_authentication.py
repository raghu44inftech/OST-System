__author__ = 'mullapudi'

import mysql.connector
from converting_uni_string_to_required_stringformat import *

def admin_secret_question(un):
    connection = mysql.connector.connect(user='admin_operations', password='raghu',host='127.0.0.1',database='tracking_system')
    cursor = connection.cursor()

    try:
        cursor.execute("select seq_q from admin_table where un=%s",(un,))
        result=cursor.fetchall()

        if result:
            print str(result[0][0])
            return str(result[0][0])
    finally:
        connection.commit()
        connection.close()

def admin_secret_answer(un):
    connection = mysql.connector.connect(user='admin_operations', password='raghu',host='127.0.0.1',database='tracking_system')
    cursor = connection.cursor()

    try:
        cursor.execute("select pwd,email,seq_a from admin_table where un=%s",(un,))
        result=cursor.fetchall()

        if result:
            return convert_uni_string_to_string(result)
    finally:
        connection.commit()
        connection.close()