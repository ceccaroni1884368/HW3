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
import index
import index_utils


index = index.InvertedIndex(index.idx)


def menu():
    choice = 0
    while choice != 1 and choice != 2:
        print("1 - Search without score\n2 - Search with score")
        choice = int(input("Number (1 - 2): "))

    result = 'None'
    search_term = input("Enter term(s) to search: ")
    if choice == 1:
        result = index.lookup_conjunctive_query(index_utils.format_text(search_term))
    elif choice == 2:
        result = index.lookup_conjunctive_query_and_ranking_score(index_utils.format_text(search_term))

    return result


while True:
    print(menu())

