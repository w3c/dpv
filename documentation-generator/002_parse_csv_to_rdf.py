#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''Take CSV and generate RDF from it'''

########################################
# How to read and understand this file #
# 1. Start from the end of the file
# 2. This script reads CSV files explicitly declared
# 3. It generates RDF terms using rdflib for Classes and Properties
# 4. It writes those terms to a file - one per each module
# 5. It combines all written files into dpv.ttl and dpv-gdpr.ttl

# This script assumes the input if well structured and formatted
# If it isn't, the 'erors' may silently propogate

# CSV FILES are in IMPORT_CSV_PATH
# RDF FILES are written to EXPORT_DPV_MODULE_PATH
########################################

IMPORT_CSV_PATH = './vocab_csv'
EXPORT_DPV_PATH = '../dpv'
EXPORT_DPV_MODULE_PATH = '../dpv/rdf'
EXPORT_DPV_GDPR_PATH = '../dpv-gdpr'
EXPORT_DPV_GDPR_MODULE_PATH = '../dpv-gdpr/rdf'

# serializations in the form of extention: rdflib name
RDF_SERIALIZATIONS = {
    'rdf': 'xml', 
    'ttl': 'turtle', 
    'n3': 'n3',
    'jsonld': 'json-ld'
    }

VOCAB_TERM_ACCEPT = ('accepted', 'changed')
VOCAB_TERM_REJECT = ('deprecated', 'removed')

import csv
from collections import namedtuple

from rdflib import Graph, Namespace
from rdflib.compare import graph_diff
from rdflib.namespace import XSD
from rdflib import RDF, RDFS, OWL
from rdflib.term import Literal, URIRef, BNode

import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

