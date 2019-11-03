#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that contains the line of code
needed to collect your data from the html page
(from which you get the urls) and Wikipedia
"""
import utils
import collector_utils

n_file = input("number of file (1, 2, 3): ")
n_idx = input("start idx: ")
wiki_link_df = collector_utils.data_html_to_dataframe('data/movies' + n_file + '.html')
for i in range(int(n_idx)-1, len(wiki_link_df)):
    try:
        collector_utils.save_webpage(wiki_link_df.iloc[i]['links'],
                                     'article_' + wiki_link_df.iloc[i]['idx'] + '.html')
    except:
        print(wiki_link_df.iloc[i]['idx'])

