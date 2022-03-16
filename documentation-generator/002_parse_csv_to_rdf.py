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
EXPORT_DPV_MODULE_PATH = '../dpv/modules'
EXPORT_DPV_GDPR_PATH = '../dpv-gdpr'
EXPORT_DPV_GDPR_MODULE_PATH = '../dpv-gdpr/modules'
EXPORT_DPV_PD_PATH = '../dpv-pd'

# serializations in the form of extention: rdflib name
RDF_SERIALIZATIONS = {
    'rdf': 'xml', 
    'ttl': 'turtle', 
    'n3': 'n3',
    'jsonld': 'json-ld'
    }

VOCAB_TERM_ACCEPT = ('accepted', 'changed', 'modified')
VOCAB_TERM_REJECT = ('deprecated', 'removed')

import csv
from collections import namedtuple
import json

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

# Namespaces are in two files: 
# 1. Namespaces.csv for DPV issued namespaces
# 2. Namespaces_other for External namespaces

DCT = Namespace('http://purl.org/dc/terms/')
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

DPV = Namespace('https://w3id.org/dpv#')
DPV_NACE = Namespace('https://w3id.org/dpv/nace#')
DPV_GDPR = Namespace('https://w3id.org/dpv/gdpr#')
DPV_PD = Namespace('https://w3id.org/dpv/pd#')
DPVS = Namespace('https://w3id.org/dpv/dpv-skos#')
DPVS_GDPR = Namespace('https://w3id.org/dpv/dpv-skos/gdpr#')
DPVS_PD = Namespace('https://w3id.org/dpv/dpv-skos/pd#')
DPVO = Namespace('https://w3id.org/dpv/dpv-owl#')
DPVO_GDPR = Namespace('https://w3id.org/dpv/dpv-owl/gdpr#')
DPVO_PD = Namespace('https://w3id.org/dpv/dpv-owl/pd#')

# The dpv namespace is the default base for all terms
# Later, this is changed to write terms under DPV-GDPR namespace
BASE = DPV

NAMESPACES = {
    'dct': DCT,
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
    # DPV
    'dpv': DPV,
    'dpv-nace': DPV_NACE,
    'dpv-gdpr': DPV_GDPR,
    'dpv-pd': DPV_PD,
    'dpvs': DPVS,
    'dpvs-gdpr': DPVS_GDPR,
    'dpvs-pd': DPVS_PD,
    'dpvo': DPVO,
    'dpvo-gdpr': DPVO_GDPR,
    'dpvo-pd': DPVO_PD,
}

# the field labels are based on what they should be translated to

DPV_Class = namedtuple('DPV_Class', [
            'term', 'skos_prefLabel', 'skos_definition', 'dpv_isSubTypeOf', 
            'skos_related', 'relation', 'skos_note', 'skos_scopeNote', 
            'dct_created', 'dct_modified', 'sw_termstatus', 'dct_creator', 
            'resolution'])
DPV_Property = namedtuple('DPV_Property', [
            'term', 'skos_prefLabel', 'skos_definition', 
            'rdfs_domain', 'rdfs_range', 'rdfs_subpropertyof',
            'skos_related', 'relation', 'skos_note', 'skos_scopeNote', 
            'dct_created', 'dct_modified', 'sw_termstatus', 'dct_creator', 
            'resolution'])

LINKS = {}


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


def add_common_triples_for_all_terms(term, graph):
    '''Adds triples for any term to graph
    Common triples are those shared by Class and Property
    terms: data structure of term; is object with attributes
    graph: rdflib graph
    returns: None'''

    graph.add((BASE[f'{term.term}'], RDF.type, SKOS.Concept))
    # rdfs:label
    graph.add((BASE[f'{term.term}'], SKOS.prefLabel, Literal(term.skos_prefLabel, lang='en')))
    # dct:description
    graph.add((BASE[f'{term.term}'], SKOS.definition, Literal(term.skos_definition, lang='en')))
    # rdfs:seeAlso
    if term.skos_related:
        links = [l.strip() for l in term.skos_related.split(',')]
        for link in links:
            if link.startswith('http'):
                graph.add((BASE[f'{term.term}'], SKOS.related, URIRef(link)))
            elif ':' in link:
                # assuming something like rdfs:Resource
                prefix, label = link.split(':')
                # gets the namespace from registered ones and create URI
                # will throw an error if namespace is not registered
                # dpv internal terms are expected to have the prefix i.e. dpv:term
                link = NAMESPACES[prefix][f'{label}']
                graph.add((BASE[f'{term.term}'], SKOS.related, link))
            else:
                graph.add((BASE[f'{term.term}'], SKOS.related, Literal(link, datatype=XSD.string)))
    # rdfs:comment
    if term.skos_note:
        graph.add((BASE[f'{term.term}'], SKOS.note, Literal(term.skos_note, lang='en')))
    # rdfs:isDefinedBy
    if term.skos_scopeNote:
        links = [l.strip() for l in term.skos_scopeNote.replace('(','').replace(')','').split(',')]
        link_iterator = iter(links)
        for label in link_iterator:
            link = next(link_iterator)
            # add link to a temp file so that the label can be displayed in HTML
            if not link in LINKS:
                LINKS[link] = label
            # add link to graph
            if link.startswith('http'):
                graph.add((BASE[f'{term.term}'], DCT.source, URIRef(link)))
            else:
                graph.add((BASE[f'{term.term}'], DCT.source, Literal(link, datatype=XSD.string)))
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
    # is defined by this vocabulary
    graph.add((BASE[f'{term.term}'], RDFS.isDefinedBy, BASE['']))
    # resolution
        # do nothing

    return None


