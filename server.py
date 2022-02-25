from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from product import Product


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
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
        soup = BeautifulSoup(r.content, 'html5lib')

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
