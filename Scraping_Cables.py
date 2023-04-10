import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml as lxml


# Задаем URL сайта
url_long = 'https://k-ps.ru/spravochnik/kabeli-silovyie/'
url = url_long[:16]

# Запрос статуса ответа с сервера
r = requests.get(url_long)
# print(r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

# Ссылки уровня 1 (словарь ссылок links_level_1)
links_level_1 = {}
link_1 = 0
for link in soup.find_all('h3'):
    link_1 += 1
    links_level_1[link_1] = url+link.a['href']

# Ссылки уровня 2 (словарь ссылок links_level_2)
r2 = requests.get(links_level_1[1])
soup2 = BeautifulSoup(r2.text, "html.parser")
links_level_2 = {}
link_2 = 0
for link in soup2.find_all('h3'):
    link_2 += 1
    links_level_2[link_2] = url+link.a['href']

#Словарь марок кабелей для DataFrame
cable_list = []

#Цикл присваивания параметром по семействам марок кабелей
for link3 in links_level_2.values():
    #Цикл присваивания параметром по маркам кабеля из dict (для одной марки)

    # Ссылки уровня 3 (словарь ссылок links_level_3)
    r3 = requests.get(link3)
    soup3 = BeautifulSoup(r3.text, "html.parser")
    
    # обработка ссылок с отличной от заданной структурой
    try:
        list_markTable = soup3.find(class_='markTable_on_mr')
        for link in list_markTable.find_all('a'):
            link4 = url+link['href']

            # обработка ссылок с отличной от заданной структурой
            try:
                r4 = requests.get(link4)
                soup4 = BeautifulSoup(r4.text, "html.parser")

                '''
                #Присваивание параметров 
                #для каждой марки кабеля
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

                #construction_length_m
                options_block = soup4.find(class_='col-xs-12 col-md-7 pl0 mt10 obshie-table-blue pad_mob')
                option_block_items = options_block.find_all(class_='col-md-4 col-xs-4 pad0 tar')
                if len(option_block_items[1].text.split()[0]) < 4:
                    construction_length_m = int(option_block_items[1].text.split()[0])
                else:
                    construction_length_m = 'N/A'

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

                #Список словарей(строк) кабелей
                cable_list.append(cable_dict_item)
            except:
                # сcылки, в которых нет информации или не соответствует требуемой структуре
                with open('log_errors.txt', 'r+') as f:
                    f.seek(0, 2)    # перемещение курсора в конец файла
                    f.write('\n'+link)
                f.close()
                continue
    except:
        continue


# экспорт в .xlsx 
cable_table = pd.DataFrame(cable_list)
cable_table.to_excel('cables.xlsx', sheet_name='Cables')