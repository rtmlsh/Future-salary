import requests
import numpy
from itertools import count
from terminaltables import AsciiTable


def search_vacations(language, url, page=None):
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
        if salary['currency'] != 'RUR':
            None
        elif salary['from'] and salary['to']:
            predictioned_salaries.append(numpy.mean([salary['from'], salary['to']]))
        elif salary['from']:
            predictioned_salaries.append(salary['from'] * 1.2)
        else:
            predictioned_salaries.append(salary['to'] * 0.8)
    return predictioned_salaries


def get_salaries_bracket(language, url):
    salaries_bracket = []
    for page in count(0):
        vacations = search_vacations(language, url, page=page)
        for salary in vacations['items']:
            salaries_bracket.append(salary['salary'])
        if page >= vacations['pages']: break
    return salaries_bracket


def average_salaries(programming_languages, url):
    vacancies_jobs = {}
    for language in programming_languages:
        predictioned_salaries = predict_rub_salary(language, url)
        vacancies_jobs[language] = {
            'vacancies_found': search_vacations(language, url)['found'],
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
    table.title = 'Head Hunter'
    return table.table


url = 'https://api.hh.ru/vacancies/'
programming_languages = ['Python', 'Java', 'Javascript', 'Go', 'Scala', 'Ruby', 'C++', 'PHP']
print(table_data(programming_languages, url))