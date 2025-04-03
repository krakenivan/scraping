import random
from time import sleep
from bs4 import BeautifulSoup
import json
import requests
import csv

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
}  # заголовки
url = (
    "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
)

with open("./all_categories_dict.json") as file:
    all_categories = json.load(file)  # словарь со ссылками

iteration_count = len(all_categories) - 1 # количество страниц в категории
print(f"Всего итераций: {iteration_count}")

count = 0
for category_name, category_href in all_categories.items():
    rep = [",", " ", "-", "'"]
    for item in rep:  # заменяем символы в названии
        if item in category_name:
            category_name = category_name.replace(item, "_")
    req = requests.get(url=category_href, headers=headers)  # запрос по ссылкам
    src = req.text

    with open(f"data/{count}_{category_name}.html", "w") as file:
        # сохраняем каждую страницу в отдельный файл
        file.write(src)

    with open(f"data/{count}_{category_name}.html") as file:
        # открываем сохраненную страницу
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    alert_block = soup.find(class_="uk-alert-danger")
    # блок ошибки
    if alert_block is not None:
        continue

    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    # класс таблицы
    product = table_head[0].text  # получаем заголовки таблицы
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (product, calories, proteins, fats, carbohydrates)
        )  # записываем заголовки в файл csv

    product_data = soup.find(class_="mzr-tc-group-table").find('tbody').find_all('tr')
    # данные продуктов
    product_info = []

    for item in product_data:
        product_tds = item.find_all('td')

        title = product_tds[0].find('a').text  # название
        calories = product_tds[1].text  # калории
        proteins = product_tds[2].text  # белки
        fats = product_tds[3].text  # жиры
        carbohydrates = product_tds[4].text  # углеводы

        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                'Carbohydrates': carbohydrates
            }
        )

        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
            # дописываем данные в файл csv
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
        # запись в json

    count += 1
    print(f"# Итерация {count}. {category_name} записан ... ")
    iteration_count -= 1
    if iteration_count == 0:
        print("Работа завершена")
        break
    print(f"Осталось итераций: {iteration_count}")
    sleep(random.randrange(2, 4))
