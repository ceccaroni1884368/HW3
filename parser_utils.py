#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that gathers the function used in parser.py
"""
from bs4 import BeautifulSoup as bs
import re
import pandas as pd


def html_to_dict(file_name):
    film_dict = {}
    with open(file_name, 'rb') as html:
        soup = bs(html, 'html.parser')

    title = soup.title.text
    title = re.sub(r' - Wikipedia', '', title)
    film_dict.update({"Title": title})
    p = soup.find_all("p")
    if len(p) >= 2:
        intro = p[0].text
        intro = re.sub(r'\n', '', intro)
        intro = re.sub(r'\[\d*\]', '', intro)
        film_dict.update({"Intro": intro})

        plot = p[1].text
        plot = re.sub(r'\n', '', plot)
        plot = re.sub(r'\[\d*\]', '', plot)
        film_dict.update({"Plot": plot})

    infobox = soup.find_all("table", {"class": "infobox vevent"})

    if infobox:
        infobox = infobox[0]

        descriptions_wiki = infobox.find_all("th", {"scope": "row", "style": "white-space:nowrap;padding-right:0.65em;"})
        descriptions = []
        for description in descriptions_wiki:
            descriptions.append(description.text)
        variables_wiki = infobox.find_all('td', {"class": ""})
        variables = []

        for i in range(len(variables_wiki)):
            text = variables_wiki[i].text
            if '  ' == text[:2]:
                text = text[2:]
            if '\n' == text[:1]:
                text = text[1:]
            if '  ' == text[-2:]:
                text = text[:-2]
            if '\n' == text[-1:]:
                text = text[:-1]
            text = re.sub(r'\[\d*\]', '', text)
            text = text.replace("  ", ", ")
            text = text.replace("\n", ", ")
            if i == 0 and text == '':
                pass
            else:
                variables.append(text)

        for i in range(len(descriptions)):
            film_dict.update({descriptions[i]: variables[i]})

    return film_dict


# print(html_to_dict('Wikipedia/article_200.html'))

def save_tsv_dataframe(list_info_film):
    dataframe = pd.DataFrame(list_info_film)
    dataframe = dataframe.dropna(subset=['Plot'])
    n_file = input("Number of movies file (1, 2, 3): ")
    name_file = 'Wikipedia/movie' + n_file + '.tsv'
    dataframe.to_csv(name_file, delimiter='\t', index=False)
