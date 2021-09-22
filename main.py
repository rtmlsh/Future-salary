import requests
import pprint

url = 'https://api.hh.ru/vacancies/'

def search_job(vacancy, url):
    payload = {'text': f'Программист {vacancy}', 'area': 1, 'period': 30, 'only_with_salary': 'True'}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()['found']

def give_statistics(url):
    vacancies = {'Python', 'Java', 'Javascript', 'Go', 'Scala', 'Ruby', 'C++', 'PHP'}
    vacancies_statistics = {}
    for vacancy in vacancies:
        count_vacancies = search_job(vacancy, url)
        job_title = vacancy
        vacancies_statistics[job_title] = count_vacancies
    pprint.pprint(vacancies_statistics)

give_statistics(url)