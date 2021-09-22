import requests
import pprint

url = 'https://api.hh.ru/vacancies/'
vacancies = {'Python', 'Java', 'Javascript', 'Go', 'Scala', 'Ruby', 'C++', 'PHP'}
vacancies_statistics = {}

def search_job(vacancy):
    payload = {'text': f'Программист {vacancy}', 'area': 1, 'period': 30, 'only_with_salary': 'True'}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()['found']


for vacancy in vacancies:
    count_vacancies = search_job(vacancy)
    job_title = vacancy
    vacancies_statistics[job_title] = count_vacancies


pprint.pprint(vacancies_statistics)

