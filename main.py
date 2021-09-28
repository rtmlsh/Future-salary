import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

from fetch_hh_vacancies import average_hh_salaries
from fetch_superjob_vacancies import average_sj_salaries


def show_hh_table(programming_languages, url):
    salary_statistics = average_hh_salaries(programming_languages, url)
    hh_table_stats = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]
    for language, statistics in salary_statistics.items():
        hh_table_stats.append(
            [
                language, statistics['vacancies_found'],
                statistics['vacancies_processed'],
                statistics['average_salary']
            ]
        )
    table = AsciiTable(hh_table_stats)
    table.title = 'Head Hunter'
    print(table.table)


def show_sj_table(programming_languages, url, sj_token):
    salary_statistics = average_sj_salaries(programming_languages, url, sj_token)
    sj_table_stats = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]
    for language, statistics in salary_statistics.items():
        sj_table_stats.append(
            [
                language,
                statistics['vacancies_found'],
                statistics['vacancies_processed'],
                statistics['average_salary']
            ]
        )
    table = AsciiTable(sj_table_stats)
    table.title = 'Superjob'
    print(table.table)


if __name__ == '__main__':
    load_dotenv()
    sj_token = os.getenv('SUPERJOB_API_KEY')

    programming_languages = [
        'Python',
        'Java',
        'Javascript',
        'Go',
        'Scala',
        'Ruby',
        'C++',
        'PHP'
    ]

    sj_api_url = 'https://api.superjob.ru/2.0/vacancies/'
    hh_api_url = 'https://api.hh.ru/vacancies/'

    show_sj_table(programming_languages, sj_api_url, sj_token)
    show_hh_table(programming_languages, hh_api_url)
