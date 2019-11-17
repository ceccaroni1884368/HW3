
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
from math import log, sqrt
import heapq


# Dataframe
dataframe = utils.load_dataframe().reset_index(drop=True)

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
        try:
            with open(r'Json\inverted_index_dict.json', 'r') as f:
                self.index = json.load(f)
        except:
            print("Load Error Database")
        r = {}
        for term in query.split(' '):
            if term in self.index:
                r.update({term: self.index[term]})
            else:
                r.update({term: []})
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
            idx_set = idx_set.intersection(l[i])

        return dataframe[['Title', 'Intro', 'Wikipedia Url']].iloc[list(idx_set)].reset_index(drop=True)

    def generate_tfidf(self):
        D = len(dataframe_df[['Intro+Plot']])
        for word in self.index:
            d = len(self.index[word])
            for doc_dict in self.index[word]:
                tfidf = (doc_dict['frequency'] / len(dataframe_df['Intro+Plot'].iloc[doc_dict['docId']].split(" "))) * (1 + log(D/d))
                doc_dict['tfidf'] = tfidf
        with open(r'Json\inverted_index_tfidf.json', 'w') as f:
            json.dump(self.index, f)

    def lookup_conjunctive_query_and_ranking_score(self, query):
        # import inverted index tfidf database
        try:
            with open(r'Json\inverted_index_tfidf.json', 'r') as f:
                self.index = json.load(f)
        except:
            with open(r'Json\inverted_index_dict.json', 'r') as f:
                self.index = json.load(f)
            self.generate_tfidf()
            with open(r'Json\inverted_index_tfidf.json', 'r') as f:
                self.index = json.load(f)

        index_for_query = {term: self.index[term] for term in query.split(' ') if term in self.index}

        # calculate tfidf for query
        query_tfidf = []
        query_split = query.split(' ')
        tf = 1 / len(query_split)
        for word in query_split:
            try:
                idf = 1 + log(len(dataframe_df[['Intro+Plot']])/len(self.index[word]))
            except:
                idf = 1
            query_tfidf.append({'word': word, 'tfidf': tf*idf})

        # calculate cosine similarity
        ## index -> dataframe
        index_for_query_df = {word: {doc_dict['docId']: doc_dict['tfidf'] for doc_dict in index_for_query[word]}
                              for word in index_for_query}
        index_for_query_df = pd.DataFrame(index_for_query_df).fillna(0)

        ## Cosine similarity
        col_list = list(index_for_query_df)

        index_for_query_df.loc[:, 'den'] = ((index_for_query_df.loc[:, col_list] ** 2)[col_list].sum(axis=1)) ** (1/2)
        index_for_query_df.loc[:, 'num'] = 0
        query_mod = 0

        for i in range(len(query_tfidf)):
            if query_tfidf[i]['word'] in index_for_query_df:
                index_for_query_df.loc[:, 'num'] += index_for_query_df.loc[:, query_tfidf[i]['word']] * query_tfidf[i]['tfidf']
            query_mod += (query_tfidf[i]['tfidf'] ** 2)
        query_mod = sqrt(query_mod)
        index_for_query_df.loc[:, 'den'] *= query_mod
        index_for_query_df.loc[:, 'Similarity'] = index_for_query_df.loc[:, 'num'] / index_for_query_df.loc[:, 'den']
        df_similarity = pd.merge(dataframe[['Title', 'Intro', 'Wikipedia Url']], index_for_query_df[['Similarity']],
                                 left_index=True, right_index=True, sort=True)
        df_similarity = df_similarity.sort_values(by=['Similarity'], ascending=False)

        return df_similarity[df_similarity['Similarity'] >= 0.75].reset_index(drop=True)

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


def define_new_score(query, k):
    # Trovare per cosa cercare + ripulire testo
    heap = []
    try:
        what = pd.read_json(r'Json\dataframe_format_all.json', orient='table')
    except:
        what = index_utils.generate_format_for_new_score(dataframe)

    what = what[['All']]
    format_query = index_utils.format_text(query)

    for i in range(len(what)):
        heapq.heappush(heap, [index_utils.get_jaccard_sim(format_query, str(what.iloc[i])), i])
    result = {int(x[1]): float(x[0])for x in heapq.nlargest(k, heap) if float(x[0]) > 0}

    if result:
        new_score_df = pd.DataFrame(heapq.nlargest(k, heap), columns=['Similarity', 'idx'])
        df_similarity = pd.merge(dataframe[['Title', 'Intro', 'Wikipedia Url']], new_score_df[['Similarity', 'idx']],
                                 left_index=True, right_on='idx', sort=True)
        df_similarity = df_similarity.sort_values(by=['Similarity'], ascending=False)
        return df_similarity[['Title', 'Intro', 'Wikipedia Url', 'Similarity']]
    else:
        return 'Not Found'
