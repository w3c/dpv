#!/usr/bin/env python3
#author: Harshvardhan J. Pandit 

'''Generates Use-case and Requirements documentation for DPV'''

# Vocabulary is stored in /dpv/use-cases/vocab.ttl
# Use-cases are stored in /dpv/use-cases/use-cases.ttl
# Requirements are stored in /dpv/use-cases/requirements.ttl

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
EXPORT_UCR_PATH = '../use-cases'
MAPPINGS = {}
TEMPLATE_DATA = { 'mappings': MAPPINGS }

g = Graph()
for prefix, namespace in NAMESPACES.items():
    g.namespace_manager.bind(prefix, namespace)
import csv
CSVHEAD = namedtuple('CSVHEAD', 
    ('uid', 'title', 'desc', 'source', 
    'subject', 'ref', 'date', 'contributor'))


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
    DEBUG(term.uid)
    g.add((UCR[term.uid], DCT.identifier, Literal(term.uid)))
    g.add((UCR[term.uid], DCT.title, Literal(term.title)))
    g.add((UCR[term.uid], DCT.description, Literal(term.desc)))
    # if term.source:
    #     g.add((UCR[term], DCT.source, Literal(term.source)))
    if term.ref:
        for ref in term.ref.split(','):
            g.add((UCR[term.uid], DCT.references, UCR[ref]))
            g.add((UCR[ref], DCT.references, UCR[term.uid]))
    if term.subject:
        for subject in term.subject.split(','):
            prefix, subject = subject.split(':')
            subject = NAMESPACES[prefix][f'{subject}']
            g.add((UCR[term.uid], DCT.subject, URIRef(subject)))
            if subject not in MAPPINGS:
                MAPPINGS[subject] = { 'usecases': [], 'requirements': [] }
            if term.uid.startswith('U'):
                MAPPINGS[subject]['usecases'].append(term.uid)
            elif term.uid.startswith('R'):
                MAPPINGS[subject]['requirements'].append(term.uid)
    if term.date:
        g.add((UCR[term.uid], DCT.date, Literal(date)))
    if term.contributor:
        g.add((UCR[term.uid], DCT.contributor, Literal(term.contributor)))

# UseCases
terms = extract_terms_from_csv(f'{IMPORT_CSV_PATH}/UseCase.csv', CSVHEAD)
for term in terms:
    g.add((UCR[term.uid], RDF.type, UCR['UseCase']))
    add_common_annotations(g, term)        

# Requirements
terms = extract_terms_from_csv(f'{IMPORT_CSV_PATH}/Requirement.csv', CSVHEAD)
for term in terms:
    g.add((UCR[term.uid], RDF.type, UCR['Requirement']))
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


g.serialize(f'{EXPORT_UCR_PATH}/ucr.ttl', format='ttl')
G = DataGraph()
G.parse(g)
G.graph.ns = { k:v for k,v in G.graph.namespaces() }

# UseCases
TEMPLATE_DATA['usecases'] = {}
for uc in G.get_instances_of('ucr_UseCase'):
    TEMPLATE_DATA['usecases'][uc.dct_identifier] = uc

# Requirements
TEMPLATE_DATA['requirements'] = {}
for req in G.get_instances_of('ucr_Requirement'):
    TEMPLATE_DATA['requirements'][req.dct_identifier] = req

# substitute constructed objects back as list for easier iteration
TEMPLATE_DATA['usecases'] = sorted(
    TEMPLATE_DATA['usecases'].values(), key=lambda x: x.dct_identifier)
TEMPLATE_DATA['requirements'] = sorted(
    TEMPLATE_DATA['requirements'].values(), key=lambda x: x.dct_identifier)

# JINJA2 for templating and generating HTML
from jinja2 import FileSystemLoader, Environment
JINJA2_FILTERS = {
    'generate_author_affiliation': generate_author_affiliation,
    'prefix_this': prefix_this,
}

template_loader = FileSystemLoader(searchpath='./jinja2_resources')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)
template_env.filters.update(JINJA2_FILTERS)

template = template_env.get_template('template_ucr.jinja2')
with open(f'{EXPORT_UCR_PATH}/index.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote UCR document at f{EXPORT_UCR_PATH}/index.html')
with open(f'{EXPORT_UCR_PATH}/ucr.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote UCR document at f{EXPORT_UCR_PATH}/ucr.html')
