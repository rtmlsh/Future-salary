from itertools import count

import numpy
import requests

from count_average_salaries import predict_salary


def search_vacancies(language, page=None, city_num=1, publish_period=30):
    url = 'https://api.hh.ru/vacancies/'
    payload = {
        'text': f'Программист {language}',
        'area': city_num,
        'period': publish_period,
        'only_with_salary': 'True',
        'page': page
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_salaries(language):
    salaries = []
    for page in count(0):
        vacancies_page = search_vacancies(language, page=page)
        for salary in vacancies_page['items']:
            salaries.append(salary['salary'])
        if page >= vacancies_page['pages']:
            break
    return salaries, vacancies_page['found']


def predict_rub_salaries(language):
    salaries, vacancies_found = get_salaries(language)
    predicted_salaries = []
    for salary in salaries:
        if salary['currency'] == 'RUR':
            payment_from = salary['from']
            payment_to = salary['to']
            average_salary = predict_salary(payment_from, payment_to)
            if average_salary:
                predicted_salaries.append(average_salary)
    return predicted_salaries, vacancies_found


def get_hh_salary_stats(programming_languages):
    salary_statistics = {}
    for language in programming_languages:
        predicted_salaries, vacancies_found = \
            predict_rub_salaries(language)
        salary_statistics[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(predicted_salaries),
            'average_salary': int(numpy.mean(predicted_salaries))
        }
    return salary_statistics
