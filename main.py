import requests
import pprint
import numpy
from itertools import count


def search_job(language, url, page=None):
    payload = {'text': f'Программист {language}', 'area': 1, 'period': 30, 'only_with_salary': 'True', 'page': page}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def predict_rub_salary(language, url):
    salary_bracket = get_salaries(language, url)
    job_salaries = []
    for salary in salary_bracket:
        if salary['currency'] != 'RUR':
            None
        elif salary['from'] and salary['to']:
            job_salaries.append(numpy.mean([salary['from'], salary['to']]))
        elif salary['from']:
            job_salaries.append(salary['from'] * 1.2)
        else:
            job_salaries.append(salary['to'] * 0.8)
    return job_salaries


def get_salaries(language, url):
    salary_information = []
    for page in count(0):
        language_statistics = search_job(language, url, page=page)
        for salary in language_statistics['items']:
            salary_information.append(salary['salary'])
        if page >= language_statistics['pages']:
            break
    return salary_information


def average_salaries(programming_languages, url):
    vacancies_jobs = {}
    for language in programming_languages:
        average_salaries = predict_rub_salary(language, url)
        vacancies_jobs[language] = {
            'vacancies_found': search_job(language, url)['found'],
            'vacancies_processed': len(average_salaries),
            'average_salary': int(numpy.mean(average_salaries))
        }
    pprint.pprint(vacancies_jobs)



url = 'https://api.hh.ru/vacancies/'
programming_languages = ['Python', 'Java', 'Javascript', 'Go', 'Scala', 'Ruby', 'C++', 'PHP']
average_salaries(programming_languages, url)

