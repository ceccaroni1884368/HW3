#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that contains the implementation
of the algorithm that solves problem 4.
"""


def algorithm_palindrome_sub_string_len(string, idx_start, idx_end):
    """
    recursive algorithm
    """

    if idx_end < idx_start:
        return 0
    if idx_end == idx_start:
        return 1
    if string[idx_start] == string[idx_end]:
        return algorithm_palindrome_sub_string_len(string, idx_start+1, idx_end-1) + 2
    right = algorithm_palindrome_sub_string_len(string, idx_start+1, idx_end)
    left = algorithm_palindrome_sub_string_len(string, idx_start, idx_end-1)

    if right > left:
        return right
    else:
        return left


def palindrome_sub_string_len(string):
    return algorithm_palindrome_sub_string_len(string, 0, len(string)-1)


print(palindrome_sub_string_len(input('Insert string: ')))
