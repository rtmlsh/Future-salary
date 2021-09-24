import requests
import pprint

superjob_api = 'v3.r.124446881.cc370bafaaee6098c089f335a7902bc241c1bc02.28bcb2cd6a9e7b9d79fd7930896a81a00d847dd6'
url = 'https://api.superjob.ru/2.0/vacancies/'

payload = {'X-Api-App-Id': superjob_api}
response = requests.get(url, headers=payload)
response.raise_for_status()
print(response.url)
for profession in response.json()['objects']:
    print(profession['profession'])