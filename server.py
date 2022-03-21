from click import password_option
from flask import Flask, redirect, render_template, request
import requests
from bs4 import BeautifulSoup
from product import Product
import mysql
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mN2bFn@1'
app.config['MYSQL_DB'] = 'track_karo'

mysql = MySQL(app)


# email='gauravsharma@gmail.com'
# password='123456'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails=request.form
        username=userDetails['username']
        password=userDetails['password']
        print(username,password)

        with app.app_context():
            cur = mysql.connection.cursor()  # USED TO ACCESS DATABASE QUERIES IN SQL.
            st="SELECT * FROM users WHERE email='"+username+"' AND password='"+password+"';"
            print(st)
            ob=cur.execute(st);
            mysql.connection.commit()
            cur.close()
        print(ob)

        if (ob==0):
            return render_template('invalid.html')
        else:
            return redirect('/Home')
    return render_template('login.html')

@app.route('/Home', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        productName = request.form
        search = productName['search']
        print(search)
        prod_classes=[["div","_4rR01T"],["a","s1Q9rs"],["a","IRpwTa"]]
        link_classes=[["a","_1fQZEK"],["a","_2rpwqI"],["a","_2UzuFa"]]
        img_classes=[["img","_396cs4 _3exPp9"],["img","_396cs4 _3exPp9"],["img","_2r_T1I"]]
        price_classes=[["div","_30jeq3 _1_WHN1"],["div","_30jeq3"],["div","_30jeq3"]]
        URL = "https://www.flipkart.com/search?q="+search
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')

        for i in range(0,3):
            p=prod_classes[i]
            productList = soup.findAll(p[0], attrs={'class': p[1]})
            if len(productList) != 0:
                q=img_classes[i]
                r=price_classes[i]
                s=link_classes[i]

                imageList = soup.findAll(q[0], attrs={'class': q[1]})
                priceList = soup.findAll(r[0], attrs={'class': r[1]})
                linkList = soup.findAll(s[0], attrs={'class': s[1]})

                n=len(productList)
                final_product=[]
                for j in range(0,n):
                    if imageList[j].get("src")=='':
                        imageList[j]={'src':'https://lightwidget.com/wp-content/uploads/local-file-not-found-480x488.png'}
                    temp=Product(productList[j].text,priceList[j].text,imageList[j].get("src"),linkList[j].get("href"))
                    final_product.append(temp)
                return render_template('index.html', len=n ,products=final_product)
    return render_template('index.html', len=0)


if __name__ == '__main__':
    app.run(debug=True)
