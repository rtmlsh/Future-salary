import argparse
import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

from fetch_hh_vacancies import get_hh_salary_stats
from fetch_sj_vacancies import get_sj_salary_stats


def insert_table(salary_statistics):
    table_stats = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]
    for language, statistics in salary_statistics.items():
        table_stats.append(
            [
                language,
                statistics['vacancies_found'],
                statistics['vacancies_processed'],
                statistics['average_salary']
            ]
        )
    return table_stats


def show_hh_table(programming_languages):
    salary_statistics = get_hh_salary_stats(programming_languages)
    hh_table_stats = insert_table(salary_statistics)
    table = AsciiTable(hh_table_stats)
    table.title = 'Head Hunter'
    print(table.table)


def show_sj_table(programming_languages, sj_token):
    salary_statistics = get_sj_salary_stats(programming_languages, sj_token)
    sj_table_stats = insert_table(salary_statistics)
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
