from fetch_superjob_vacancies import average_sj_salaries
from fetch_hh_vacancies import average_hh_salaries
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_hh_table(programming_languages, url):
    vacancies_jobs = average_hh_salaries(programming_languages, url)
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language, statistics in vacancies_jobs.items():
        table_data.append([language, statistics['vacancies_found'], statistics['vacancies_processed'], statistics['average_salary']])
    table = AsciiTable(table_data)
    table.title = 'Head Hunter'
    print(table.table)


def get_sj_table(programming_languages, url, sj_token):
    vacancies_jobs = average_sj_salaries(programming_languages, url, sj_token)
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language, statistics in vacancies_jobs.items():
        table_data.append([language, statistics['vacancies_found'], statistics['vacancies_processed'], statistics['average_salary']])
    table = AsciiTable(table_data)
    table.title = 'Superjob'
    print(table.table)


if __name__ == '__main__':
    load_dotenv()
    sj_token = os.getenv('SUPERJOB_API_KEY')

    programming_languages = ['Python', 'Java', 'Javascript', 'Go', 'Scala', 'Ruby', 'C++', 'PHP']

    sj_api_url = 'https://api.superjob.ru/2.0/vacancies/'
    hh_api_url = 'https://api.hh.ru/vacancies/'

    get_sj_table(programming_languages, sj_api_url, sj_token)
    get_hh_table(programming_languages, hh_api_url)

