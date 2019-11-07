#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that contains the line of code
needed to parse the entire collection of
html pages and save those in tsv files
"""
import utils
import parser_utils

list_info_film = []
for link in utils.list_links_file_in_directory_by_extension('Wikipedia/', '.html'):
    print(link)
    list_info_film.append(parser_utils.html_to_dict(link))


parser_utils.save_tsv_dataframe(list_info_film)

