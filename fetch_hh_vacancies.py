from itertools import count

import numpy
import requests

from count_average_salaries import predict_salary_hh


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
    salaries = get_salaries(language, url)
    predictioned_salaries = []
    for salary in salaries:
        currency = salary['currency']
        payment_from = salary['from']
        payment_to = salary['to']
        predict_salary_hh(currency, payment_from, payment_to, predictioned_salaries)
    return predictioned_salaries


def get_salaries(language, url):
    salaries = []
    for page in count(0):
        vacancies = search_vacancies(language, url, page=page)
        for salary in vacancies['items']:
            salaries.append(salary['salary'])
        if page >= vacancies['pages']:
            break
    return salaries


def average_hh_salaries(programming_languages, url):
    salary_statistics = {}
    for language in programming_languages:
        predictioned_salaries = predict_rub_salary(language, url)
        salary_statistics[language] = {
            'vacancies_found': search_vacancies(language, url)['found'],
            'vacancies_processed': len(predictioned_salaries),
            'average_salary': int(numpy.mean(predictioned_salaries))
        }
    return salary_statistics
