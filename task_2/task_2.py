# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# Праздничные дни по дате
from pprint import pprint

import requests

url = 'https://holidays.abstractapi.com/v1/'
params = {
    'api_key': 'dfad1848c4584e1d85d7bf5709431ff9',
    'country': 'RU',
    'year': '2021',
    'month': '01',
    'day': '01'
}

response = requests.get(url, params=params)
pprint(response.json())

with open('task_2.json', 'w') as f:
    f.write(response.text)
