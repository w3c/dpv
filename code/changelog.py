#!/usr/bin/env python3

import os

from rdflib import Graph
from rdflib.term import BNode

from vocab_management import DPV_VERSION, DPV_PREVIOUS_VERSION
from vocab_management import EXPORT_RDF_PATH
from vocab_management import RDF_VOCABS

COMPARE = []

for vocab, data in RDF_VOCABS.items():
    path = data['vocab']
    path_prev = path.replace(DPV_VERSION, DPV_PREVIOUS_VERSION)
    if not os.path.exists(path_prev):
        path_prev = None
    else:
        path_prev = path_prev.replace('../', '')
    COMPARE.append((
        data['metadata']['dct:title'],
        path.replace('../', ''),
        path_prev,
        ))

# import sys; sys.exit(0)

TOTAL = 0
ADDED = 0
REMOVED = 0

def _compare_iterations(graph_old, graph_new, ignore_BNode=True):
    '''compare old and new iterations of a graph
    returns added, removed, changed sets of concepts'''
    old = set()
    new = set()
    for s in graph_old.subjects(None, None):
        if '#' not in s: continue
        s = s.split('#')[1]
        if not s: continue
        old.add(s)
    for s in graph_new.subjects(None, None):
        if '#' not in s: continue
        s = s.split('#')[1]
        if not s: continue
        new.add(s)
    # added: things in new set that are not in old set
    added = new - old
    # removed: things in old set that are not in new set
    removed = old - new
    if ignore_BNode:
        # ignore changes in BNodes
        added = [n for n in added if type(n) is not BNode]
        removed = [n for n in removed if type(n) is not BNode]
    global TOTAL
    TOTAL += len(new)
    global ADDED
    ADDED += len(added)
    global REMOVED
    REMOVED += len(removed)
    return len(new), added, removed


def _print_stats(total, added, removed):
    '''print statistics and information about terms
    will output added terms, removed terms'''
    summary = []
    details = []
    summary.append(f'total terms: {total} ; added: {len(added)} ; removed: {len(removed)}')
    details.append(f'total terms: {total} ; added: {len(added)} ; removed: {len(removed)}')
    if removed:
        details.append('Concepts Removed')
        for index, term in enumerate(sorted(removed)):
            details.append((index+1, term))
    if added:
        details.append('Concepts Added')
        for index, term in enumerate(sorted(added)):
            details.append((index+1, term))
    details.append('-'*8)
    return summary, details


def _compare(newpath, oldpath=None):
    graph_new = Graph()
    graph_new.parse(newpath, format='turtle')
    graph_old = Graph()
    if oldpath:
        graph_old.parse(oldpath, format='turtle')
    total, added, removed = _compare_iterations(graph_old, graph_new)
    return _print_stats(total, added, removed)

summary = []
details = []
for name, new, old in COMPARE:
    short, long = _compare(new, old)
    summary.append((name, *short))
    details.append((name, long))

PRINT_MODE_SHORT = False
# PRINT_MODE_SHORT = True

if PRINT_MODE_SHORT:
    for vocab, stats in summary:
        print(f'{vocab}: {stats}')
else:
    for vocab, items in details:
        print(vocab)
        for line in items:
            if type(line) is tuple:
                print(f'{line[0]}: {line[1]}')
            else:
                print(line)

print(TOTAL)
print(ADDED)
print(REMOVED)