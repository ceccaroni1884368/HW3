#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that gather functions
need in more than one of the previous
files like (collector, parser, etc.)
"""
import os


def list_links_file_in_directory_by_extension(directory, extension):
    list_file = os.listdir(path=directory)
    return_list = []
    for x in list_file:
        if extension in x:
            return_list.append(directory + x)
    return return_list
