import requests
import pprint
import numpy


def search_job(vacancy, url):
    payload = {'text': f'Программист {vacancy}', 'area': 1, 'period': 30, 'only_with_salary': 'True'}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def predict_rub_salary(vacancies):
    job_salaries = []
    for salary in vacancies['items']:
        if salary['salary']['currency'] != 'RUR':
            None
        elif salary['salary']['from'] and salary['salary']['to']:
            job_salaries.append(numpy.mean([salary['salary']['from'], salary['salary']['to']]))
        elif salary['salary']['from']:
            job_salaries.append(salary['salary']['from'] * 1.2)
        else:
            job_salaries.append(salary['salary']['to'] * 0.8)
    return job_salaries


def find_out_vacancies(programming_languages):
    vacancies_jobs = {}
    for language in programming_languages:
        vacancies = search_job(language, url)
        average_salaries = predict_rub_salary(vacancies)
        vacancies_jobs[language] = {
            'vacancies_found': search_job(language, url)['found'],
            'vacancies_processed': len(average_salaries),
            'average_salary': int(numpy.mean(average_salaries))
        }
    pprint.pprint(vacancies_jobs)


url = 'https://api.hh.ru/vacancies/'
programming_languages = ['Python', 'Java', 'Javascript', 'Go', 'Scala', 'Ruby', 'C++', 'PHP']
find_out_vacancies(programming_languages)


