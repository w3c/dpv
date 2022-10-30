#!/usr/bin/env python3
#author: Harshvardhan J. Pandit 

'''Generates Examples documentation for DPV'''

# Vocabulary is stored in /dpv/examples/vocab.ttl
# Examples are stored in /dpv/examples/examples.ttl

from rdflib import Graph, Namespace
from rdflib import RDF, RDFS, OWL
from rdflib.term import Literal, URIRef, BNode
from rdform import DataGraph, RDFS_Resource

from collections import namedtuple

import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug

from vocab_management import *

IMPORT_CSV_PATH = 'vocab_csv'
EXPORT_DEX_PATH = '../examples'
MAPPINGS = {}
TEMPLATE_DATA = { 'mappings': MAPPINGS }

g = Graph()
for prefix, namespace in NAMESPACES.items():
    g.namespace_manager.bind(prefix, namespace)
import csv
CSVHEAD = namedtuple('CSVHEAD', 
    ('uid', 'title', 'desc', 'source', 
    'subject', 'ref', 'embed', 'date', 'contributor'))


def extract_terms_from_csv(filepath, Mapping):
    '''extracts data from file.csv and creates instances of Class
    returns list of Mapping-defined instances'''
    # this is a hack to get parseable number of fields from CSV
    # it relies on the internal data structure of a namedtuple
    attributes = Mapping.__dict__
    attributes = len(attributes['_fields'])
    with open(filepath) as fd:
        csvreader = csv.reader(fd)
        next(csvreader)
        terms = []
        for row in csvreader:
            # skip empty rows
            if not row[0].strip():
                continue
            # extract required amount of terms, ignore any field after that
            row = [term.strip() for term in row[:attributes]]
            # create instance of required class
            terms.append(Mapping(*row))

    return terms


def add_common_annotations(g, term):
    DEBUG(f'Adding Example#{term.uid}')
    g.add((DEX[term.uid], DCT.identifier, Literal(term.uid)))
    g.add((DEX[term.uid], DCT.title, Literal(term.title)))
    g.add((DEX[term.uid], DCT.description, Literal(term.desc)))
    if term.source:
        if not term.source.startswith('http'):
            source = f'https://w3id.org/dpv/examples/{term.source}'
        else:
            source = term.source
        g.add((DEX[term.uid], DCT.source, Literal(source)))
    if term.ref:
        for ref in term.ref.split(','):
            g.add((DEX[term.uid], DCT.references, DEX[ref]))
            g.add((DEX[ref], DCT.references, DEX[term.uid]))
    if term.subject:
        for subject in term.subject.split(','):
            prefix, subject = subject.split(':')
            subject = NAMESPACES[prefix][f'{subject}']
            g.add((DEX[term.uid], DCT.subject, URIRef(subject)))
            if subject not in MAPPINGS:
                MAPPINGS[subject] = []
            MAPPINGS[subject].append((term.uid, term.title))
    if term.embed == 'Y':
        g.add((DEX[term.uid], DEX.isEmbedded, Literal(True)))
    else:
        g.add((DEX[term.uid], DEX.isEmbedded, Literal(False)))
    if term.date:
        g.add((DEX[term.uid], DCT.date, Literal(term.date)))
    if term.contributor:
        g.add((DEX[term.uid], DCT.contributor, Literal(term.contributor)))

# Examples
terms = extract_terms_from_csv(f'{IMPORT_CSV_PATH}/Example.csv', CSVHEAD)
for term in terms:
    g.add((DEX[term.uid], RDF.type, DEX['Example']))
    add_common_annotations(g, term)        


def prefix_this(item):
    # DEBUG(f'item: {item} type: {type(item)}')
    if type(item) is RDFS_Resource:
        item = item.iri
    elif type(item) is URIRef:
        item = str(item)
    if type(item) is str and item.startswith('http'):
        iri = URIRef(item).n3(G.graph.namespace_manager)
    else:
        iri = item
    if iri.count('_') > 0:
        iri = iri.split('_', 1)[1]
    # DEBUG(f'prefixed {item} to: {iri}')
    return iri


def retrieve_source(path):
    if not path.startswith('https://w3id.org/dpv/examples/'):
        raise Exception(f'Examples path {path} is not supported')
        return
    path = path.replace('https://w3id.org/dpv', '..')
    with open(path, 'r') as fd:
        contents = fd.read()
    return contents


g.serialize(f'{EXPORT_DEX_PATH}/examples.ttl', format='ttl')
G = DataGraph()
G.parse(g)
G.graph.ns = { k:v for k,v in G.graph.namespaces() }

# UseCases
TEMPLATE_DATA['examples'] = {}
for dex in G.get_instances_of('dex_Example'):
    TEMPLATE_DATA['examples'][dex.dct_identifier] = dex

# substitute constructed objects back as list for easier iteration
TEMPLATE_DATA['examples'] = sorted(
    TEMPLATE_DATA['examples'].values(), key=lambda x: x.dct_identifier)

# JINJA2 for templating and generating HTML
from jinja2 import FileSystemLoader, Environment
JINJA2_FILTERS = {
    'generate_author_affiliation': generate_author_affiliation,
    'prefix_this': prefix_this,
    'retrieve_source': retrieve_source,
}

template_loader = FileSystemLoader(searchpath='./jinja2_resources')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)
template_env.filters.update(JINJA2_FILTERS)

template = template_env.get_template('template_examples.jinja2')
with open(f'{EXPORT_DEX_PATH}/index.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DEX document at f{EXPORT_DEX_PATH}/index.html')
with open(f'{EXPORT_DEX_PATH}/examples.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DEX document at f{EXPORT_DEX_PATH}/examples.html')
