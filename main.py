from fetch_superjob_vacancies import average_salaries
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


def table_data(programming_languages, url, superjob_token):
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
    url = 'https://api.superjob.ru/2.0/vacancies/'
    print(table_data(programming_languages, url, superjob_token))