def add_triples_for_classes(classes, graph):
    '''Adds triples for classes to graph
    classes: list of CSV data rows
    graph: rdflib graph
    returns: None'''

    proposed = []
    for cls in classes:
        # only add accepted classes
        if cls.sw_termstatus not in VOCAB_TERM_ACCEPT:
            if cls.sw_termstatus == 'proposed':
                proposed.append(cls.term)
            continue
        # rdf:type
        DEBUG(cls.term)
        graph.add((BASE[f'{cls.term}'], RDF.type, DPV.Concept))
        # rdfs:subClassOf
        if cls.dpv_isSubTypeOf:
            parents = [p.strip() for p in cls.dpv_isSubTypeOf.split(',')]
            for parent in parents:
                if parent.startswith('http'):
                    graph.add((BASE[f'{cls.term}'], DPV.isSubTypeOf, URIRef(parent)))
                elif ':' in parent:
                    if parent == "dpv:Concept":
                        continue
                    # assuming something like rdfs:Resource
                    prefix, term = parent.split(':')
                    prefix = prefix.replace("sc__", "")
                    # gets the namespace from registered ones and create URI
                    # will throw an error if namespace is not registered
                    # dpv internal terms are expected to have the prefix i.e. dpv:term
                    parent = NAMESPACES[prefix][f'{term}']
                    graph.add((BASE[f'{cls.term}'], DPV.isSubTypeOf, parent))
                else:
                    graph.add((BASE[f'{cls.term}'], DPV.isSubTypeOf, Literal(parent, datatype=XSD.string)))
        
        add_common_triples_for_all_terms(cls, graph)

    return proposed
        

def add_triples_for_properties(properties, graph):
    '''Adds triples for properties to graph
    properties: list of CSV data rows
    graph: rdflib graph
    returns: None'''

    proposed = []
    for prop in properties:
        # only record accepted classes
        if prop.sw_termstatus not in VOCAB_TERM_ACCEPT:
            if prop.sw_termstatus == 'proposed':
                proposed.append(prop.term)
            continue
        # rdf:type
        DEBUG(prop.term)
        graph.add((BASE[f'{prop.term}'], RDF.type, DPV.Relation))
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
                    if parent == "dpv:Relation":
                        continue
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

    return proposed


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
        'model': 'vocabulary',
        },
    'personal_data': {
        'classes': f'{IMPORT_CSV_PATH}/PersonalData.csv',
        'properties': f'{IMPORT_CSV_PATH}/PersonalData_properties.csv',
        'model': 'ontology',
        'topconcept': DPV.PersonalData,
        },
    'purposes': {
        'classes': f'{IMPORT_CSV_PATH}/Purpose.csv',
        'properties': f'{IMPORT_CSV_PATH}/Purpose_properties.csv',
        'model': 'taxonomy',
        'topconcept': DPV.Purpose,
        },
    'context': {
        'classes': f'{IMPORT_CSV_PATH}/Context.csv',
        'properties': f'{IMPORT_CSV_PATH}/Context_properties.csv',
        'model': 'taxonomy',
        'topconcept': DPV.Context,
        },
    'processing': {
        'classes': f'{IMPORT_CSV_PATH}/Processing.csv',
        'properties': f'{IMPORT_CSV_PATH}/Processing_properties.csv',
        'model': 'taxonomy',
        'topconcept': DPV.Processing,
        },
    'processing_context': {
        'classes': f'{IMPORT_CSV_PATH}/ProcessingContext.csv',
        'properties': f'{IMPORT_CSV_PATH}/ProcessingContext_properties.csv',
        'model': 'taxonomy',
        },
    'technical_organisational_measures': {
        'classes': f'{IMPORT_CSV_PATH}/TechnicalOrganisationalMeasure.csv',
        'properties': f'{IMPORT_CSV_PATH}/TechnicalOrganisationalMeasure_properties.csv',
        'model': 'taxonomy',
        'topconcept': DPV.TechnicalOrganisationalMeasure,
        },
    'entities': {
        'classes': f'{IMPORT_CSV_PATH}/Entities.csv',
        'properties': f'{IMPORT_CSV_PATH}/Entities_properties.csv',
        'model': 'ontology',
        'topconcept': DPV.Entity,
        },
    'jurisdictions': {
        'classes': f'{IMPORT_CSV_PATH}/Jurisdictions.csv',
        'properties': f'{IMPORT_CSV_PATH}/Jurisdictions_properties.csv',
        'model': 'ontology',
        },
    'legal_basis': {
        'classes': f'{IMPORT_CSV_PATH}/LegalBasis.csv',
        'properties': f'{IMPORT_CSV_PATH}/LegalBasis_properties.csv',
        'model': 'taxonomy',
        'topconcept': DPV.LegalBasis,
    },
    'consent': {
        # 'classes': f'{IMPORT_CSV_PATH}/Consent.csv',
        'properties': f'{IMPORT_CSV_PATH}/Consent_properties.csv',
        },
    }

