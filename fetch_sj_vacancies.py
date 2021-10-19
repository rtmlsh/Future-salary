from itertools import count

import numpy
import requests

from count_average_salaries import predict_salary


def search_sj_vacancies(language, sj_token, page=None,
                        job_area=33, publish_period=30, city_num=4):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    header = {'X-Api-App-Id': sj_token}
    payload = {
        'catalogues': job_area,
        'period': publish_period,
        'keyword': f'Программист {language}',
        'town': city_num,
        'page': page
    }
    response = requests.get(url, headers=header, params=payload)
    response.raise_for_status()
    return response.json()


def get_salaries(language, sj_token):
    salaries = []
    for page in count(0):
        vacancies_page = search_sj_vacancies(language, sj_token, page=page)
        salaries.extend(predict_sj_rub_salary(vacancies_page))
        if not vacancies_page['more']:
            break
    return salaries, vacancies_page['total']


def predict_sj_rub_salary(vacancies):
    salary_range = []
    for vacancy in vacancies['objects']:
        if vacancy['currency'] == 'rub':
            payment_from = vacancy['payment_from']
            payment_to = vacancy['payment_to']
            average_salary = predict_salary(payment_from, payment_to)
            if average_salary:
                salary_range.append(average_salary)
    return salary_range


def get_sj_salary_stats(programming_languages, sj_token):
    salary_statistics = {}
    for language in programming_languages:
        predicted_salaries, vacancies_found = get_salaries(
            language,
            sj_token
        )
        salary_statistics[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(predicted_salaries),
            'average_salary': int(numpy.mean(predicted_salaries))
        }
    return salary_statistics
