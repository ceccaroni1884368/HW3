#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that contains the functions
used for creating indexes
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np


# https://medium.com/@deangelaneves/how-to-build-a-search-engine-from-scratch-in-python-part-1-96eb240f9ecb
def cosine_similar(search_keys, dataframe, label, min_talks=1):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_weights_matrix = tfidf_vectorizer.fit_transform(dataframe.loc[:, label])
    search_query_weights = tfidf_vectorizer.transform([search_keys])

    cosine_distance = cosine_similarity(search_query_weights, tfidf_weights_matrix)
    similarity_list = cosine_distance[0]

    dataframe_similarity = dataframe.join(pd.DataFrame(similarity_list, columns=['Similarity']))

    most_similar = []

    while min_talks > 0:
        tmp_index = np.argmax(similarity_list)
        most_similar.append(tmp_index)
        similarity_list[tmp_index] = 0
        min_talks -= 1

    return dataframe_similarity.iloc[most_similar]


# cosine_similar('Doctors', dataframe.fillna('None'), 'Title', 3)