# this graph will get written to dpv.ttl
DPV_GRAPH = Graph()
DPV_GRAPH.add((BASE[''], RDF.type, SKOS.ConceptScheme))
proposed_terms = {}
for name, module in DPV_CSV_FILES.items():
    graph = Graph()
    proposed = []
    DEBUG('------')
    DEBUG(f'Processing {name} module')
    for prefix, namespace in NAMESPACES.items():
        graph.namespace_manager.bind(prefix, namespace)
    if 'classes' in module:
        classes = extract_terms_from_csv(module['classes'], DPV_Class)
        DEBUG(f'there are {len(classes)} classes in {name}')
        returnval = add_triples_for_classes(classes, graph)
        if returnval:
            proposed.extend(returnval)
    if 'properties' in module:
        properties = extract_terms_from_csv(module['properties'], DPV_Property)
        DEBUG(f'there are {len(properties)} properties in {name}')
        returnval = add_triples_for_properties(properties, graph)
        if returnval:
            proposed.extend(returnval)
    if proposed:
        proposed_terms[name] = proposed
    # add collection representing concepts
    graph.add((BASE[f'{name.title()}Concepts'], RDF.type, SKOS.Collection))
    graph.add((BASE[f'{name.title()}Concepts'], DCT.title, Literal(f'{name.title()} Concepts', datatype=XSD.string)))
    for concept, _, _ in graph.triples((None, RDF.type, SKOS.Concept)):
        graph.add((BASE[f'{name.title()}Concepts'], SKOS.member, concept))
        DPV_GRAPH.add((concept, SKOS.inScheme, DPV['']))
    # serialize
    graph.load('ontology_metadata/dpv-semantics.ttl', format='turtle')
    serialize_graph(graph, f'{EXPORT_DPV_MODULE_PATH}/{name}')
    if 'topconcept' in module:
        DPV_GRAPH.add((BASE[''], SKOS.hasTopConcept, module['topconcept']))
    DPV_GRAPH += graph

if proposed_terms:
    with open(f'{EXPORT_DPV_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPV')

# add information about ontology
# this is assumed to be in file dpv-ontology-metadata.ttl
graph = Graph()
graph.load('ontology_metadata/dpv.ttl', format='turtle')
graph.load('ontology_metadata/dpv-semantics.ttl', format='turtle')
DPV_GRAPH += graph

for prefix, namespace in NAMESPACES.items():
        DPV_GRAPH.namespace_manager.bind(prefix, namespace)
serialize_graph(DPV_GRAPH, f'{EXPORT_DPV_PATH}/dpv')

##############################################################################

# DPV-GDPR #
# dpv-gdpr is the exact same as dpv in terms of requirements and structure
# except that the namespace is different
# so instead of rewriting the entire code again for dpv-gdpr,
# here I become lazy and instead change the DPV namespace to DPV-GDPR

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

BASE = NAMESPACES['dpv-gdpr']
DPV_GDPR_GRAPH = Graph()
proposed_terms = {}
DPV_GDPR_GRAPH.add((BASE[''], RDF.type, SKOS.ConceptScheme))

