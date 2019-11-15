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
import utils
from collections import Counter


def tokenizer(text):
    tkenizer = RegexpTokenizer(r'\w+')
    return tkenizer.tokenize(text)


def remove_stop_word(text):
    return [w for w in text if w not in stopwords.words('english')]


def word_lemmatizer(text):
    lemmatizater = WordNetLemmatizer()
    return [lemmatizater.lemmatize(w, pos="v") for w in text]


def word_stemmer(text):
    stemmer = SnowballStemmer("english")
    return [stemmer.stem(w) for w in text]


def format_text(text):
    text = text.lower()
    text = tokenizer(text)
    text = remove_stop_word(text)
    text = word_lemmatizer(text)
    return " ".join(text)


def generate_format_intro_plot_df(dataframe):
    dataframe.loc[:, 'Intro+Plot'] = dataframe.fillna('').loc[:, 'Intro'] + dataframe.fillna('').loc[:, 'Plot']
    dataframe['Intro+Plot'] = dataframe['Intro+Plot'].apply(lambda x: format_text(x))
    dataframe.to_json(r'Json\dataframe_format_intro_plot.json', index=False, orient='table')
    return dataframe


def generate_vocabulary_df(dataframe_df):
    vocabulary = list(set((' '.join(dataframe_df['Intro+Plot'].tolist())).split(' ')))
    vocabulary.remove('')
    vocabulary = pd.DataFrame(vocabulary, columns=['Word'])
    vocabulary.to_json(r'Json\vocabulary.json', index=False, orient='table')
    return vocabulary


def generate_tf_idf_df(inverted_index):
    pass


def save_dataframe(dataframe, name_file):
    name_file = 'tsv/' + name_file + '.tsv'
    dataframe.to_csv(name_file, sep='\t', index=False)


