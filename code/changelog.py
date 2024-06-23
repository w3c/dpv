#!/usr/bin/env python3

from rdflib import Graph
from rdflib.term import BNode

COMPARE = (
    ('DPV', '2.0/dpv/dpv.ttl', 'v1.0/dpv/dpv.ttl'),
    ('PD', '2.0/pd/pd.ttl', 'v1.0/dpv-pd/dpv-pd.ttl'),
    ('EU-GDPR', '2.0/legal/eu/gdpr/eu-gdpr.ttl', 'v1.0/dpv-gdpr/dpv-gdpr.ttl'),
    ('LEGAL', '2.0/legal/legal.ttl', 'v1.0/dpv-legal/dpv-legal.ttl'),
    ('LOC', '2.0/loc/loc.ttl', 'v1.0/dpv-legal/dpv-legal.ttl'),
    ('TECH', '2.0/tech/tech.ttl', 'v1.0/dpv-tech/dpv-tech.ttl'),
    ('EU-RIGHTS', '2.0/legal/eu/rights/eu-rights.ttl', 'v1.0/rights/eu/rights-eu.ttl'),
    ('RISK', '2.0/risk/risk.ttl', 'v1.0/risk/risk.ttl'),
    ('AI', '2.0/ai/ai.ttl', None), # None means there is no old version
    ('Justifications', '2.0/justifications/justifications.ttl', None),
    ('EU-DGA', '2.0/legal/eu/dga/eu-dga.ttl', None),
    ('EU-AIAct', '2.0/legal/eu/aiact/eu-aiact.ttl', None),
    ('EU-NIS2', '2.0/legal/eu/nis2/eu-nis2.ttl', None),
    ('LEGAL-IE', '2.0/legal/ie/legal-ie.ttl', None),
    ('LEGAL-IN', '2.0/legal/in/legal-in.ttl', None),
    ('LEGAL-DE', '2.0/legal/de/legal-de.ttl', None),
    ('LEGAL-GB', '2.0/legal/gb/legal-gb.ttl', None),
    ('LEGAL-US', '2.0/legal/us/legal-us.ttl', None),
    ('LEGAL-EU', '2.0/legal/eu/legal-eu.ttl', None),
    )


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

# print(TOTAL)
# print(ADDED)
# print(REMOVED)