DCT = Namespace('http://purl.org/dc/terms/')
DPV = Namespace('http://www.w3.org/ns/dpv#')
DPV_GDPR = Namespace('http://www.w3.org/ns/dpv-gdpr#')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
ODRL = Namespace('http://www.w3.org/ns/odrl/2/')
PROV = Namespace('http://www.w3.org/ns/prov#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SPL = Namespace('http://www.specialprivacy.eu/langs/usage-policy#')
SVD = Namespace('http://www.specialprivacy.eu/vocabs/data#')
SVDU = Namespace('http://www.specialprivacy.eu/vocabs/duration#')
SVL = Namespace('http://www.specialprivacy.eu/vocabs/locations#')
SVPR = Namespace('http://www.specialprivacy.eu/vocabs/processing#')
SVPU = Namespace('http://www.specialprivacy.eu/vocabs/purposes#')
SVR = Namespace('http://www.specialprivacy.eu/vocabs/recipients')
SW = Namespace('http://www.w3.org/2003/06/sw-vocab-status/ns#')
TIME = Namespace('http://www.w3.org/2006/time#')

# The dpv namespace is the default base for all terms
# Later, this is changed to write terms under DPV-GDPR namespace
BASE = DPV

NAMESPACES = {
    'dct': DCT,
    'dpv': DPV,
    'dpv-gdpr': DPV_GDPR,
    'foaf': FOAF,
    'odrl': ODRL,
    'owl': OWL,
    'prov': PROV,
    'rdf': RDF,
    'rdfs': RDFS,
    'skos': SKOS,
    'spl': SPL,
    'svd': SVD,
    'svdu': SVDU,
    'svl': SVL,
    'svpr': SVPR,
    'svpu': SVPU,
    'svr': SVR,
    'sw': SW,
    'time': TIME,
    'xsd': XSD,
}

# the field labels are based on what they should be translated to

DPV_Class = namedtuple('DPV_Class', [
    'term', 'rdfs_label', 'dct_description', 'rdfs_subclassof', 
    'rdfs_seealso', 'relation', 'rdfs_comment', 'rdfs_isdefinedby', 
    'dct_created', 'dct_modified', 'sw_termstatus', 'dct_creator', 
    'resolution'])

DPV_Property = namedtuple('DPV_Property', [
    'term', 'rdfs_label', 'dct_description', 
    'rdfs_domain', 'rdfs_range', 'rdfs_subpropertyof',
    'rdfs_seealso', 'relation', 'rdfs_comment', 'rdfs_isdefinedby', 
    'dct_created', 'dct_modified', 'sw_termstatus', 'dct_creator', 
    'resolution'])

LINKS = {}


def extract_terms_from_csv(filepath, Class):
    '''extracts data from file.csv and creates instances of Class
    returns list of Class instances'''
    # this is a hack to get parseable number of fields from CSV
    # it relies on the internal data structure of a namedtuple
    attributes = Class.__dict__
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
            terms.append(Class(*row))

    return terms


def add_common_triples_for_all_terms(term, graph):
    '''Adds triples for any term to graph
    Common triples are those shared by Class and Property
    terms: data structure of term; is object with attributes
    graph: rdflib graph
    returns: None'''

    # rdfs:label
    graph.add((BASE[f'{term.term}'], RDFS.label, Literal(term.rdfs_label, lang='en')))
    # dct:description
    graph.add((BASE[f'{term.term}'], DCT.description, Literal(term.dct_description, lang='en')))
    # rdfs:seeAlso
    # TODO: use relation field for relevant terms
    # currently this considers all terms that are related to use rdfs:seeAlso
    # the next column contains the relation, parse and use that
    if term.rdfs_seealso:
        links = [l.strip() for l in term.rdfs_seealso.split(',')]
        for link in links:
            if link.startswith('http'):
                graph.add((BASE[f'{term.term}'], RDFS.seeAlso, URIRef(link)))
            elif ':' in link:
                # assuming something like rdfs:Resource
                prefix, label = link.split(':')
                # gets the namespace from registered ones and create URI
                # will throw an error if namespace is not registered
                # dpv internal terms are expected to have the prefix i.e. dpv:term
                link = NAMESPACES[prefix][f'{label}']
                graph.add((BASE[f'{term.term}'], RDFS.seeAlso, link))
            else:
                graph.add((BASE[f'{term.term}'], RDFS.seeAlso, Literal(link, datatype=XSD.string)))
    # rdfs:comment
    if term.rdfs_comment:
        graph.add((BASE[f'{term.term}'], RDFS.comment, Literal(term.rdfs_comment, lang='en')))
    # rdfs:isDefinedBy
    if term.rdfs_isdefinedby:
        links = [l.strip() for l in term.rdfs_isdefinedby.replace('(','').replace(')','').split(',')]
        link_iterator = iter(links)
        for label in link_iterator:
            link = next(link_iterator)
            # add link to a temp file so that the label can be displayed in HTML
            if not link in LINKS:
                LINKS[link] = label
            # add link to graph
            if link.startswith('http'):
                graph.add((BASE[f'{term.term}'], RDFS.isDefinedBy, URIRef(link)))
            else:
                graph.add((BASE[f'{term.term}'], RDFS.isDefinedBy, Literal(link, datatype=XSD.string)))
    # dct:created
    graph.add((BASE[f'{term.term}'], DCT.created, Literal(term.dct_created, datatype=XSD.date)))
    # dct:modified
    if term.dct_modified:
        graph.add((BASE[f'{term.term}'], DCT.modified, Literal(term.dct_modified, datatype=XSD.date)))
    # sw:term_status
    graph.add((BASE[f'{term.term}'], SW.term_status, Literal(term.sw_termstatus, lang='en')))
    # dct:creator
    if term.dct_creator:
        authors = [a.strip() for a in term.dct_creator.split(',')]
        for author in authors:
            graph.add((BASE[f'{term.term}'], DCT.creator, Literal(author, datatype=XSD.string)))
    # resolution
        # do nothing

    return None


def add_triples_for_classes(classes, graph):
    '''Adds triples for classes to graph
    classes: list of CSV data rows
    graph: rdflib graph
    returns: None'''

    for cls in classes:
        # only add accepted classes
        if cls.sw_termstatus not in VOCAB_TERM_ACCEPT:
            continue
        # rdf:type
        graph.add((BASE[f'{cls.term}'], RDF.type, RDFS.Class))
        # rdfs:subClassOf
        if cls.rdfs_subclassof:
            parents = [p.strip() for p in cls.rdfs_subclassof.split(',')]
            for parent in parents:
                if parent.startswith('http'):
                    graph.add((BASE[f'{cls.term}'], RDFS.subClassOf, URIRef(parent)))
                elif ':' in parent:
                    # assuming something like rdfs:Resource
                    prefix, term = parent.split(':')
                    # gets the namespace from registered ones and create URI
                    # will throw an error if namespace is not registered
                    # dpv internal terms are expected to have the prefix i.e. dpv:term
                    parent = NAMESPACES[prefix][f'{term}']
                    graph.add((BASE[f'{cls.term}'], RDFS.subClassOf, parent))
                else:
                    graph.add((BASE[f'{cls.term}'], RDFS.subClassOf, Literal(parent, datatype=XSD.string)))
        
        add_common_triples_for_all_terms(cls, graph)

    return None
        

def add_triples_for_properties(properties, graph):
    '''Adds triples for properties to graph
    properties: list of CSV data rows
    graph: rdflib graph
    returns: None'''

    for prop in properties:
        # only record accepted classes
        if prop.sw_termstatus not in VOCAB_TERM_ACCEPT:
            continue
        # rdf:type
        graph.add((BASE[f'{prop.term}'], RDF.type, RDF.Property))
        # rdfs:domain
        if prop.rdfs_domain:
            # assuming something like rdfs:Resource
            prefix, label = prop.rdfs_domain.split(':')
            # gets the namespace from registered ones and create URI
            # will throw an error if namespace is not registered
            # dpv internal terms are expected to have the prefix i.e. dpv:term
            link = NAMESPACES[prefix][f'{label}']
            graph.add((BASE[f'{prop.term}'], RDFS.domain, link))
        # rdfs:range
        if prop.rdfs_range:
            # assuming something like rdfs:Resource
            prefix, label = prop.rdfs_range.split(':')
            # gets the namespace from registered ones and create URI
            # will throw an error if namespace is not registered
            # dpv internal terms are expected to have the prefix i.e. dpv:term
            link = NAMESPACES[prefix][f'{label}']
            graph.add((BASE[f'{prop.term}'], RDFS.range, link))
        # rdfs:subPropertyOf
        if prop.rdfs_subpropertyof:
            parents = [p.strip() for p in prop.rdfs_subpropertyof.split(',')]
            for parent in parents:
                if parent.startswith('http'):
                    graph.add((BASE[f'{prop.term}'], RDFS.subPropertyOf, URIRef(parent)))
                elif ':' in parent:
                    # assuming something like rdfs:Resource
                    prefix, term = parent.split(':')
                    # gets the namespace from registered ones and create URI
                    # will throw an error if namespace is not registered
                    # dpv internal terms are expected to have the prefix i.e. dpv:term
                    parent = NAMESPACES[prefix][f'{term}']
                    graph.add((BASE[f'{prop.term}'], RDFS.subPropertyOf, parent))
                else:
                    graph.add((BASE[f'{prop.term}'], RDFS.subPropertyOf, Literal(parent, datatype=XSD.string)))
        add_common_triples_for_all_terms(prop, graph)


def serialize_graph(graph, filepath):
    '''serializes given graph at filepath with defined formats'''
    for ext, format in RDF_SERIALIZATIONS.items():
        graph.serialize(f'{filepath}.{ext}', format=format)
        INFO(f'wrote {filepath}.{ext}')


# #############################################################################

# DPV #

DPV_CSV_FILES = {
    'base': {
        'classes': f'{IMPORT_CSV_PATH}/BaseOntology.csv',
        'properties': f'{IMPORT_CSV_PATH}/BaseOntology_properties.csv',
        },
    'personal_data_categories': {
        'classes': f'{IMPORT_CSV_PATH}/PersonalDataCategory.csv',
        },
    'purposes': {
        'classes': f'{IMPORT_CSV_PATH}/Purpose.csv',
        'properties': f'{IMPORT_CSV_PATH}/Purpose_properties.csv',
        },
    'processing': {
        'classes': f'{IMPORT_CSV_PATH}/Processing.csv',
        'properties': f'{IMPORT_CSV_PATH}/Processing_properties.csv',
        },
    'technical_organisational_measures': {
        'classes': f'{IMPORT_CSV_PATH}/TechnicalOrganisationalMeasure.csv',
        'properties': f'{IMPORT_CSV_PATH}/TechnicalOrganisationalMeasure_properties.csv',
        },
    'entities': {
        'classes': f'{IMPORT_CSV_PATH}/Entities.csv',
        'properties': f'{IMPORT_CSV_PATH}/Entities_properties.csv'
        },
    'legal_basis': {
        'classes': f'{IMPORT_CSV_PATH}/LegalBasis.csv',
    },
    'consent': {
        # 'classes': f'{IMPORT_CSV_PATH}/Consent.csv',
        'properties': f'{IMPORT_CSV_PATH}/Consent_properties.csv',
        },
    }

# this graph will get written to dpv.ttl
DPV_GRAPH = Graph()

for name, module in DPV_CSV_FILES.items():
    graph = Graph()
    for prefix, namespace in NAMESPACES.items():
        graph.namespace_manager.bind(prefix, namespace)
    if 'classes' in module:
        classes = extract_terms_from_csv(module['classes'], DPV_Class)
        DEBUG(f'there are {len(classes)} classes in {name}')
        add_triples_for_classes(classes, graph)
    if 'properties' in module:
        properties = extract_terms_from_csv(module['properties'], DPV_Property)
        DEBUG(f'there are {len(properties)} properties in {name}')
        add_triples_for_properties(properties, graph)
    serialize_graph(graph, f'{EXPORT_DPV_MODULE_PATH}/{name}')
    DPV_GRAPH += graph

# add information about ontology
# this is assumed to be in file dpv-ontology-metadata.ttl
graph = Graph()
graph.load('dpv-ontology-metadata.ttl', format='turtle')
DPV_GRAPH += graph

for prefix, namespace in NAMESPACES.items():
        DPV_GRAPH.namespace_manager.bind(prefix, namespace)
serialize_graph(DPV_GRAPH, f'{EXPORT_DPV_PATH}/dpv')

# DPV-GDPR #
# dpv-gdpr is the exact same as dpv in terms of requirements and structure
# except that the namespace is different
# so instead of rewriting the entire code again for dpv-gdpr,
# here I become lazy and instead change the DPV namespace to DPV-GDPR

BASE = NAMESPACES['dpv-gdpr']

DPV_GDPR_GRAPH = Graph()

DPV_GDPR_CSV_FILES = {
    'legal_basis': {
        'classes': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis.csv',
        },
    'rights': {
        'classes': f'{IMPORT_CSV_PATH}/GDPR_LegalRights.csv',
        },
    'data_transfers': {
        'classes': f'{IMPORT_CSV_PATH}/GDPR_DataTransfers.csv',
        },
    }

for name, module in DPV_GDPR_CSV_FILES.items():
    graph = Graph()
    for prefix, namespace in NAMESPACES.items():
        graph.namespace_manager.bind(prefix, namespace)
    if 'classes' in module:
        classes = extract_terms_from_csv(module['classes'], DPV_Class)
        DEBUG(f'there are {len(classes)} classes in {name}')
        add_triples_for_classes(classes, graph)
    if 'properties' in module:
        properties = extract_terms_from_csv(module['properties'], DPV_Property)
        DEBUG(f'there are {len(properties)} properties in {name}')
        add_triples_for_properties(properties, graph)
    serialize_graph(graph, f'{EXPORT_DPV_GDPR_MODULE_PATH}/{name}')
    DPV_GDPR_GRAPH += graph

graph = Graph()
graph.load('dpv-gdpr-ontology-metadata.ttl', format='turtle')
DPV_GDPR_GRAPH += graph

for prefix, namespace in NAMESPACES.items():
    DPV_GDPR_GRAPH.namespace_manager.bind(prefix, namespace)
serialize_graph(DPV_GDPR_GRAPH, f'{EXPORT_DPV_GDPR_PATH}/dpv-gdpr')

# #############################################################################

# Save collected links as resource for generating HTML A HREF in JINJA2 templates
# file is in jinja2_resources/links_labels.json

import json
with open('jinja2_resources/links_label.json', 'w') as fd:
    fd.write(json.dumps(LINKS))