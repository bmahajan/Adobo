from flask import Flask, request, render_template, redirect
import os
app = Flask(__name__)
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


@app.route("/checkin_create_user")
def parseRequest():
    email = request.args.get("email")
    id = request.args.get("id")
    try:
        connection = pymysql.connect(host=os.getenv("MYSQL_HOST"),
                                     user=os.getenv("MYSQL_USER"),
                                     password=os.getenv("MYSQL_PASS"),
                                     db= os.getenv("MYSQL_DB"),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (email, id) VALUES (%s, %s);", (email, id))
            connection.commit()
            connection.close()
    except Exception as e:
        return str(e)
    return "success"

@app.route("/check_user_event")
def check_user_account():
    id = request.args.get("id")
    event = request.args.get("event")
    try:
        connection = pymysql.connect(host=os.getenv("MYSQL_HOST"),
                                     user=os.getenv("MYSQL_USER"),
                                     password=os.getenv("MYSQL_PASS"),
                                     db= os.getenv("MYSQL_DB"),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s;", (id))
            result = cursor.fetchall()[0]
            if event not in result or result[event] == 1:
                connection.close()
                return "consumed"
            else:
                print(event)
                cursor.execute("UPDATE users SET " + event + "= 1 WHERE id = %s", (id))
                connection.commit()
                connection.close();
    except Exception as e:
        return str(e)
    return "success"



if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=True)
