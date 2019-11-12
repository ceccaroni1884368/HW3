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





def conjunctive_query_and_ranking_score():
    query = input("Search: ")
    query = index_utils.format_document(query).split(" ")

    with open('Json/inverted_index_score.json') as json_file:
        inverted_index_score = json.load(json_file)

    index_for_query = {query[i]: {idx: tfidf for idx, tfidf in inverted_index_score[query[i]]}
                       for i in range(len(query))}

    query = {query[i]: index_utils.tfidf(query[i], query, query.count(query[i]), len(query))
             for i in range(len(query))}

    idx, score = index_utils.cosine_similar(query, index_for_query)


conjunctive_query_and_ranking_score()