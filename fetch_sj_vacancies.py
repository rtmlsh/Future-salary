from itertools import count

import numpy
import requests

from count_average_salaries import predict_salary


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
    salaries, vacancies_found = get_salaries(language, url, sj_token)
    predicted_salaries = []
    for salary in salaries:
        if salary['currency'] == 'rub':
            payment_from = salary['payment_from']
            payment_to = salary['payment_to']
            predict_salary(payment_from, payment_to, predicted_salaries)
    return predicted_salaries, vacancies_found


def get_salaries(language, url, sj_token):
    salaries = []
    for page in count(0):
        vacancies = search_sj_vacancies(language, url, sj_token, page=page)
        if vacancies['more']:
            get_salary_range(vacancies, salaries)
        else:
            get_salary_range(vacancies, salaries)
            break
    return salaries, vacancies['total']


def get_salary_range(vacancies, salaries):
    for vacancy in vacancies['objects']:
        salaries.append(
            {
                'currency': vacancy['currency'],
                'payment_from': vacancy['payment_from'],
                'payment_to': vacancy['payment_to']
            }
        )
    return salaries


def get_sj_salary_stats(programming_languages, url, sj_token):
    salary_statistics = {}
    for language in programming_languages:
        predicted_salaries, vacancies_found = predict_rub_salary_for_sj(
            language,
            url,
            sj_token
        )
        salary_statistics[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(predicted_salaries),
            'average_salary': int(numpy.mean(predicted_salaries))
        }
    return salary_statistics
