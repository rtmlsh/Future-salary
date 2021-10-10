from itertools import count

import numpy
import requests

from count_average_salaries import predict_salary


def search_vacancies(language, url, page=None):
    payload = {
        'text': f'Программист {language}',
        'area': 1,
        'period': 30,
        'only_with_salary': 'True',
        'page': page
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def predict_rub_salary(language, url):
    salaries, vacancies_found = get_salaries(language, url)
    predicted_salaries = []
    for salary in salaries:
        if salary['currency'] == 'RUR':
            payment_from = salary['from']
            payment_to = salary['to']
            predict_salary(payment_from, payment_to, predicted_salaries)
    return predicted_salaries, vacancies_found


def get_salaries(language, url):
    salaries = []
    for page in count(0):
        vacancies = search_vacancies(language, url, page=page)
        for salary in vacancies['items']:
            salaries.append(salary['salary'])
        if page >= vacancies['pages']:
            break
    return salaries, vacancies['found']


def get_hh_salary_stats(programming_languages, url):
    salary_statistics = {}
    for language in programming_languages:
        predicted_salaries, vacancies_found = \
            predict_rub_salary(language, url)
        salary_statistics[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(predicted_salaries),
            'average_salary': int(numpy.mean(predicted_salaries))
        }
    return salary_statistics
