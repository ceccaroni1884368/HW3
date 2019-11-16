
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that once executed generate
the indexes of the Search engines
"""
import utils
import pandas as pd
import json
import index_utils


# Dataframe
dataframe = utils.load_dataframe()

# Dataframe (Intro + Plot) Documents
try:
    dataframe_df = pd.read_json(r'Json\dataframe_format_intro_plot.json', orient='table')
except ValueError:
    # Generate (Intro + Plot) Documents
    dataframe_df = index_utils.generate_format_intro_plot_df(dataframe)

# Vocabulary
try:
    vocabulary = pd.read_json(r'Json\vocabulary.json', orient='table')
except ValueError:
    vocabulary = index_utils.generate_vocabulary_df(dataframe_df)
vocabulary_dict = dict(vocabulary['Word'])


# InvertedIndex
class InvertedIndex:
    """
    Inverted Index class.
    """

    def __init__(self, index):
        self.index = index

    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.index)

    def index_document(self, document):
        """
        Process a given document, save it to the DB and update the index.
        """

        # Remove punctuation from the text.
        clean_text = index_utils.format_text(document['text'])
        terms = clean_text.split(' ')
        appearances_dict = dict()
        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            term_frequency = appearances_dict[term]['frequency'] if term in appearances_dict else 0
            appearances_dict[term] = {'docId': document['id'], 'frequency': (term_frequency + 1)}

        # Update the inverted index
        update_dict = {key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items()}
        self.index.update(update_dict)
        # Add the document into the database
        return document

    def lookup_conjunctive_query(self, query):
        r = {term: self.index[term] for term in query.split(' ') if term in self.index}
        j = 0
        l = []
        for d in r:
            t = []
            for i in range(len(r[d])):
                t.append(r[d][i]['docId'])
            l.append(set(t))
            j += 1
        idx_set = l[0]
        for i in range(1, len(l)):
            idx_set.intersection(l[i])

        return dataframe[['Title', 'Intro', 'Wikipedia Url']].iloc[list(idx_set)]

    def generate_tfidf(self):
        for word in self.index:
            for doc_dict in self.index[x]:
                doc_dict['frequency'] = (doc_dict['frequency'] / len(dataframe_df['Intro+Plot'].iloc[doc_dict['docId']]))

    def lookup_query_conjunctive_query_and_ranking_score(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances.
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        # DA FARE!!!!!!!!!!
        return {term: self.index[term] for term in query.split(' ') if term in self.index}

    def save_inverted_index(self):
        with open(r'Json\inverted_index_dict.json', 'w') as f:
            json.dump(self.index, f)


try:
    with open(r'Json\inverted_index_dict.json', 'r') as f:
        idx = json.load(f)
except:
    idx = {}
    index = InvertedIndex(idx)
    # Dataframe (Intro + Plot)
    dataframe_df = dataframe_df['Intro+Plot']
    for idx in range(len(dataframe_df)):
        index.index_document({'id': idx, 'text': dataframe_df.iloc[idx]})

    index.save_inverted_index()
    with open(r'Json\inverted_index_dict.json', 'r') as f:
        idx = json.load(f)

