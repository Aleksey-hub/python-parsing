# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для
# конкретного пользователя, сохранить JSON-вывод в файле *.json.

import json
from pprint import pprint

import requests

username = 'Aleksey-hub'
url = f'https://api.github.com/users/{username}/repos'
params = {'accept': 'application/vnd.github.v3+json'}

response = requests.get(url, params=params)
# pprint(response.json())

with open('task_1.json', 'w') as f:
    f.write(response.text)

with open('task_1.json', 'r') as f:
    a = json.load(f)
    pprint(a)