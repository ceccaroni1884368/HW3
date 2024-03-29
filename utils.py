#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that gather functions
need in more than one of the previous
files like (collector, parser, etc.)
"""
import os
import pandas as pd


def list_links_file_in_directory_by_extension(directory, extension):
    list_file = os.listdir(path=directory)
    return_list = []
    for x in list_file:
        if extension in x:
            return_list.append(directory + x)
    return return_list


def load_data(path):
    dataframe = pd.read_csv(path, sep='\t')
    return dataframe


def load_dataframe():
    files = list_links_file_in_directory_by_extension('Wikipedia/tsv/', '.tsv')
    frames = [load_data(f) for f in files]
    result = pd.concat(frames, sort=True)
    return result


def print_actor(list_actor):
    print(list_actor)

