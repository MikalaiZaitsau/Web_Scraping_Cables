import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml as lxml


# Define URL
url_long = 'https://k-ps.ru/spravochnik/kabeli-silovyie/'
url = url_long[:16]

# Ask hosting server to fetch url
r = requests.get(url_long)
# print(r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

# Ссылки уровня 1
links_level_1 = {}
link_1 = 0
for link in soup.find_all('h3'):
    link_1 += 1
    links_level_1[link_1] = url+link.a['href']

# Ссылки уровня 2
r2 = requests.get(links_level_1[1])
soup2 = BeautifulSoup(r2.text, "html.parser")
links_level_2 = {}
link_2 = 0
for link in soup2.find_all('h3'):
    link_2 += 1
    links_level_2[link_2] = url+link.a['href']

# Ссылки уровня 3
r3 = requests.get(links_level_2[3])
soup3 = BeautifulSoup(r3.text, "html.parser")
links_level_3 = {}
link_3 = 0
list_markTable = soup3.find(class_='markTable_on_mr')
for link in list_markTable.find_all('a'):
    link_3 += 1
    links_level_3[link_3] = url+link['href']

# Ссылки уровня 4
r4 = requests.get(links_level_3[1])
soup4 = BeautifulSoup(r4.text, "html.parser")


'''
Присваивание параметров для каждой марки кабеля
и создание DataFrame c требуемыми параметрами
'''

#category
category = soup4.h1.text.split(' ')[0]

#name_short
name_short = soup4.h1.text.split(' ')[1]

#voltage_kV
voltage_block = soup4.find(class_='top-mobile')
item_voltage = voltage_block.find_all('td')
voltage_kV = item_voltage[1].string.split()[0]

#nominal_section_mm2
nominal_section_mm2 = soup4.h1.text.split(' ')[2]

#weight_one_km_kg
weight_block = soup4.find(class_='col-md-7 col-xs-12 pl0 pad_mob')
weight_all = weight_block.find_all('p')
weight_one_km_kg = float(weight_all[0].span.text.split()[0].replace(',', '.'))

#diameter_mm	
diameter_block = soup4.find(class_='col-md-7 pl0 pad_mob')
diameter_all = diameter_block.find_all('p')
diameter_mm = float(diameter_all[0].span.text.split()[0].replace(',', '.'))
print(diameter_mm)









'''
id				                # 1
category			            # Кабель силовой
name_short			            # ВВГнг-FRLS - 0,66/1кВ
voltage_kV			            # 0,66/1
nominal_section_mm2		        # 3х50
weight_one_km_kg		        # 2533
diameter_mm			            # 35,9
current_air_A			        # 209
current_ground_A		        # 205
inductive_impedance_ohm_per_km	# 0,0625
insulation resistance_Mohm	    # 7
insulation_thickness_mm		    # 1,4
Construction length_m		    # 300
'''