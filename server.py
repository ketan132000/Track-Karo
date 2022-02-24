from click import style
from flask import render_template,Flask
import requests
from bs4 import BeautifulSoup
import os

prod_classes=[["div","_4rR01T"],["a","s1Q9rs"],["a","IRpwTa"]]


strings="iphone"
URL = "https://www.flipkart.com/search?q="+strings
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib') 

prod=[]
for c in prod_classes:
    flag=True
    productList = soup.findAll(c[0] , attrs = {'class': c[1]})
    
    if len(productList)!=0:
        print(c,"\n")
        for i in productList:
            print(i.text) 
            prod.append(str(i.text))
        print(prod)

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
@app.route('/')
def home():
  return render_template('index.html', len=1,products=prod) 


if __name__ == '__main__':
    app.run()