for name, module in DPV_GDPR_CSV_FILES.items():
    graph = Graph()
    proposed = []
    DEBUG('------')
    DEBUG(f'Processing {name} module')
    for prefix, namespace in NAMESPACES.items():
        graph.namespace_manager.bind(prefix, namespace)
    if 'classes' in module:
        classes = extract_terms_from_csv(module['classes'], DPV_Class)
        DEBUG(f'there are {len(classes)} classes in {name}')
        returnval = add_triples_for_classes(classes, graph)
        if returnval:
            proposed.extend(returnval)
    if 'properties' in module:
        properties = extract_terms_from_csv(module['properties'], DPV_Property)
        DEBUG(f'there are {len(properties)} properties in {name}')
        returnval = add_triples_for_properties(properties, graph)
        if returnval:
            proposed.extend(returnval)
    if proposed:
        proposed_terms[name] = proposed
    # add collection representing concepts
    graph.add((BASE[f'{name.title()}Concepts'], RDF.type, SKOS.Collection))
    graph.add((BASE[f'{name.title()}Concepts'], DCT.title, Literal(f'{name.title()} Concepts', datatype=XSD.string)))
    for concept, _, _ in graph.triples((None, RDF.type, SKOS.Concept)):
        graph.add((BASE[f'{name.title()}Concepts'], SKOS.member, concept))
        DPV_GDPR_GRAPH.add((concept, SKOS.inScheme, DPV_GDPR['']))
    # serialize
    serialize_graph(graph, f'{EXPORT_DPV_GDPR_MODULE_PATH}/{name}')
    if 'topconcept' in module:
        DPV_GDPR_GRAPH.add((BASE[''], SKOS.hasTopConcept, module['topconcept']))
    DPV_GDPR_GRAPH += graph

if proposed_terms:
    with open(f'{EXPORT_DPV_GDPR_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_GDPR_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPV-GDPR')
graph = Graph()
graph.load('ontology_metadata/dpv-gdpr.ttl', format='turtle')
DPV_GDPR_GRAPH += graph

for prefix, namespace in NAMESPACES.items():
    DPV_GDPR_GRAPH.namespace_manager.bind(prefix, namespace)
serialize_graph(DPV_GDPR_GRAPH, f'{EXPORT_DPV_GDPR_PATH}/dpv-gdpr')

##############################################################################

# DPV-PD #
# dpv-gdpr is the exact same as dpv in terms of requirements and structure
# except that the namespace is different
# so instead of rewriting the entire code again for dpv-gdpr,
# here I become lazy and instead change the DPV namespace to DPV-PD

DPV_PD_CSV_FILES = f'{IMPORT_CSV_PATH}/dpv-pd.csv'

BASE = NAMESPACES['dpv-pd']
DPV_PD_GRAPH = Graph()
proposed_terms = []
DEBUG('------')
DEBUG(f'Processing DPV-PD')
for prefix, namespace in NAMESPACES.items():
    DPV_PD_GRAPH.namespace_manager.bind(prefix, namespace)
classes = extract_terms_from_csv(DPV_PD_CSV_FILES, DPV_Class)
DEBUG(f'there are {len(classes)} classes in {name}')
returnval = add_triples_for_classes(classes, DPV_PD_GRAPH)
if returnval:
        proposed_terms.extend(returnval)
# add collection representing concepts
DPV_PD_GRAPH.add((BASE[f'PersonalDataConcepts'], RDF.type, SKOS.Collection))
DPV_PD_GRAPH.add((BASE[f'PersonalDataConcepts'], DCT.title, Literal(f'Personal Data Concepts', datatype=XSD.string)))
for concept, _, _ in DPV_PD_GRAPH.triples((None, RDF.type, SKOS.Concept)):
    DPV_PD_GRAPH.add((BASE[f'PersonalDataConcepts'], SKOS.member, concept))
if proposed_terms:
    with open(f'{EXPORT_DPV_PD_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_PD_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPV-PD')
# serialize
DPV_PD_GRAPH.load('ontology_metadata/dpv-pd.ttl', format='turtle')

for prefix, namespace in NAMESPACES.items():
    DPV_PD_GRAPH.namespace_manager.bind(prefix, namespace)
serialize_graph(DPV_PD_GRAPH, f'{EXPORT_DPV_PD_PATH}/dpv-pd')

# #############################################################################

# Save collected links as resource for generating HTML A HREF in JINJA2 templates
# file is in jinja2_resources/links_labels.json

import json
with open('jinja2_resources/links_label.json', 'w') as fd:
    fd.write(json.dumps(LINKS))