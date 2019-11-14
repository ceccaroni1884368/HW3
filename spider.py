import bs4
import requests
import re
import os
import pandas as pd
import random
import time


def save(html, path):
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs(os.path.split(path)[0])
    try:
        with open(path, 'wb') as f:
            f.write(html.encode('utf8'))
    except Exception as e:
        print('save error')


df = pd.DataFrame(columns=['film_name', 'director', 'producer',
                           'writer', 'starring', 'music', 'release date',
                           'country', 'language', 'budget', 'runtime'])


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
movies1 = open('data/movies3.html')
m1_soup = bs4.BeautifulSoup(movies1.read(), 'html5lib')
elems = m1_soup.select('a')
type(elems)

f_dict = {}
for i in elems:
    html = requests.get(i.getText(), headers=headers).text
    save(html, 'movie3/'+i.getText()[8:]+'.html')
    soup = bs4.BeautifulSoup(html, 'lxml')
    table = soup.find_all(attrs={"class": "infobox vevent"})
    tr = table[0].find_all('tr')
    final_dict = {}
    final_dict.update({'film_name': i.getText()[30:]})
    for j in tr:
        try:
            if j.select('th')[0].string == 'Directed by':
                final_dict.update({'director': j.select('td')[0].string})
        except IndexError as e:
            final_dict.update({'director': 'NA'})
        try:
            if j.select('th')[0].string == 'Produced by':
                final_dict.update({'producer': j.select('td')[0].string})
        except IndexError as e:
            final_dict.update({'producer': 'NA'})
        try:
            if j.select('th')[0].string == 'Written by':
                final_dict.update({'writter': j.select('td')[0].string})
        except IndexError as e:
            final_dict.update({'writter': 'NA'})
        try:
            if j.select('th')[0].string == 'Starring':
                final_dict.update({'starring': j.select('td')[0].string})
        except IndexError as e:
            final_dict.update({'starring': 'NA'})
        try:
            if j.select('th')[0].string == 'Music by':
                final_dict.update({'music': j.select('td')[0].string})
        except IndexError as e:
            final_dict.update({'music': 'NA'})
        try:
            if j.select('th')[0].string == 'Release date':
                final_dict.update({'Release date': j.select('td')[0].string})
        except IndexError as e:
            final_dict.update({'Release date': 'NA'})
        try:
            if j.select('th')[0].string == 'Running time':
                final_dict.update({'runtime,': j.select('td')[0].string})
        except IndexError as e:
            final_dict.update({'runtime': 'NA'})
        try:
            if j.select('th')[0].string == 'Country':
                final_dict.update({'Country': j.select('td')[0].string})
        except IndexError as e:
            final_dict.update({'Country': 'NA'})
        try:
            if j.select('th')[0].string == 'Language':
                final_dict.update({'Language': j.select('td')[0].string})
        except IndexError as e:
            final_dict.update({'Language': 'NA'})
        try:
            if j.select('th')[0].string == 'Budget':
                final_dict.update({'budget': j.select('td')[0].string})
        except IndexError as e:
            final_dict.update({'budget': 'NA'})
    df = df.append(final_dict, ignore_index=True)
    time.sleep(random.randint(1, 5))
    df.to_tsv('final.tsv')
