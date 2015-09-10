#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-

import csv
# для python 2.7 - urllib2
import urllib2
import requests
import pdb

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


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    work_item = soup.find('div', class_='js-catalog_after-ads')
    
    # print work_item
    # description = work_item.find_all('h3')

    # ".encode('utf-8')" нужен для правильной интерпретации unicode
    
    description = work_item.find_all('div', class_='description')

    # print description[0].div.text.encode('utf-8')

    data = []
    for item in description:

    #   cols = row.find_all('td')
        data.append({
            'title': item.a.text,
            'price': item.div.text,
    #         'categories': [category.text for category in cols[0].find_all('noindex')],
    #         'price': cols[1].text.strip().split()[0],
    #         'application': cols[2].text.split()[0]
        })
    # print data
    return data

def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(('Вакансия', 'Зарплата'))

        writer.writerows(
            # (project['title'].encode('utf-8'),) for project in projects
            (project['title'].encode('utf-8'), project['price'].encode('utf-8')) for project in projects
            # (project['title'], ', '.join(project['categories']), project['price'], project['application']) for project in projects
        )



def main():

    total_pages_words = get_page_count(get_html(BASE_URL))
    # print total_pages_words

    print('Всего найдено %d страниц...' % total_pages_words)

    projects = []

    # for page in range(1, total_pages + 1):
    #     print('Парсинг %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
    projects.extend(parse(get_html(BASE_URL + "?p=%d" % 127)))

    print('Сохранение...')
    save(projects, 'projects.csv')
    
    for item in projects:
        print item['title'].encode('utf-8'),
        print item['price'].encode('utf-8'),


if __name__ == '__main__':
    main()
