from math import prod
import requests
from bs4 import BeautifulSoup



URL = "https://www.flipkart.com/osiris-100-pcs-pack-mask-certified-ce-iso-who-gmp-fda-breathable-pollution-premium-black-disposable-water-resistant-surgical-melt-blown-fabric-layer/p/itm5945993f4ea0a?pid=MRPGC93KZHBHJ5ZM&lid=LSTMRPGC93KZHBHJ5ZM0PVMPE&marketplace=FLIPKART&q=mask&store=hlc&srno=s_1_3&otracker=search&fm=organic&iid=55141f6e-b61c-49de-9edf-87f0da08316c.MRPGC93KZHBHJ5ZM.SEARCH&ppt=None&ppn=None&ssid=d64je6kkrk0000001652187726795&qH=f2ce11ebf1109936"

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')
# print(soup)
productList = soup.findAll(attrs={'class':"_16Jk6d"})
print(productList[0].text)

str=productList[0].text

str=str[1:]
print(str)
price=int (str)
print(type(price))