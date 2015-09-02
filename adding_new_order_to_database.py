__author__ = 'mullapudi'

import mysql.connector

from random import randint
def addnew_to_database(pid,usid,address,status,phno,email,ord_date,del_date):
    connection = mysql.connector.connect(user='admin_operations', password='raghu',host='127.0.0.1',database='tracking_system')
    cursor = connection.cursor()

    cursor.execute("select tid from track_table where tid")
    existing=cursor.fetchall()
    existing_new_format=[]
    for i in existing:
        existing_new_format.append(str(i[0]))

    tid=str(randint(1,1000000))
    while tid in existing_new_format:
        tid=str(randint(1,1000000))

    try:
        print tid,pid,usid,address,status,phno,email,ord_date,del_date
        cursor.execute("insert into track_table (tid,pid,usid,address,status,phno,email,ord_date,del_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(tid,pid,usid,address,status,phno,email,ord_date,del_date))
        cursor.execute("insert into user_table (tid,usid) values(%s,%s)",(tid,usid))
        return tid
    finally:
        connection.commit()
        connection.close()

