#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that gathers the function used in parser.py
"""
from bs4 import BeautifulSoup as bs
import pandas as pd


def html_to_dict(file_name):
    with open(file_name, 'rb') as html:
        soup = bs(html, 'html.parser')
    for x in soup.find_all('p'):
        print(x.text)

html_to_dict('Wikipedia/article_3.html')