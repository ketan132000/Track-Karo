from flask import Flask, redirect, render_template, request
import mysql
from flask_mysqldb import MySQL
# import yaml


app = Flask(__name__)

# CONFIGURE DB
# db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db_name'

mysql = MySQL(app)

email='dev12345@gmail.com'
password='789670'

with app.app_context():
    cur = mysql.connection.cursor()  # USED TO ACCESS DATABASE QUERIES IN SQL.
    cur.execute("INSERT INTO users VALUE (%s, %s)", (email, password))
    mysql.connection.commit()
    cur.close()


# Used to display the data

# @app.route('/users')
# def users():
#     cur= mysql.connection.cursor()
#     resultValue=cur.execute("SELECT * FROM users")
#     if resultValue>0:
#         userDetails=cur.fetchall()
#         return render_template('users.html',userDetails=userDetails)


# if __name__ =='__main__':
#      app.run(debug=True)
