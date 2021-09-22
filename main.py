import requests
import pprint
import numpy

url = 'https://api.hh.ru/vacancies/'
vacancy = 'Python'

def search_job(vacancy, url):
    payload = {'text': f'Программист {vacancy}', 'area': 1, 'period': 30, 'only_with_salary': 'True'}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def give_statistics(url):
    vacancies = {'Python', 'Java', 'Javascript', 'Go', 'Scala', 'Ruby', 'C++', 'PHP'}
    vacancies_statistics = {}
    for vacancy in vacancies:
        count_vacancies = search_job(vacancy, url)['found']
        job_title = vacancy
        vacancies_statistics[job_title] = count_vacancies
    pprint.pprint(vacancies_statistics)


def find_out_salary(url, vacancy):
    job_vacation = search_job(vacancy, url)
    for job in job_vacation['items']:
        if job['salary']['currency'] != 'RUR':
            print(None)
        elif job['salary']['from'] and job['salary']['to']:
            print(numpy.mean([job['salary']['from'], job['salary']['to']]))
        elif job['salary']['from']:
            print(job['salary']['from'] * 1.2)
        else:
            print(job['salary']['to'] * 0.8)




find_out_salary(url, vacancy)
# give_statistics(url)