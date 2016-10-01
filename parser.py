#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-

import csv
# для python 2.7 - urllib2
import urllib2
import requests
from time import sleep

from bs4 import BeautifulSoup


BASE_URL = 'https://www.avito.ru/sankt-peterburg/rabota'


def get_html(url):
    response = urllib2.urlopen(url)
    return response.read()


def get_page_count(html):
    # 'html.parser' для совместмости с debian 8. без этого на debian не работает. на ubuntu нормально.
    soup = BeautifulSoup(html, 'html.parser')
    paggination = soup.find('div', class_='pagination-pages clearfix')
    # основаная строка для парсинга количества страниц
    return int(paggination.find_all('a', href=True)[-1]['href'][-3:])


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    work_item = soup.find('div', class_='js-catalog_after-ads')
    

    
    description = work_item.find_all('div', class_='description')

    data = []
    for item in description:

        data.append({
            'title': item.a.text.strip(),
            'price': item.find('div', class_='about').text.strip()[:-5],
            'type': item.find('div', class_='data').p.text.strip(),
        })
    # print data
    return data

def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(('Вакансия', 'Зарплата', 'Тип'))

        writer.writerows(
            # ".encode('utf-8')" нужен для правильной интерпретации unicode
            (project['title'].encode('utf-8'),
             project['price'].encode('utf-8'),
             project['type'].encode('utf-8'),
            ) for project in projects
        )


def main():

    total_pages_words = get_page_count(get_html(BASE_URL))

    print('Всего найдено %d страниц...' % total_pages_words)

    projects = []
    try:
        for page in range(1, total_pages_words + 1):
            print('Парсинг %d%% (%d/%d)' % (int(float(page) / float(total_pages_words) * 100), page, total_pages_words))
            projects.extend(parse(get_html(BASE_URL + "?p=%d" % page)))
	    sleep(10)
    finally:    
        print('Сохранение...')
        save(projects, 'projects_all.csv')

    # печать для теста
    # for item in projects:
    #     print item['title'].encode('utf-8'),
    #     print item['price'].encode('utf-8'),


if __name__ == '__main__':
    main()
