from terminaltables import AsciiTable
from fetch_superjob_vacancies import average_salaries
from fetch_hh_vacancies import average_salaries


def table_data(programming_languages, url):
    vacancies_jobs = average_salaries(programming_languages, url)
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language, statistics in vacancies_jobs.items():
        table_data.append([language, statistics['vacancies_found'], statistics['vacancies_processed'], statistics['average_salary']])
    table = AsciiTable(table_data)
    table.title = 'Superjob'
    return table.table


if __name__ == '__main__':
    programming_languages = ['Python', 'Java', 'Javascript', 'Go', 'Scala', 'Ruby', 'C++', 'PHP']
    superjob_api_url = 'https://api.superjob.ru/2.0/vacancies/'
    hh_api_url = 'https://api.hh.ru/vacancies/'
    print(table_data(programming_languages, superjob_api_url))
    # print(table_data(programming_languages, hh_api_url))