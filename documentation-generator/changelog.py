#!/usr/bin/env python3

from rdflib import Graph, Namespace
from rdflib import RDF, RDFS, OWL
from rdflib.term import Literal, BNode
SW = Namespace('http://www.w3.org/2003/06/sw-vocab-status/ns#')

GITHUB_REPO_RAW = 'https://raw.githubusercontent.com/coolharsh55/dpv/master/'
GITHUB_DPV_RAW = f'{GITHUB_REPO_RAW}dpv/modules/'
GITHUB_DPV_GDPR_RAW = f'{GITHUB_REPO_RAW}dpv-gdpr/modules/'
GITHUB_DPV_PD_RAW = f'{GITHUB_REPO_RAW}dpv-pd/'
GITHUB_DPV_LEGAL_RAW = f'{GITHUB_REPO_RAW}dpv-legal/modules/'
GITHUB_DPV_TECH_RAW = f'{GITHUB_REPO_RAW}dpv-tech/'
GITHUB_RISK_RAW = f'{GITHUB_REPO_RAW}risk/modules/'
GITHUB_RIGHTS_EU_RAW = f'{GITHUB_REPO_RAW}rights/eu/'

LOCAL_DPV = '../dpv/modules/'
LOCAL_DPV_GDPR = '../dpv-gdpr/modules/'
LOCAL_DPV_PD = '../dpv-pd/'
LOCAL_DPV_LEGAL = '../dpv-legal/modules/'
LOCAL_DPV_TECH = '../dpv-tech/'
LOCAL_RISK = '../risk/modules/'
LOCAL_RIGHTS_EU = '../rights/eu/'

DPV_MODULES = (
    'base',
    'consent_status',
    'consent',
    'consent_types',
    'context',
    'entities_authority',
    'entities_datasubject',
    'entities_legalrole',
    'entities_organisation',
    'entities',
    'jurisdiction',
    'legal_basis',
    'organisational_measures',
    'personal_data',
    'processing_context',
    'processing_scale',
    'processing',
    'purposes',
    'risk',
    'status',
    'technical_measures',
    'technical_organisational_measures',
    'rights',
    'rules',
    )
DPV_GDPR_MODULES = (
    'legal_basis',
    'legal_basis_special',
    'legal_basis_data_transfer',
    'rights',
    'data_transfers',
    'dpia',
    'compliance',
    )
DPV_LEGAL_MODULES = (
    'authorities',
    'eu_adequacy',
    'eu_eea',
    'laws',
    'locations',
    'ontology',
    )
RISK_MODULES = (
    'risk_consequences',
    'risk_assessment',
    'risk_controls',
    'risk_levels',
    'risk_matrix',
    )
RIGHTS_MODULES = (
    'rights-eu',
    )

import urllib
import tempfile


def _download_file_to_rdf_graph(url):
    '''Downloads URL and loads into rdflib graph'''
    graph = Graph()
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        tfd = tempfile.NamedTemporaryFile()
        with open(tfd.name, 'w') as fd:
            fd.write(data)
        graph.parse(tfd, format='turtle')
    except urllib.error.HTTPError:
        pass
    return graph


def _compare_iterations(graph_old, graph_new, ignore_BNode=True):
    '''compare old and new iterations of a graph
    returns added, removed, changed sets of concepts'''
    old = set(s for s in graph_old.subjects(None, None))
    new = set(s for s in graph_new.subjects(None, None))
    # added: things in new set that are not in old set
    added = new - old
    # removed: things in old set that are not in new set
    removed = old - new
    if ignore_BNode:
        # ignore changes in BNodes
        added = [n for n in added if type(n) is not BNode]
        removed = [n for n in removed if type(n) is not BNode]
    return added, removed


def _print_stats(added, removed):
    '''print statistics and information about terms
    will output added terms, removed terms'''
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


def _retrieve_and_compare(NAME, MODULES=None):
    '''Will retrieve old version from GitHub and compare new version'''
    print(f'\n--- {NAME} --- ')
    if MODULES is None:
        MODULES = [NAME.lower()]
    var_github_raw = globals()[f"GITHUB_{NAME.replace('-','_')}_RAW"]
    var_local = globals()[f"LOCAL_{NAME.replace('-','_')}"]
    for module in MODULES:
        print(f'MODULE: {module}')
        old = _download_file_to_rdf_graph(f'{var_github_raw}{module}.ttl')
        new = Graph()
        new.parse(f'{var_local}{module}.ttl', format='turtle')
        added, removed = _compare_iterations(old, new)
        _print_stats(added, removed)

_retrieve_and_compare('DPV', MODULES=DPV_MODULES)
_retrieve_and_compare('DPV-GDPR', MODULES=DPV_GDPR_MODULES)
_retrieve_and_compare('DPV-PD')
_retrieve_and_compare('DPV-LEGAL', MODULES=DPV_LEGAL_MODULES)
_retrieve_and_compare('DPV-TECH')
_retrieve_and_compare('RISK', MODULES=RISK_MODULES)
_retrieve_and_compare('RIGHTS-EU', MODULES=RIGHTS_MODULES)