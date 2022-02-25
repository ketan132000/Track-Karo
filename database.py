from flask import Flask, redirect,render_template,request
import mysql
from flask_mysqldb import MySQL
import yaml




app= Flask(__name__)

#CONFIGURE DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method== 'POST':
        
        #Fetch Form DATA or sending data to db
        userDetails=request.form
        name=userDetails['name']
        email=userDetails['email']
        cur= mysql.connection.cursor() #USED TO ACCESS DATABASE QUERIES IN SQL.
        cur.execute("INSERT INTO users(name,email) VALUE (%s, %s)",(name,email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')

#Used to display the data

@app.route('/users')
def users():
    cur= mysql.connection.cursor()
    resultValue=cur.execute("SELECT * FROM users")
    if resultValue>0:
        userDetails=cur.fetchall() 
        return render_template('users.html',userDetails=userDetails)


if __name__ =='__main__':
     app.run(debug=True)
