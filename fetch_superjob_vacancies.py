import math
from itertools import count

import numpy
import requests


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
    salaries_bracket = get_salaries_bracket(language, url, sj_token)
    predictioned_salaries = []
    for salary in salaries_bracket:
        if salary['currency'] != 'rub':
            None
        elif salary['payment_from'] and salary['payment_to'] == 0:
            None
        elif salary['payment_from'] and salary['payment_to']:
            predictioned_salaries.append(numpy.mean(
                [salary['payment_from'], salary['payment_to']]
            ))
        elif salary['payment_from']:
            predictioned_salaries.append(salary['payment_from'] * 1.2)
        else:
            predictioned_salaries.append(salary['payment_to'] * 0.8)
    return predictioned_salaries


def get_salaries_bracket(language, url, sj_token):
    salaries_bracket = []
    page_result = 20
    for page in count(0):
        vacations = search_sj_vacancies(language, url, sj_token, page=page)
        all_pages = math.ceil(search_sj_vacancies(
            language, url, sj_token)['total'] / page_result
                              )
        for vacancy in vacations['objects']:
            salaries_bracket.append(
                {
                 'currency': vacancy['currency'],
                 'payment_from': vacancy['payment_from'],
                 'payment_to': vacancy['payment_to']
                 }
            )
        if page >= all_pages:
            break
    return salaries_bracket


def average_sj_salaries(programming_languages, url, sj_token):
    vacancies_jobs = {}
    for language in programming_languages:
        predictioned_salaries = predict_rub_salary_for_sj \
            (language, url, sj_token)
        vacancies_jobs[language] = {
            'vacancies_found': search_sj_vacancies(language, url, sj_token)
            ['total'],
            'vacancies_processed': len(predictioned_salaries),
            'average_salary': int(numpy.mean(predictioned_salaries))
        }
    return vacancies_jobs
