# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import re, functools

def get_range(r):
    try:
        v = int(r)
        return [r, r+1]
    except TypeError:
        return map(lambda x: int(x), list(r))

def _exists(ranges, r):
    rs, re = get_range(r)
    for s, e in ranges:
        if rs >= s:
            rs = re if re <= e else e
        if rs==re:
            return True
        if s >= re:
            break
    return False

def add_range(s, e, ranges):
    assert e >= s
    if s == e:
        return

    if len(ranges) == 0:
        ranges.append([s,e])
    elif e == ranges[0][0]:
        ranges[0][0] = s
    elif e < ranges[0][0]:
        ranges.insert(0, [s,e])
    elif s == ranges[-1][1]:
        ranges[-1][1] = e
    elif s > ranges[-1][1]:
        ranges.append([s,e])
    else:
        idx = 0
        while s > ranges[idx][1]:
            idx += 1
        while idx < len(ranges) and s <= ranges[idx][0] and e >= ranges[idx][1]:
            del ranges[idx]
        if idx < len(ranges):
            if s < ranges[idx][0]:
                if e < ranges[idx][0]:
                    ranges.insert(idx, [s,e])
                elif e >= ranges[idx][0] and e < ranges[idx][1]:
                    ranges[idx][0] = s
                elif e >= ranges[idx][1]:
                    ranges.insert(idx, [s,e])
            elif s == ranges[idx][0]:
                if e >= ranges[idx][1]:
                    ranges.insert(idx, [s,e])
            elif s > ranges[idx][0]:
                if e >= ranges[idx][1]:
                    ranges[idx][1] = e
        else:
            ranges.append([s,e])

def generate_ranges(indices, initial_ranges=[]):
    ranges = initial_ranges
    for r in indices:
        s, e = get_range(r)
        add_range(s, e, ranges)
    return ranges


def has_range(range, ranges):
    pass

def has_index(index, ranges):
    pass

def pack_ranges(ranges):
    pass

def restore_range(r, restored_ranges):
    restored_ranges.append(get_range(r))

def collect_data(data, ranges):
    collected = []
    for s, e in ranges:
        for idx in range(s,e):
            collected.append(data['data'][idx])
    return collected

def restore(mapping, selected=None):
    if selected is None:
        selected = mapping['output']
    selected_ranges = generate_ranges(selected)
    if 'imap' in mapping:
        exists = functools.partial(_exists, selected_ranges)
        local_dict = {'exists':exists, 'E':exists}
        restored_ranges = []
        for r, expr in mapping['imap'].items():
            if eval(expr, globals(), local_dict):
                restore_range(r, restored_ranges)
        return collect_data(mapping['input'], restored_ranges)
    else:
        return collect_data(mapping, selected_ranges)
