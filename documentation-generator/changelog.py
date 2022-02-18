#!/usr/bin/env python3

from rdflib import Graph, Namespace
from rdflib import RDF, RDFS, OWL
from rdflib.term import Literal
SW = Namespace('http://www.w3.org/2003/06/sw-vocab-status/ns#')

GITHUB_REPO_RAW = 'https://raw.githubusercontent.com/w3c/dpv/master/'
GITHUB_DPV_RAW = f'{GITHUB_REPO_RAW}dpv/rdf/'
GITHUB_GDPR_RAW = f'{GITHUB_REPO_RAW}dpv-gdpr/rdf/'

LOCAL_DPV = '../dpv/modules/'
LOCAL_GDPR = '../dpv-gdpr/modules/'

DPV_MODULES = (
    'base',
    'personal_data_categories',
    'purposes',
    'processing',
    'technical_organisational_measures',
    'entities',
    'legal_basis',
    'consent',
    )
DPV_GDPR_MODULES = (
    'legal_basis',
    'rights',
    'data_transfers',
    )

import urllib
import tempfile


def download_file_to_rdf_graph(url):
    '''Downloads URL and loads into rdflib graph'''
    graph = Graph()
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        tfd = tempfile.NamedTemporaryFile()
        with open(tfd.name, 'w') as fd:
            fd.write(data)
        graph.load(tfd, format='turtle')
    except urllib.error.HTTPError:
        pass
    return graph


def compare_iterations(old, new):
    '''compare old and new iterations of a graph
    returns added, removed, changed sets of concepts'''
    added = new - old
    added = tuple(
        x.split('#')[1] for x in added.subjects(RDF.type, RDFS.Class))
    removed = old - new
    removed = tuple(
        x.split('#')[1] for x in removed.subjects(RDF.type, RDFS.Class))
    changed = tuple(x.split('#')[1] for x in new.subjects(
        SW.term_status, Literal('changed', lang='en')))
    return added, removed, changed


# DPV
print('--- DPV --- ')
for module in DPV_MODULES:
    print(f'MODULE: {module}')
    old = download_file_to_rdf_graph(f'{GITHUB_DPV_RAW}{module}.ttl')
    new = Graph()
    new.load(f'{LOCAL_DPV}{module}.ttl', format='turtle')
    removed, added, changed = compare_iterations(old, new)
    print(f'added: {len(added)} ; removed: {len(removed)} ; changed: {len(changed)}')
    if removed:
        print('\nTerms Removed')
        for term in removed:
            print(term)
    if added:
        print('\nTerms Added')
        for term in added:
            print(term)
    if changed:
        print('\nTerms Changed')
        for term in changed:
            print(term)
    print('\n')


# DPV-GDPR
print('\n\n--- DPV-GDPR --- ')
for module in DPV_GDPR_MODULES:
    print(f'MODULE: {module}')
    old = download_file_to_rdf_graph(f'{GITHUB_GDPR_RAW}{module}.ttl')
    new = Graph()
    new.load(f'{LOCAL_GDPR}{module}.ttl', format='turtle')
    removed, added, changed = compare_iterations(old, new)
    print(f'added: {len(added)} ; removed: {len(removed)} ; changed: {len(changed)}')
    if removed:
        print('\nTerms Removed')
        for term in removed:
            print(term)
    if added:
        print('\nTerms Added')
        for term in added:
            print(term)
    if changed:
        print('\nTerms Changed')
        for term in changed:
            print(term)
    print('\n')
