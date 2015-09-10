#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-

import csv
import urllib2

from bs4 import BeautifulSoup


BASE_URL = 'https://www.avito.ru/sankt-peterburg/rabota'
# BASE_URL = 'https://www.avito.ru/sankt-peterburg/rabota?p='


def get_html(url):
    response = urllib2.urlopen(url)
    return response.read()


def get_page_count(html):
    # 'html.parser' для совместмости с debian 8. без этого на debian не работает. на ubuntu нормально.
    soup = BeautifulSoup(html, 'html.parser')
    paggination = soup.find('div', class_='pagination__pages clearfix')
    # основаная строка для парсинга количества страниц
    return int(paggination.find_all('a', href=True)[-1]['href'][-3:])


# def parse(html):
#     soup = BeautifulSoup(html)
#     table = soup.find('table', class_='items_list')
#     rows = table.find_all('tr')[1:]

#     projects = []
#     for row in rows:

#         cols = row.find_all('td')

#         projects.append({
#             'title': cols[0].a.text,
#             'categories': [category.text for category in cols[0].find_all('noindex')],
#             'price': cols[1].text.strip().split()[0],
#             'application': cols[2].text.split()[0]
#         })

#     return projects

# def save(projects, path):
#     with open(path, 'w') as csvfile:
#         writer = csv.writer(csvfile)

#         writer.writerow(('Проект', 'Категории', 'Цена', 'Заявки'))

#         writer.writerows(
#             (project['title'], ', '.join(project['categories']), project['price'], project['application']) for project in projects
#         )


# def get_words():
#     with open("keyword.txt", "r") as keyword_file:
#         key = keyword_file.read().split(",")
#     return key


def main():
    # keywords = get_words()
    # for item in keywords:
    # print BASE_URL+keywords[0]
    total_pages_words = get_page_count(get_html(BASE_URL))
    print total_pages_words
    # total_pages_words = get_page_count(get_html(BASE_URL+item))

    # print('Всего найдено %d страниц...' % total_pages)

    # projects = []

    # for page in range(1, total_pages + 1):
    #     print('Парсинг %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
    #     projects.extend(parse(get_html(BASE_URL + "page=%d" % page)))

    # print('Сохранение...')
    # save(projects, 'projects.csv')


if __name__ == '__main__':
    main()
