#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that contains the line of code
needed to parse the entire collection of
html pages and save those in tsv files
"""
import utils
import parser_utils

print(utils.list_links_file_in_directory_by_extension('Wikipedia/', '.html'))
