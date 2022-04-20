# -*- coding: utf-8 -*-

"""Utils module.

This module contains utility functions determinator package

"""

def merge_terms_dict(a, b):
    for key in b.keys():
        if key in a.keys() and a[key]['dc:language']==b[key]['dc:language']:
            for item in b[key]['dc:uri']:
                a[key]['dc:uri'].append(item)
            for item in b[key]['frequency']:
                a[key]['frequency'].append(item)
        else:
            a[key] = {}
            for b_key in b[key].keys():
                a[key][b_key] = b[key][b_key]