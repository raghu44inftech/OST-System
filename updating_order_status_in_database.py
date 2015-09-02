__author__ = 'mullapudi'

import mysql.connector
from converting_uni_string_to_required_stringformat import *

def updating_status_in_database(tid,status):
    connection = mysql.connector.connect(user='admin_operations', password='raghu',host='127.0.0.1',database='tracking_system')
    cursor = connection.cursor()

    try:
        cursor.execute("select tid from track_table where tid")
        existing=cursor.fetchall()
        existing_new_format=[]
        for i in existing:
            existing_new_format.append(str(i[0]))

        if tid in existing_new_format:
            cursor.execute ("UPDATE track_table SET status=%s where tid=%s", (status,tid))
            cursor.execute("select email,status from track_table where tid=%s",(tid,))
            result=cursor.fetchall()
            return convert_uni_string_to_string(result)
        else:
            return False
    finally:
        connection.commit()
        connection.close()