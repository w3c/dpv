#!/usr/bin/env python3

from rdflib import Graph, Namespace
from rdflib import RDF, RDFS, OWL
from rdflib.term import Literal
SW = Namespace('http://www.w3.org/2003/06/sw-vocab-status/ns#')

GITHUB_REPO_RAW = 'https://raw.githubusercontent.com/w3c/dpv/master/'
GITHUB_DPV_RAW = f'{GITHUB_REPO_RAW}dpv/modules/'
GITHUB_GDPR_RAW = f'{GITHUB_REPO_RAW}dpv-gdpr/modules/'
GITHUB_PD_RAW = f'{GITHUB_REPO_RAW}dpv-pd/'

LOCAL_DPV = '../dpv/modules/'
LOCAL_GDPR = '../dpv-gdpr/modules/'
LOCAL_PD = '../dpv-pd/'

DPV_MODULES = (
    'base',
    'consent',
    'context',
    'entities_authority',
    'entities_datasubject',
    'entities_legalrole',
    'entities_organisation',
    'entities',
    'jurisdiction',
    'legal_basis',
    'personal_data',
    'processing_context',
    'processing',
    'purposes',
    'risk',
    'technical_organisational_measures',
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


def compare_iterations(graph_old, graph_new):
    '''compare old and new iterations of a graph
    returns added, removed, changed sets of concepts'''
    old = set(s for s in graph_old.subjects(None, None))
    new = set(s for s in graph_new.subjects(None, None))
    # added: things in new set that are not in old set
    added = new - old
    print(f'added: {len(added)}')
    # removed: things in old set that are not in new set
    removed = old - new
    print(f'removed: {len(removed)}')
    return added, removed


# DPV
print('--- DPV --- ')
for module in DPV_MODULES:
    print(f'MODULE: {module}')
    old = download_file_to_rdf_graph(f'{GITHUB_DPV_RAW}{module}.ttl')
    new = Graph()
    new.load(f'{LOCAL_DPV}{module}.ttl', format='turtle')
    added, removed = compare_iterations(old, new)
    print(f'added: {len(added)} ; removed: {len(removed)}')
    if removed:
        print('Concepts Removed')
        for term in removed:
            print(term)
    if added:
        print('\nConcepts Added')
        for term in added:
            print(term)
    print('---')


# DPV-GDPR
print('\n--- DPV-GDPR --- ')
for module in DPV_GDPR_MODULES:
    print(f'MODULE: {module}')
    old = download_file_to_rdf_graph(f'{GITHUB_GDPR_RAW}{module}.ttl')
    new = Graph()
    new.load(f'{LOCAL_GDPR}{module}.ttl', format='turtle')
    added, removed = compare_iterations(old, new)
    print(f'added: {len(added)} ; removed: {len(removed)}')
    if removed:
        print('Concepts Removed')
        for term in removed:
            print(term)
    if added:
        print('\nConcepts Added')
        for term in added:
            print(term)
    print('---')


# DPV-PD
print('\n--- DPV-PD ---')
old = download_file_to_rdf_graph(f'{GITHUB_PD_RAW}dpv-pd.ttl')
new = Graph()
new.load(f'{LOCAL_PD}dpv-pd.ttl', format='turtle')
added, removed = compare_iterations(old, new)
print(f'added: {len(added)} ; removed: {len(removed)}')
if removed:
    print('\nConcepts Removed')
    for term in removed:
        print(term)
if added:
    print('Concepts Added')
    for term in added:
        print(term)
print('---')
