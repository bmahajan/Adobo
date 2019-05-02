from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

def get_emails():
    try:
        connection = pymysql.connect(host=os.getenv("MYSQL_HOST"),
                                     user=os.getenv("MYSQL_USER"),
                                     password=os.getenv("MYSQL_PASS"),
                                     db= os.getenv("MYSQL_DB"),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT email FROM users WHERE HoppyHour=1 ORDER BY email;")
            result = cursor.fetchall()
    except Exception as e:
        return str(e)
    return result

for i in get_emails():
    print(i["email"])
