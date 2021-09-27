from fetch_superjob_vacancies import average_salaries
from fetch_hh_vacancies import average_salaries
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_hh_table(programming_languages, url):
    vacancies_jobs = average_salaries(programming_languages, url)
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language, statistics in vacancies_jobs.items():
        table_data.append([language, statistics['vacancies_found'], statistics['vacancies_processed'], statistics['average_salary']])
    table = AsciiTable(table_data)
    table.title = 'Head Hunter'
    return table.table


def get_superjob_table(programming_languages, url, superjob_token):
    vacancies_jobs = average_salaries(programming_languages, url, superjob_token)
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language, statistics in vacancies_jobs.items():
        table_data.append([language, statistics['vacancies_found'], statistics['vacancies_processed'], statistics['average_salary']])
    table = AsciiTable(table_data)
    table.title = 'Superjob'
    return table.table


if __name__ == '__main__':
    load_dotenv()
    superjob_token = os.getenv('SUPERJOB_API_KEY')
    programming_languages = ['Python', 'Java', 'Javascript', 'Go', 'Scala', 'Ruby', 'C++', 'PHP']
    programming_languages_hh = ['Python', 'Java']
    url = 'https://api.superjob.ru/2.0/vacancies/'
    hh_api_url = 'https://api.hh.ru/vacancies/'


    # print(get_hh_table(programming_languages_hh, hh_api_url))
    print(get_superjob_table(programming_languages, url, superjob_token))


