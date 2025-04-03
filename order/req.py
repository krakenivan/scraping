import requests

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
}  # заголовки что бы показать что не бот
url = (
    "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
)

req = requests.get(url, headers=headers)
src = req.text
print(src)  # убеждаемся в получении кода страницы

with open ('index.html', 'w') as file:  # сохранение страницы
    file.write(src)
