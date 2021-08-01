# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
#    записывающую собранные вакансии в созданную БД.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
#    больше введённой суммы.
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

from pprint import pprint

from pymongo import MongoClient

import parse_hh

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']

vacancies_hh = db.vacancies_hh


def insert_vacancies(vacancies):
    # Функция добавления вакансий в БД
    vacancies_hh.insert_many(vacancies)


def vacancies_with_salary_gt(salary, salary_currency):
    # Функция поиска и вывода на экран вакансий с заработной платой больше введённой суммы
    vacancies = vacancies_hh.find(
        {'salary_currency': salary_currency,
         '$or': [
             {'salary_min': {'$gt': salary}},
             {'salary_max': {'$gt': salary}}]
         })
    for vacance in vacancies:
        pprint(vacance)


def vacancies_update():
    # Функция добавления в БД новых вакансий с сайта
    vacancies = parse_hh.parcer('python')
    for vacance in vacancies:
        vacancies_hh.update_one(vacance, {'$set': vacance}, upsert=True)


# 1. Добавление вакансий в БД
# insert_vacancies(parse_hh.parcer('python'))

# Очистка БД
# vacancies_hh.delete_many({})

# 2. Вывод на экран вакансий с зарплатой выше задананной
vacancies_with_salary_gt(230000, 'руб.')

# 3. Добавление в БД новых вакансий с сайта
vacancies_update()
