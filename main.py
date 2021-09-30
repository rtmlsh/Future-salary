import argparse
import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

from fetch_hh_vacancies import average_hh_salaries
from fetch_sj_vacancies import average_sj_salaries


def show_hh_table(programming_languages):
    hh_api_url = 'https://api.hh.ru/vacancies/'
    salary_statistics = average_hh_salaries(programming_languages, hh_api_url)
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
                language,
                statistics['vacancies_found'],
                statistics['vacancies_processed'],
                statistics['average_salary']
            ]
        )
    table = AsciiTable(hh_table_stats)
    table.title = 'Head Hunter'
    print(table.table)


def show_sj_table(programming_languages, sj_token):
    sj_api_url = 'https://api.superjob.ru/2.0/vacancies/'
    salary_statistics = average_sj_salaries(programming_languages, sj_api_url, sj_token)
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
    parser = argparse.ArgumentParser(
        description='Скрипт интегрируется с API Head Hunter, Superjob, '
                    'и показывает статистику зарплат по вакансиям программистов'
    )
    parser.parse_args()

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

    show_sj_table(programming_languages, sj_token)
    show_hh_table(programming_languages)
