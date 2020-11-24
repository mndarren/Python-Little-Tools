#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. current_module:: little_funcs.py
.. created_by:: Darren Xie
.. created_on:: 11/02/2020

Give some basic ideas
"""
import os


# Change all files ext name in a dir
def rename_all_ext(dir_path=None):
    dir = 'default_path'
    new_ext = '.sql'
    os.chdir(dir)
    for count, filename in enumerate(os.listdir(dir)):
        pre, ext = os.path.splitext(filename)
        os.rename(filename, pre + new_ext)


# Check if all elements in list are unique
def is_any_item_unique(item):
    temp_set = set()
    return not any(i in temp_set or temp_set.add(i) for i in item)


# Check if all elements are the same in list
def is_any_item_same(items):
    return items.count(items[0]) == len(items)


# Compare 2 unsorted lists (anagram)
def is_same_list(list1, list2):
    from collections import Counter
    return Counter(list1) == Counter(list2)


# Get the most frequent item from a list
def get_most_frequent_item(list1):
    return max(set(list1), key=list1.count)


# Convert 2 lists into a dict
def list2dict(list1, list2):
    return dict(zip(list1, list2))


# swap values
def swap(a, b):
    b, a = a, b
    return a, b


# reverse string or list
def reverse(items):
    return items[::-1]


# Capitalize a list
def capitalize_list(list1):
    return map(str.capitalize, list1)


# Filter values
def filter_values(list1):
    return filter(eligibility, list1)


def eligibility(age):
    return age >= 24


# Merge 2 dictionaries
def merge_dicts(dict1, dict2):
    return {**dict1, **dict2}



