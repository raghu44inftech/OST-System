__author__ = 'mullapudi'


import mysql.connector
from converting_uni_string_to_required_stringformat import *

def track_status_from_database(tid):
    connection = mysql.connector.connect(user='admin_operations', password='raghu',host='127.0.0.1',database='tracking_system')
    cursor = connection.cursor()

    try:
        cursor.execute("select * from track_table where tid=%s",(tid,))
        result=cursor.fetchall()

        if result:
            return convert_uni_string_to_string(result)
    finally:
        connection.commit()
        connection.close()
