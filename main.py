import requests
import pprint

url = 'https://api.hh.ru/vacancies/'
payload = {'text': 'Программист', 'area': 1, 'period': 20}
response = requests.get(url, params=payload)
response.raise_for_status()
pprint.pprint(response.json())