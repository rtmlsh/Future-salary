import math
from itertools import count

import numpy
import requests

from count_average_salaries import predict_salary_sj


def search_sj_vacancies(language, url, sj_token, page=None):
    header = {'X-Api-App-Id': sj_token}
    payload = {
        'catalogues': 33,
        'period': 30,
        'keyword': f'Программист {language}',
        'town': 4,
        'page': page
    }
    response = requests.get(url, headers=header, params=payload)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_for_sj(language, url, sj_token):
    salaries = get_salaries(language, url, sj_token)
    predictioned_salaries = []
    for salary in salaries:
        currency = salary['currency']
        payment_from = salary['payment_from']
        payment_to = salary['payment_to']
        predict_salary_sj(currency, payment_from, payment_to, predictioned_salaries)
    return predictioned_salaries


def get_salaries(language, url, sj_token):
    salaries = []
    page_result = 20
    for page in count(0):
        vacancies = search_sj_vacancies(language, url, sj_token, page=page)
        all_pages = math.ceil(search_sj_vacancies(
            language,
            url,
            sj_token
        )['total'] / page_result)
        for vacancy in vacancies['objects']:
            salaries.append(
                {
                 'currency': vacancy['currency'],
                 'payment_from': vacancy['payment_from'],
                 'payment_to': vacancy['payment_to']
                 }
            )
        if page >= all_pages:
            break
    return salaries


def average_sj_salaries(programming_languages, url, sj_token):
    salary_statistics = {}
    for language in programming_languages:
        predictioned_salaries = predict_rub_salary_for_sj(
            language,
            url,
            sj_token
        )
        salary_statistics[language] = {
            'vacancies_found': search_sj_vacancies(language, url, sj_token)
            ['total'],
            'vacancies_processed': len(predictioned_salaries),
            'average_salary': int(numpy.mean(predictioned_salaries))
        }
    return salary_statistics
