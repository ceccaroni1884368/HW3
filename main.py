#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that once executed build up the search engine.
This file is very important because it is going to be the one
you will launch during the exam, ideed you will perform live
queries on your search engine. In order to let everything go
the best, you have to be sure that the engine will work on
pre-computed indeces. Thus, forget to allow the main file to
build the index from scratch. When the user executes the file
it should be able to choose:
+ search_engine: a parameter that the user set to choose the
  search engine to run. According to the request of the
  homework, you can get 1,2 or 3.
+ Any other parameters you would like.
"""

import utils
import index_utils
import json


dataframe = utils.load_dataframe()


def conjunctive_query():
    query = input("Search: ")
    query = index_utils.format_document(query).split(" ")

    with open('Json/inverted_index.json') as json_file:
        inverted_index = json.load(json_file)

    idx = set(inverted_index[query[0]])
    for word in query:
        idx = idx.intersection(inverted_index[word])
    idx = list(idx)

    return dataframe[['Title', 'Intro', 'Wikipedia Url']].iloc[idx]
