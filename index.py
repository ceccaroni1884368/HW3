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
dataframe = utils.load_dataframe()


def generate_inverted_index():
    # Save Format Documents (Intro + Plot)
    documents = []
    for i in range(len(dataframe[['Intro']])):
        documents.append(str(dataframe['Intro'].iloc[i]) + str(dataframe['Plot'].iloc[i]))
    index_utils.save_format_documents(documents, 'format_documents')

    # Save Inverted Index
    with open('Json/format_documents.json') as json_file:
        documents = json.load(json_file)
    index_utils.save_inverted_index(documents)


def generate_inverted_index_score():
    with open('Json/format_documents.json') as json_file:
        documents = json.load(json_file)

    with open('Json/inverted_index.json') as json_file:
        inverted_index = json.load(json_file)

    for word in inverted_index:
        for i in range(len(inverted_index[word])):
            inverted_index[word][i] = [inverted_index[word][i],
                                       index_utils.tfidf(word,
                                                         documents[inverted_index[word][i]],
                                                         len(inverted_index[word]),
                                                         len(documents))]
    # Save Inverted Index Score
    with open('Json/inverted_index_score.json', 'w') as f:
        json.dump(inverted_index, f)


generate_inverted_index()
generate_inverted_index_score()
