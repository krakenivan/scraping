from bs4 import BeautifulSoup
import json

with open('index.html') as file:  # открываем страницу
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
all_product_href = soup.find_all(class_="mzr-tc-group-item-href")  # ссылки

all_categories_dict = {}

for item in all_product_href:
    item_text = item.text  # текст ссылки
    item_href = 'https://health-diet.ru'+item.get('href')  # доменно имя + ссылка 
    all_categories_dict[item_text] = item_href

with open ('all_categories_dict.json', 'w') as file:  # сохранение в json
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

