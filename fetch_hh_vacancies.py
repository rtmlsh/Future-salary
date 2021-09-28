from itertools import count

import numpy
import requests


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
    salaries_bracket = get_salaries_bracket(language, url)
    predictioned_salaries = []
    for salary in salaries_bracket:
        if salary:
            if salary['currency'] == 'RUR':
                if salary['from'] and salary['to']:
                    predictioned_salaries.append(numpy.mean(
                        [salary['from'], salary['to']]
                    ))
                elif salary['from']:
                    predictioned_salaries.append(salary['from'] * 1.2)
                else:
                    predictioned_salaries.append(salary['to'] * 0.8)
            else:
                None
    return predictioned_salaries


def get_salaries_bracket(language, url):
    salaries_bracket = []
    for page in count(0):
        vacations = search_vacancies(language, url, page=page)
        for salary_bracket in vacations['items']:
            salaries_bracket.append(salary_bracket['salary'])
        if page >= vacations['pages']:
            break
    return salaries_bracket


def average_hh_salaries(programming_languages, url):
    vacancies_jobs = {}
    for language in programming_languages:
        predictioned_salaries = predict_rub_salary(language, url)
        vacancies_jobs[language] = {
            'vacancies_found': search_vacancies(language, url)['found'],
            'vacancies_processed': len(predictioned_salaries),
            'average_salary': int(numpy.mean(predictioned_salaries))
        }
    return vacancies_jobs
