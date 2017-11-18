# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from functools import partial
import interval

class span(interval.interval):
    '''This is a placeholder for future modification
    for supporting integer-only indexing
    '''
    pass

def _exists(ranges, r):
    return r in ranges

def collect_data(data, ranges):
    collected = []
    for s, e in ranges:
        for idx in range(int(s),int(e+1)):
            collected.append(data['data'][idx])
    return collected

def intspan(r, ranges):
    start = stop = r
    if r-1 in ranges:
        start = r - 1
    if r+1 in ranges:
        start = r + 1
    return span((start, stop))

def normalize(r, ranges):
    if isinstance(r, int):
        return intspan(r, ranges)
    elif isinstance(r, span):
        return r
    else:
        raise Exception('%s is not supported.'%r.__class__.__name__)

def restore(mapping, ranges=None):

    if ranges is None:
        ranges = mapping['output']

    if isinstance(ranges, int):
        ranges = span(ranges)
    elif not isinstance(ranges, span):
        _ranges = span()
        try:
            for r in ranges:
                _ranges |= normalize(r, _ranges)
        except:
            raise Exception('%s is not supported.'%ranges.__class__.__name__)
        ranges = _ranges

    if 'imap' in mapping:
        exists = partial(_exists, ranges)
        local_dict = {'exists':exists, 'E':exists}
        restored_ranges = span()
        for r, expr in mapping['imap'].items():
            if eval(expr, globals(), local_dict):
                restored_ranges |= normalize(r, restored_ranges)
        return collect_data(mapping['input'], restored_ranges)
    else:
        return collect_data(mapping, ranges)
