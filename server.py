from click import password_option
from flask import Flask, redirect, render_template, request
import requests
from bs4 import BeautifulSoup
from product import Product
import mysql
from flask_mysqldb import MySQL
import smtplib


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mN2bFn@1'
app.config['MYSQL_DB'] = 'trackkaro'

mysql = MySQL(app)


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


@app.route('/addToTrack', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        details = request.form
        # print(details["budget"])
        name = details["name"]
        link = details["link"]
        image=details['image']
        budget=details["budget"]
        price=details["price"]
        price=price.replace(',','')
        price=price.replace('₹','')
        if budget =='':
            budget='0'
        if int(price)<= int(budget):
            
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
  
            # start TLS for security
            s.starttls()
  
            # Authentication
            s.login("ketankay07@gmail.com", "kanikachawla")
  
            # message to be sent
            message = name+" is available in your budget.\n Buy now from this link: "+link
  
            # sending the mail
            s.sendmail("ketankay07@gmail.com", "gaurav.sharma0865@gmail.com", message)
  
            # terminating the session
            s.quit()
            return redirect('/addToTrack')
                       
        with app.app_context():
            cur = mysql.connection.cursor() 
            st1="SELECT name FROM products;"
            cur.execute(st1)
            ob1=cur.fetchall()
            for i in ob1:
                if(name==i[0]):
                     return redirect('/addToTrack')       
            st="Insert into products Value ('ketanchawla2000@gmail.com','"+link+"','"+name+"','"+image+"','"+budget+"');"
            # print(st)
            cur.execute(st);
            ob=cur.fetchall()
            mysql.connection.commit()
            cur.close()

       

        return redirect('/addToTrack')
    
    if request.method=='GET':

         # USED TO ACCESS DATABASE QUERIES IN SQL.


         with app.app_context():
            cur = mysql.connection.cursor()  # USED TO ACCESS DATABASE QUERIES IN SQL.
            st="SELECT name,image,link,budget FROM products;"
            cur.execute(st)
            ob=cur.fetchall()
            final_price=[]
            for i in ob:
                url_links=[i[2]]
               
                for j in url_links:
                    print(j)
                    URLL = j
                    r = requests.get(URLL)
                    soupp = BeautifulSoup(r.content, 'html.parser')
                    pricelist = soupp.findAll(attrs={'class':"_16Jk6d"})
                    str=pricelist[0].text
                    str=str[1:]
                    final_price.append(str)
            print(final_price)
            mysql.connection.commit()
            cur.close()


         return render_template('track.html', len=len(ob), trackitem=ob, price=final_price)
        

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        details = request.form
        name=details["prod_name"]
        with app.app_context():
            cur = mysql.connection.cursor() 
            st1="DELETE FROM PRODUCTS WHERE name='"+name+"';"
            cur.execute(st1)
            ob=cur.fetchall()
            mysql.connection.commit()
            cur.close()
        return redirect('/addToTrack')

@app.route('/remove_all', methods=['GET', 'POST'])
def remove_all():
    if request.method == 'POST':
        with app.app_context():
            cur = mysql.connection.cursor() 
            st1="DELETE FROM PRODUCTS;"
            cur.execute(st1)
            ob=cur.fetchall()
            mysql.connection.commit()
            cur.close()
        return redirect('/addToTrack')


if __name__ == '__main__':
    app.run(debug=True)
