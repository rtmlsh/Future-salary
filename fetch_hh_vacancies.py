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


def predict_rub_salary(language):
    salaries = []
    for page in count(0):
        vacancies_page = search_vacancies(language, page=page)
        for salary in vacancies_page['items']:
            if salary['salary']['currency'] == 'RUR':
                payment_from = salary['salary']['from']
                payment_to = salary['salary']['to']
                average_salary = predict_salary(payment_from, payment_to)
                if average_salary:
                    salaries.append(average_salary)
        if page >= vacancies_page['pages']:
            break
    return salaries, vacancies_page['found']


def get_hh_salary_stats(programming_languages):
    salary_statistics = {}
    for language in programming_languages:
        predicted_salaries, vacancies_found = \
            predict_rub_salary(language)
        salary_statistics[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(predicted_salaries),
            'average_salary': int(numpy.mean(predicted_salaries))
        }
    return salary_statistics
