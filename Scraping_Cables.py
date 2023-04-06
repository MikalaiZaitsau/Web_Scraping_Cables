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
Присваивание параметров 
для каждой марки кабеля

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

#current_air_A
current_block = soup4.find(class_='col-xs-12 col-md-6 pl0 pad_mob elect-table-green')
item_current = current_block.find_all(class_='col-xs-5 pad0 tar')
current_air_A = float(item_current[0].text.split()[0])

#current_ground_A
current_block = soup4.find(class_='col-xs-12 col-md-6 pl0 pad_mob elect-table-green')
item_current = current_block.find_all(class_='col-xs-5 pad0 tar')
current_ground_A = float(item_current[1].text.split()[0])

#min_radius_mm
options_block = soup4.find(class_='col-xs-12 col-md-7 pl0 mt10 obshie-table-blue pad_mob')
option_block_items = options_block.find_all(class_='col-md-4 col-xs-4 pad0 tar')
min_radius_mm = float(option_block_items[0].text.split()[0].replace(',', '.'))
print(min_radius_mm)

#construction_length_m
options_block = soup4.find(class_='col-xs-12 col-md-7 pl0 mt10 obshie-table-blue pad_mob')
option_block_items = options_block.find_all(class_='col-md-4 col-xs-4 pad0 tar')
construction_length_m = int(option_block_items[1].text.split()[0])
print(construction_length_m)


#Создание DataFrame c параметрами кабелей
cable_dict_item = {'category': category,
                   'name_short': name_short,
                   'voltage_kV': voltage_kV,
                   'nominal_section_mm2': nominal_section_mm2,
                   'weight_one_km_kg': weight_one_km_kg,
                   'diameter_mm': diameter_mm,
                   'current_air_A': current_air_A,
                   'current_ground_A': current_ground_A,
                   'min_radius_mm': min_radius_mm,
                   'construction_length_m': construction_length_m}

table_row = pd.DataFrame(cable_dict_item, index=[0])
table_row.to_excel('cables.xlsx', sheet_name='Cables')
print(table_row)