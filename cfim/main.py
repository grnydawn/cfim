# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import re, functools

class interval(object):
    def __init__(self, start, stop=None, left_open=False, right_open=False):
        if isinstance(start, int):
            if stop is None: stop = start + 1
            self.start = start+1 if left_open else start
            self.stop = stop-1 if right_open else stop
            if self.start > self.stop:
                self.start = None
                self.stop = None
        elif isinstance(start, interval):
            self.start = start.start
            self.stop = start.stop
        else:
            assert False
        self.current = self.start

    def __getitem__(self, key):
        assert isinstance(key, int)
        if key>=self.start and key<=self.stop:
            return True
        else:
            return False

    def __iter__(self):
        if self.start is None or self.stop is None:
            return iter([])
        else:
            self.current = self.start
            return self

    def __next__(self):
        if self.current is None or self.current>self.stop:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

    next = __next__

    def __hash__(self):
        return hash(self.slice())

    def __repr__(self):
        return str(self.slice())

    def slice(self):
        return self.start, self.stop if self.stop is None else self.stop+1

class intervals(object):
    pass

    def __contains__(self, index):
        pass

    def insert(self, index):
        pass

    def remove(self, index):
        pass


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
