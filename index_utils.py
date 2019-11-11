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
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import json
import utils

def tokenizer(text):
    tkenizer = RegexpTokenizer(r'\w+')
    return tkenizer.tokenize(text)


def remove_stop_word(text):
    return [w for w in text if w not in stopwords.words('english')]


def word_lemmatizer(text):
    lemmatizater = WordNetLemmatizer()
    return [lemmatizater.lemmatize(w) for w in text]


def word_stemmer(text):
    # stemmer = PorterStemmer()
    stemmer = SnowballStemmer("english")
    return [stemmer.stem(w) for w in text]


def format_document(document):
    return " ".join(word_stemmer(remove_stop_word(tokenizer(document.lower()))))


def get_vocabulary(documents):
    vocabulary = set()
    for document in documents:
        vocabulary = vocabulary.union(set(tokenizer(document)))

    return vocabulary


def documents_index(documents, vocabulary):
    documents_idx = {}
    for word in vocabulary:
        documents_idx[word] = set()
        for idx in range(len(documents)):
            if word in documents[idx].lower():
                documents_idx[word].add(idx)
        documents_idx[word] = list(documents_idx[word])

    return documents_idx


def save_inverted_index(documents):
    vocabulary = get_vocabulary(documents)
    idx = documents_index(documents, vocabulary)

    with open('inverted_index.json', 'w') as f:
        json.dump(idx, f)


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

dataframe = utils.load_data(utils.list_links_file_in_directory_by_extension('Wikipedia/', '.tsv')[0])
