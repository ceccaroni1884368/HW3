#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that once executed generate
the indexes of the Search engines
"""
import json
import utils
import index_utils

# Dataframe
dataframe = utils.load_data(utils.list_links_file_in_directory_by_extension('Wikipedia/', '.tsv')[0])


def generate_inverted_index():
    documents = []
    for i in range(len(dataframe[['Intro']])):
        documents.append(index_utils.format_document(str(dataframe['Intro'].iloc[i]) + str(dataframe['Plot'].iloc[i])))

    index_utils.save_inverted_index(documents)


def conjunctive_query():
    query = input("Search: ")
    query = index_utils.format_document(query).split(" ")

    with open('inverted_index.json') as json_file:
        inverted_index = json.load(json_file)

    idx = set(inverted_index[query[0]])
    for word in query:
        idx = idx.intersection(inverted_index[word])
    idx = list(idx)

    return dataframe[['Title', 'Intro', 'Wikipedia Url']].iloc[idx]

print(conjunctive_query())
