#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that contains the functions
used for creating indexes
"""

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import json
import math
import pandas as pd



def tokenizer(text):
    tkenizer = RegexpTokenizer(r'\w+')
    return tkenizer.tokenize(text)


def remove_stop_word(text):
    return [w for w in text if w not in stopwords.words('english')]


def word_lemmatizer(text):
    lemmatizater = WordNetLemmatizer()
    return [lemmatizater.lemmatize(w) for w in text]


def word_stemmer(text):
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


def tfidf(word, document, df, N):
    tf = int(document.count(word))/len(document)
    idf = math.log(N/df)
    return tf * idf


def save_format_documents(documents, name):
    format_documents = []
    for i in range(len(documents)):
        format_documents.append(format_document(documents[i]))

    with open('Json/' + name + '.json', 'w') as f:
        json.dump(format_documents, f)


def save_inverted_index(documents):
    vocabulary = get_vocabulary(documents)
    idx = documents_index(documents, vocabulary)

    with open('Json/inverted_index.json', 'w') as f:
        json.dump(idx, f)


def cosine_similar(query, index_for_query):
    # Cosine Similarity(Query,Document1) = Dot product(Query, Document1) / ||Query|| * ||Document1||
    documents_tfidf = pd.DataFrame(index_for_query).fillna(0)
    documents_tfidf.loc[:, 'den'] *= -1
    pass


"""
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
"""

