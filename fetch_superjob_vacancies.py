import requests
import numpy
import math
import os
from dotenv import load_dotenv
from itertools import count
from terminaltables import AsciiTable


def search_superjob_vacancies(url, superjob_token, language, page=None):
    header = {'X-Api-App-Id': superjob_token}
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


def predict_rub_salary_for_superjob(url, superjob_token, language):
    salaries_bracket = get_salaries_bracket(url, superjob_token, language)
    predictioned_salaries = []
    for salary in salaries_bracket:
        if salary['currency'] != 'rub':
            None
        elif salary['payment_from'] and salary['payment_to'] == 0:
            None
        elif salary['payment_from'] and salary['payment_to']:
            predictioned_salaries.append(numpy.mean([salary['payment_from'], salary['payment_to']]))
        elif salary['payment_from']:
            predictioned_salaries.append(salary['payment_from'] * 1.2)
        else:
            predictioned_salaries.append(salary['payment_to'] * 0.8)
    return predictioned_salaries


def get_salaries_bracket(url, superjob_token, language):
    salaries_bracket = []
    for page in count(0):
        vacations = search_superjob_vacancies(url, superjob_token, language, page=page)
        all_pages = math.ceil(search_superjob_vacancies(url, superjob_token, language)['total'] / 20)
        for vacancy in vacations['objects']:
            salaries_bracket.append(
                {
                 'currency': vacancy['currency'],
                 'payment_from': vacancy['payment_from'],
                 'payment_to': vacancy['payment_to']
                 }
            )
        if page >= all_pages: break
    return salaries_bracket


def average_salaries(programming_languages, url):
    vacancies_jobs = {}
    for language in programming_languages:
        predictioned_salaries = predict_rub_salary_for_superjob(url, superjob_token, language)
        vacancies_jobs[language] = {
            'vacancies_found': search_superjob_vacancies(url, superjob_token, language)['total'],
            'vacancies_processed': len(predictioned_salaries),
            'average_salary': int(numpy.mean(predictioned_salaries))
        }
    return vacancies_jobs


def table_data(programming_languages, url):
    vacancies_jobs = average_salaries(programming_languages, url)
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language, statistics in vacancies_jobs.items():
        table_data.append([language, statistics['vacancies_found'], statistics['vacancies_processed'], statistics['average_salary']])
    table = AsciiTable(table_data)
    table.title = 'Superjob'
    return table.table


load_dotenv()
superjob_token = os.getenv('SUPERJOB_API_KEY')
programming_languages = ['Python', 'Java', 'Javascript', 'Go', 'Scala', 'Ruby', 'C++', 'PHP']
url = 'https://api.superjob.ru/2.0/vacancies/'




