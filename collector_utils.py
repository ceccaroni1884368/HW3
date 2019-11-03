#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that stores the function
used in collector.py
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd


def save_webpage(url, file_name):
    html = urlopen(url)
    page_content = html.read()
    with open('Wikipedia/' + file_name, 'wb') as fid:
        fid.write(page_content)


def data_html_to_dataframe(file_name):
    soup = bs(open(file_name), "html.parser")
    wiki_links = {'idx': [],
                  'links': []}

    for tr in soup.findAll("tr"):
        for td in tr.findAll("td"):
            if 'http' in td.text:
                wiki_links['links'].append(td.text)
            else:
                wiki_links['idx'].append(td.text)
    df = pd.DataFrame(wiki_links, columns=['idx', 'links'])

    return df
