#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that once executed generate
the indexes of the Search engines
"""
import utils
import index_utils


dataframe = utils.load_data(utils.list_links_file_in_directory_by_extension('Wikipedia/', '.tsv')[0])

print(index_utils.cosine_similar('Doctors', dataframe.fillna('None'), 'Title', 3))
