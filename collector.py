#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that contains the line of code
needed to collect your data from the html page
(from which you get the urls) and Wikipedia
"""
import utils
import collector_utils

n_file = input("Number of file (1, 2, 3): ")
n_idx = input("Start idx: ")
wiki_link_df = collector_utils.data_html_to_dataframe('data/movies' + n_file + '.html')
for i in range(int(n_idx)-int(wiki_link_df.iloc[0]['idx']), len(wiki_link_df)):
    try:
        collector_utils.save_webpage(wiki_link_df.iloc[i]['links'],
                                     'article_' + wiki_link_df.iloc[i]['idx'] + '.html')
    except:
        print('link n.', wiki_link_df.iloc[i]['idx'], 'does not exists')

