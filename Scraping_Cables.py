import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml as lxml



# Define URL
url = 'https://k-ps.ru/spravochnik/kabeli-silovyie/'

# Ask hosting server to fetch url
r = requests.get(url)
# print(r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

for link in soup.find_all('h3'):
    print(link.a['href'])






'''
soup = BeautifulSoup('<h3><a href="spravochnik/pozharobezopasnyie-kabeli/s-pvx-izolyacziej-(0,66-1kv)/vvgng-frls/">ВВГнг-FRLS - 0,66/1кВ</a></h3>', 'lxml')
tag = soup.h3.string
print(tag)
'''



