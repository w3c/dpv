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
EXPORT_DPV_PATH = '../dpv-owl'
EXPORT_DPV_MODULE_PATH = '../dpv-owl/modules'
EXPORT_DPV_GDPR_PATH = '../dpv-owl/dpv-gdpr'
EXPORT_DPV_GDPR_MODULE_PATH = '../dpv-owl/dpv-gdpr/modules'
EXPORT_DPV_PD_PATH = '../dpv-owl/dpv-pd'
EXPORT_DPV_LEGAL_PATH = '../dpv-owl/dpv-legal'
EXPORT_DPV_LEGAL_MODULE_PATH = '../dpv-owl/dpv-legal/modules'
EXPORT_DPV_TECH_PATH = '../dpv-owl/dpv-tech'

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

from vocab_management import *

# The dpv namespace is the default base for all terms
# Later, this is changed to write terms under DPV-GDPR namespace
BASE = DPVO

NAMESPACES_DPV_OWL = {
    'dpv': DPVO,
    'dpv-nace': DPV_NACE,
    'dpv-gdpr': DPVO_GDPR,
    'dpv-pd': DPVO_PD,
    'dpv-tech': DPVO_TECH,
    'dpvo': DPVO,
    'dpvo-gdpr': DPVO_GDPR,
    'dpvo-pd': DPVO_PD,
    'dpvo-tech': DPVO_TECH,
    'dpvo-risk': DPVO_RISK,
    'dpvo-rights-eu': DPVO_RIGHTS_EU,
}

# the field labels are based on what they should be translated to

DPV_Class = namedtuple('DPV_Class', [
    'term', 'rdfs_label', 'dct_description', 'rdfs_subclassof', 
    'parent_type', 'value', 
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
        # rdfs:subClassOf
        if cls.rdfs_subclassof:
            parents = [p.strip() for p in cls.rdfs_subclassof.split(',')]
            for parent in parents:
                if parent == 'dpv:Concept':
                    graph.add((BASE[f'{cls.term}'], RDF.type, OWL.Class))
                    continue
                prefix, term = parent.split(':')
                # gets the namespace from registered ones and create URI
                # will throw an error if namespace is not registered
                # dpv internal terms are expected to have the prefix i.e. dpv:term
                parent = NAMESPACES_DPV_OWL[f'{prefix}'][f'{term}']
                DEBUG(f'has parent: {parent}')
                if cls.parent_type == 'sc':
                    graph.add((BASE[f'{cls.term}'], RDF.type, OWL.Class))
                    graph.add((BASE[f'{cls.term}'], RDFS.subClassOf, parent))
                elif cls.parent_type == 'a':
                    graph.add((BASE[f'{cls.term}'], RDF.type, OWL.NamedIndividual))
                    graph.add((BASE[f'{cls.term}'], RDF.type, parent))
                else:
                    raise Exception(f'Parent Type Unknown: {cls.parent_type} ')
        
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
        graph.add((BASE[f'{prop.term}'], RDF.type, RDF.Property))
        if prop.rdfs_domain or prop.rdfs_range:
            graph.add((BASE[f'{prop.term}'], RDF.type, OWL.ObjectProperty))
        else:
            graph.add((BASE[f'{prop.term}'], RDF.type, OWL.AnnotationProperty))
        # rdfs:domain
        if prop.rdfs_domain:
            # assuming something like rdfs:Resource
            prefix, label = prop.rdfs_domain.split(':')
            if prefix == 'dpv':
                if label == 'Concept':
                    link = OWL.Thing
                else:
                    link = NAMESPACES_DPV_OWL[f'{prefix}'][f'{label}']
            else:
                link = NAMESPACES[prefix][f'{label}']
            # gets the namespace from registered ones and create URI
            # will throw an error if namespace is not registered
            # dpv internal terms are expected to have the prefix i.e. dpv:term
            graph.add((BASE[f'{prop.term}'], RDFS.domain, link))
        # rdfs:range
        if prop.rdfs_range:
            # assuming something like rdfs:Resource
            prefix, label = prop.rdfs_range.split(':')
            if prefix == 'dpv':
                if label == 'Concept':
                    link = OWL.Thing
                else:
                    link = NAMESPACES_DPV_OWL[f'{prefix}'][f'{label}']
            else:
                link = NAMESPACES[prefix][f'{label}']
            # gets the namespace from registered ones and create URI
            # will throw an error if namespace is not registered
            # dpv internal terms are expected to have the prefix i.e. dpv:term
            graph.add((BASE[f'{prop.term}'], RDFS.range, link))
        # rdfs:subPropertyOf
        if prop.rdfs_subpropertyof:
            parents = [p.strip() for p in prop.rdfs_subpropertyof.split(',')]
            for parent in parents:
                if parent == 'dpv:Relation':
                    continue
                if parent.startswith('http'):
                    graph.add((BASE[f'{prop.term}'], RDFS.subPropertyOf, URIRef(parent)))
                elif ':' in parent:
                    # assuming something like rdfs:Resource
                    prefix, term = parent.split(':')
                    # gets the namespace from registered ones and create URI
                    # will throw an error if namespace is not registered
                    # dpv internal terms are expected to have the prefix i.e. dpv:term
                    if 'o__' in prefix:
                        # explicit owl declaration
                        parent = prefix.replace('o__')
                        parent = NAMESPACES[prefix][f'{term}']
                    elif prefix == 'dpv':
                        parent = NAMESPACES_DPV_OWL[f'{prefix}'][f'{term}']
                    else:
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
        'model': 'ontology',
        },
    'personal_data': {
        'classes': f'{IMPORT_CSV_PATH}/PersonalData.csv',
        'properties': f'{IMPORT_CSV_PATH}/PersonalData_properties.csv',
        'model': 'ontology',
        },
    'purposes': {
        'classes': f'{IMPORT_CSV_PATH}/Purpose.csv',
        'properties': f'{IMPORT_CSV_PATH}/Purpose_properties.csv',
        'model': 'taxonomy',
        'topconcept': BASE['Purpose'],
        },
    'context': {
        'classes': f'{IMPORT_CSV_PATH}/Context.csv',
        'properties': f'{IMPORT_CSV_PATH}/Context_properties.csv',
        'model': 'ontology',
        },
    'status': {
        'classes': f'{IMPORT_CSV_PATH}/Status.csv',
        'properties': f'{IMPORT_CSV_PATH}/Status_properties.csv',
        'model': 'ontology',
        },
    'risk': {
        'classes': f'{IMPORT_CSV_PATH}/Risk.csv',
        'properties': f'{IMPORT_CSV_PATH}/Risk_properties.csv',
        'model': 'ontology',
        },
    'processing': {
        'classes': f'{IMPORT_CSV_PATH}/Processing.csv',
        'properties': f'{IMPORT_CSV_PATH}/Processing_properties.csv',
        'model': 'taxonomy',
        'topconcept': BASE['Processing'],
        },
    'processing_context': {
        'classes': f'{IMPORT_CSV_PATH}/ProcessingContext.csv',
        'properties': f'{IMPORT_CSV_PATH}/ProcessingContext_properties.csv',
        'model': 'ontology',
        },
    'processing_scale': {
        'classes': f'{IMPORT_CSV_PATH}/ProcessingScale.csv',
        'properties': f'{IMPORT_CSV_PATH}/ProcessingScale_properties.csv',
        'model': 'ontology',
        },
    'technical_organisational_measures': {
        'classes': f'{IMPORT_CSV_PATH}/TechnicalOrganisationalMeasure.csv',
        'properties': f'{IMPORT_CSV_PATH}/TechnicalOrganisationalMeasure_properties.csv',
        'model': 'ontology',
        },
    'technical_measures': {
        'classes': f'{IMPORT_CSV_PATH}/TechnicalMeasure.csv',
        'model': 'taxonomy',
        'topconcept': BASE['TechnicalMeasure'],
        },
    'organisational_measures': {
        'classes': f'{IMPORT_CSV_PATH}/OrganisationalMeasure.csv',
        'model': 'taxonomy',
        'topconcept': BASE['OrganisationalMeasure'],
        },
    'entities': {
        'classes': f'{IMPORT_CSV_PATH}/Entities.csv',
        'properties': f'{IMPORT_CSV_PATH}/Entities_properties.csv',
        'model': 'ontology',
        },
    'entities_authority': {
        'classes': f'{IMPORT_CSV_PATH}/Entities_Authority.csv',
        'properties': f'{IMPORT_CSV_PATH}/Entities_Authority_properties.csv',
        'model': 'ontology',
        },
    'entities_legalrole': {
        'classes': f'{IMPORT_CSV_PATH}/Entities_LegalRole.csv',
        'properties': f'{IMPORT_CSV_PATH}/Entities_LegalRole_properties.csv',
        'model': 'ontology',
        },
    'entities_organisation': {
        'classes': f'{IMPORT_CSV_PATH}/Entities_Organisation.csv',
        'model': 'ontology',
        },
    'entities_datasubject': {
        'classes': f'{IMPORT_CSV_PATH}/Entities_DataSubject.csv',
        'properties': f'{IMPORT_CSV_PATH}/Entities_DataSubject_properties.csv',
        'model': 'ontology',
        },
    'jurisdiction': {
        'classes': f'{IMPORT_CSV_PATH}/Jurisdiction.csv',
        'properties': f'{IMPORT_CSV_PATH}/Jurisdiction_properties.csv',
        'model': 'ontology',
        },
    'legal_basis': {
        'classes': f'{IMPORT_CSV_PATH}/LegalBasis.csv',
        'properties': f'{IMPORT_CSV_PATH}/LegalBasis_properties.csv',
        'model': 'taxonomy',
        'topconcept': BASE['LegalBasis'],
    },
    'consent': {
        # 'classes': f'{IMPORT_CSV_PATH}/Consent.csv',
        'properties': f'{IMPORT_CSV_PATH}/Consent_properties.csv',
        'model': 'ontology',
    },
}

# this graph will get written to dpv.ttl
DPV_GRAPH = Graph()
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
    # serialize
    serialize_graph(graph, f'{EXPORT_DPV_MODULE_PATH}/{name}')
    DPV_GRAPH += graph

if proposed_terms:
    with open(f'{EXPORT_DPV_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPV-OWL')

# add information about ontology
# this is assumed to be in file dpv-ontology-metadata.ttl
graph = Graph()
graph.load('ontology_metadata/dpv-owl.ttl', format='turtle')
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

BASE = NAMESPACES['dpvo-gdpr']
DPV_GDPR_GRAPH = Graph()
proposed_terms = {}

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
    # serialize
    serialize_graph(graph, f'{EXPORT_DPV_GDPR_MODULE_PATH}/{name}')
    DPV_GDPR_GRAPH += graph

if proposed_terms:
    with open(f'{EXPORT_DPV_GDPR_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_GDPR_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPVO-GDPR')
graph = Graph()
graph.load('ontology_metadata/dpv-owl-gdpr.ttl', format='turtle')
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

BASE = NAMESPACES['dpvo-pd']
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
if proposed_terms:
    with open(f'{EXPORT_DPV_PD_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_PD_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPVO-PD')
# serialize
DPV_PD_GRAPH.load('ontology_metadata/dpv-owl-pd.ttl', format='turtle')

for prefix, namespace in NAMESPACES.items():
    DPV_PD_GRAPH.namespace_manager.bind(prefix, namespace)
serialize_graph(DPV_PD_GRAPH, f'{EXPORT_DPV_PD_PATH}/dpv-pd')

# #############################################################################

# DPV-LEGAL #
# The structure of DPV-Legal spreadsheets is different than the rest of DPV
# Therefore, it requires separate functions/code to handle

DPV_LEGAL_CSV_FILES = {
    f'{IMPORT_CSV_PATH}/legal_Authorities.csv',
    f'{IMPORT_CSV_PATH}/legal_EU_Adequacy.csv',
    f'{IMPORT_CSV_PATH}/legal_EU_EEA.csv',
    f'{IMPORT_CSV_PATH}/legal_Laws.csv',
    f'{IMPORT_CSV_PATH}/legal_Locations.csv',
    f'{IMPORT_CSV_PATH}/legal_properties.csv',
    }

BASE = NAMESPACES['dpvo-legal']
DPV_LEGAL_GRAPH = Graph()
for prefix, namespace in NAMESPACES.items():
    DPV_LEGAL_GRAPH.namespace_manager.bind(prefix, namespace)
graph = Graph()
for prefix, namespace in NAMESPACES.items():
    graph.namespace_manager.bind(prefix, namespace)
proposed_terms = {}
DEBUG('------')
DEBUG(f'Processing DPV-LEGAL')
for prefix, namespace in NAMESPACES.items():
    DPV_LEGAL_GRAPH.namespace_manager.bind(prefix, namespace)

DEBUG(f'Processing DPV-LEGAL classes and properties')
# NOTE: There are currently no additional classes
# >>> START
# classes = extract_terms_from_csv(DPV_LEGAL_CSV_FILES, DPV_Class)
# DEBUG(f'there are {len(classes)} classes in {name}')
# returnval = add_triples_for_classes(classes, DPV_LEGAL_GRAPH)
# if returnval:
#         proposed_terms.extend(returnval)
# add collection representing concepts
# DPV_LEGAL_GRAPH.add((BASE[f'LegalConcepts'], DCT.title, Literal(f'Legal Concepts', datatype=XSD.string)))
properties = extract_terms_from_csv(
    f'{IMPORT_CSV_PATH}/legal_properties.csv', DPV_Property)
DEBUG(f'there are {len(properties)} properties in DPV-LEGAL')
returnval = add_triples_for_properties(properties, graph)
if returnval:
    proposed_terms['ontology'] = returnval
# serialize
# DPV_LEGAL_GRAPH.load('ontology_metadata/dpv-legal.ttl', format='turtle')
serialize_graph(graph, f'{EXPORT_DPV_LEGAL_MODULE_PATH}/ontology')
DPV_LEGAL_GRAPH += graph
if proposed:
    proposed_terms['vocab'] = proposed

DEBUG('Processing DPV-LEGAL Locations')
graph = Graph()
for prefix, namespace in NAMESPACES.items():
    graph.namespace_manager.bind(prefix, namespace)
proposed = []
Location_schema = namedtuple('Legal_Location', (
    'Term', 'Label', 'ParentTerm', 'Alpha2', 'Alpha3', 'Numeric', 'M49',
    'broader', 'narrower', 'created', 'modified', 
    'status', 'contributors', 'resolution'))
concepts = extract_terms_from_csv(
    f'{IMPORT_CSV_PATH}/legal_Locations.csv', Location_schema)
for row in concepts:
    if row.status not in VOCAB_TERM_ACCEPT:
        proposed.append(row.Term)
        continue
    term = BASE[row.Term]
    parent = row.ParentTerm.replace("dpv:", "")
    graph.add((term, RDF.type, DPVO[f'{parent}']))
    graph.add((term, RDF.type, OWL.NamedIndividual))
    graph.add((term, RDFS.isDefinedBy, BASE['']))
    graph.add((term, DCT.title, Literal(row.Label, lang='en')))
    graph.add((term, RDFS.label, Literal(row.Label, lang='en')))
    if row.Alpha2:
        graph.add((
            term, BASE.iso_alpha2, Literal(row.Alpha2, datatype=XSD.string)))
        graph.add((
            term, BASE.iso_alpha3, Literal(row.Alpha3, datatype=XSD.string)))
        graph.add((
            term, BASE.iso_numeric, Literal(row.Numeric, datatype=XSD.string)))
    if row.M49:
        graph.add((
            term, BASE.un_m49, Literal(row.M49, datatype=XSD.string)))
    parents = [p.strip() for p in row.broader.split(',') if p]
    for item in parents:
        print(f'item: {item}')
        prefix, parent = item.split(':')
        parent = NAMESPACES[prefix][f'{parent}']
        graph.add((term, DCT.isPartOf, parent))
        graph.add((parent, DCT.hasPart, term))
    # dct:created
    graph.add((term, DCT.created, Literal(row.created, datatype=XSD.date)))
    # dct:modified
    if row.modified:
        graph.add((term, DCT.modified, Literal(row.modified, datatype=XSD.date)))
    # sw:term_status
    graph.add((term, SW.term_status, Literal(row.status, lang='en')))
    # dct:creator
    if row.contributors:
        authors = [a.strip() for a in row.contributors.split(',')]
        for author in authors:
            graph.add((term, DCT.creator, Literal(author, datatype=XSD.string)))
serialize_graph(graph, f'{EXPORT_DPV_LEGAL_MODULE_PATH}/locations')
DPV_LEGAL_GRAPH += graph
if proposed:
    proposed_terms['location'] = proposed

DEBUG('Processing DPV-LEGAL Laws')
graph = Graph()
for prefix, namespace in NAMESPACES.items():
    graph.namespace_manager.bind(prefix, namespace)
proposed = []
Location_schema = namedtuple('Legal_Laws', (
    'term', 'label_en', 'label_de', 'time_start', 'time_end',
    'jurisdictions', 'webpage',
    'created', 'modified', 'status', 'contributors', 'resolution'))
concepts = extract_terms_from_csv(
    f'{IMPORT_CSV_PATH}/legal_Laws.csv', Location_schema)
for row in concepts:
    if row.status not in VOCAB_TERM_ACCEPT:
        proposed.append(row.Term)
        continue
    term = BASE[row.term]
    graph.add((term, RDF.type, DPVO.Law))
    graph.add((term, RDF.type, OWL.NamedIndividual))
    graph.add((term, RDFS.isDefinedBy, BASE['']))
    graph.add((term, DCT.title, Literal(row.label_en, lang='en')))
    graph.add((term, RDFS.label, Literal(row.label_en, lang='en')))
    if row.label_de:
        graph.add((term, DCT.title, Literal(row.label_de, lang='de')))
        graph.add((term, RDFS.label, Literal(row.label_de, lang='de')))
    for loc in row.jurisdictions.split(','):
        loc = loc.replace("dpv-legal:", "")
        graph.add((term, DPVO.hasJurisdiction, BASE[f'{loc}']))
        graph.add((BASE[f'{loc}'], DPVO.hasLaw, term))
    graph.add((term, FOAF.homepage, Literal(row.webpage, datatype=XSD.anyURI)))
    if row.time_start:
        dct_temporal = BNode()
        graph.add((term, DCT.temporal, dct_temporal))
        graph.add((dct_temporal, RDF.type, TIME.ProperInterval))
        dct_date = BNode()
        graph.add((dct_temporal, TIME.hasBeginning, dct_date))
        graph.add((dct_date, TIME.inXSDDate, Literal(row.time_start, datatype=XSD.date)))
        if row.time_end:
            dct_date = BNode()
            graph.add((dct_temporal, TIME.hasEnd, dct_date))
            graph.add((dct_date, TIME.inXSDDate, Literal(row.time_end, datatype=XSD.date)))
    # dct:created
    graph.add((term, DCT.created, Literal(row.created, datatype=XSD.date)))
    # dct:modified
    if row.modified:
        graph.add((term, DCT.modified, Literal(row.modified, datatype=XSD.date)))
    # sw:term_status
    graph.add((term, SW.term_status, Literal(row.status, lang='en')))
    # dct:creator
    if row.contributors:
        authors = [a.strip() for a in row.contributors.split(',')]
        for author in authors:
            graph.add((term, DCT.creator, Literal(author, datatype=XSD.string)))
serialize_graph(graph, f'{EXPORT_DPV_LEGAL_MODULE_PATH}/laws')
DPV_LEGAL_GRAPH += graph
if proposed:
    proposed_terms['laws'] = proposed

DEBUG('Processing DPV-LEGAL Authorities')
graph = Graph()
for prefix, namespace in NAMESPACES.items():
    graph.namespace_manager.bind(prefix, namespace)
proposed = []
Location_schema = namedtuple('Legal_Laws', (
    'term', 'label_en', 'label_de', 'type', 'jurisdictions', 'laws', 'webpage',
    'created', 'modified', 'status', 'contributors', 'resolution'))
concepts = extract_terms_from_csv(
    f'{IMPORT_CSV_PATH}/legal_Authorities.csv', Location_schema)
for row in concepts:
    if row.status not in VOCAB_TERM_ACCEPT:
        proposed.append(row.Term)
        continue
    term = BASE[row.term]
    graph.add((term, RDF.type, DPVO[f'{row.type.replace("dpv:","")}']))
    graph.add((term, RDF.type, OWL.NamedIndividual))
    graph.add((term, RDFS.isDefinedBy, BASE['']))
    graph.add((term, DCT.title, Literal(row.label_en, lang='en')))
    graph.add((term, RDFS.label, Literal(row.label_en, lang='en')))
    if row.label_de:
        graph.add((term, DCT.title, Literal(row.label_de, lang='de')))
        graph.add((term, RDFS.label, Literal(row.label_de, lang='de')))
    for loc in row.jurisdictions.split(','):
        loc = loc.replace("dpv-legal:", "")
        graph.add((term, DPVO.hasJurisdiction, BASE[f'{loc}']))
        graph.add((BASE[f'{loc}'], DPVO.hasAuthority, term))
    for law in row.laws.split(','):
        law = law.replace("dpv-legal:", "")
        graph.add((term, DPVO.hasLaw, BASE[f'{law}']))
        graph.add((BASE[f'{law}'], DPVO.hasAuthority, term))
    graph.add((term, FOAF.homepage, Literal(row.webpage, datatype=XSD.anyURI)))
    # dct:created
    graph.add((term, DCT.created, Literal(row.created, datatype=XSD.date)))
    # dct:modified
    if row.modified:
        graph.add((term, DCT.modified, Literal(row.modified, datatype=XSD.date)))
    # sw:term_status
    graph.add((term, SW.term_status, Literal(row.status, lang='en')))
    # dct:creator
    if row.contributors:
        authors = [a.strip() for a in row.contributors.split(',')]
        for author in authors:
            graph.add((term, DCT.creator, Literal(author, datatype=XSD.string)))
serialize_graph(graph, f'{EXPORT_DPV_LEGAL_MODULE_PATH}/authorities')
DPV_LEGAL_GRAPH += graph
if proposed:
    proposed_terms['authorities'] = proposed

DEBUG('Processing DPV-LEGAL EU-EEA Memberships')
graph = Graph()
for prefix, namespace in NAMESPACES.items():
    graph.namespace_manager.bind(prefix, namespace)
proposed = []
Location_schema = namedtuple('Legal_EU_EEA', (
    'term', 'label', 'type', 'broader', 'time_start', 'time_end', 'members',
    'created', 'modified', 'status', 'contributors', 'resolution'))
concepts = extract_terms_from_csv(
    f'{IMPORT_CSV_PATH}/legal_EU_EEA.csv', Location_schema)
for row in concepts:
    if row.status not in VOCAB_TERM_ACCEPT:
        proposed.append(row.Term)
        continue
    term = BASE[row.term]
    graph.add((term, RDF.type, DPVO[f'{row.type.replace("dpv:","")}']))
    graph.add((term, RDF.type, OWL.NamedIndividual))
    graph.add((term, RDFS.isDefinedBy, BASE['']))
    graph.add((term, DCT.title, Literal(row.label, lang='en')))
    if row.broader:
        graph.add((term, DCT.isPartOf, BASE[f'{row.broader.replace("dpv-legal:","")}']))
        graph.add((BASE[f'{row.broader.replace("dpv-legal:","")}'], DCT.hasPart, term))
    for loc in row.members.split(','):
        loc = loc.replace("dpv-legal:", "")
        graph.add((term, DPVO.hasCountry, BASE[f'{loc}']))
        graph.add((term, DCT.isPartOf, BASE[f'{loc}']))
        graph.add((BASE[f'{loc}'], DCT.hasPart, term))
    if row.time_start:
        dct_temporal = BNode()
        graph.add((term, DCT.temporal, dct_temporal))
        graph.add((dct_temporal, RDF.type, TIME.ProperInterval))
        dct_date = BNode()
        graph.add((dct_temporal, TIME.hasBeginning, dct_date))
        graph.add((dct_date, TIME.inXSDDate, Literal(row.time_start, datatype=XSD.date)))
        if row.time_end:
            dct_date = BNode()
            graph.add((dct_temporal, TIME.hasEnd, dct_date))
            graph.add((dct_date, TIME.inXSDDate, Literal(row.time_end, datatype=XSD.date)))
    # dct:created
    graph.add((term, DCT.created, Literal(row.created, datatype=XSD.date)))
    # dct:modified
    if row.modified:
        graph.add((term, DCT.modified, Literal(row.modified, datatype=XSD.date)))
    # sw:term_status
    graph.add((term, SW.term_status, Literal(row.status, lang='en')))
    # dct:creator
    if row.contributors:
        authors = [a.strip() for a in row.contributors.split(',')]
        for author in authors:
            graph.add((term, DCT.creator, Literal(author, datatype=XSD.string)))
serialize_graph(graph, f'{EXPORT_DPV_LEGAL_MODULE_PATH}/eu_eea')
DPV_LEGAL_GRAPH += graph
if proposed:
    proposed_terms['EU_EEA'] = proposed

DEBUG('Processing DPV-LEGAL EU Adequacy Decisions')
graph = Graph()
for prefix, namespace in NAMESPACES.items():
    graph.namespace_manager.bind(prefix, namespace)
proposed = []
Location_schema = namedtuple('Legal_EU_Adequacy', (
    'term', 'label', 'webpage', 'countryA', 'countryB',
    'time_start', 'time_end',
    'created', 'modified', 'status', 'contributors', 'resolution'))
concepts = extract_terms_from_csv(
    f'{IMPORT_CSV_PATH}/legal_EU_Adequacy.csv', Location_schema)
for row in concepts:
    if row.status not in VOCAB_TERM_ACCEPT:
        proposed.append(row.Term)
        continue
    term = BASE[row.term]
    graph.add((term, RDF.type, DPVO.Law))
    graph.add((term, RDF.type, OWL.NamedIndividual))
    graph.add((term, RDF.type, DPVO_GDPR['A45-3']))
    graph.add((term, RDFS.isDefinedBy, BASE['']))
    graph.add((term, DCT.title, Literal(row.label, lang='en')))
    graph.add((term, FOAF.homepage, Literal(row.webpage, datatype=XSD.anyURI)))
    graph.add((term, DPVO.hasJurisdiction, BASE[f'{row.countryA.replace("dpv-legal:","")}']))
    graph.add((term, DPVO.hasJurisdiction, BASE[f'{row.countryB.replace("dpv-legal:","")}']))
    if row.time_start:
        dct_temporal = BNode()
        graph.add((term, DCT.temporal, dct_temporal))
        graph.add((dct_temporal, RDF.type, TIME.ProperInterval))
        dct_date = BNode()
        graph.add((dct_temporal, TIME.hasBeginning, dct_date))
        graph.add((dct_date, TIME.inXSDDate, Literal(row.time_start, datatype=XSD.date)))
        if row.time_end:
            dct_date = BNode()
            graph.add((dct_temporal, TIME.hasEnd, dct_date))
            graph.add((dct_date, TIME.inXSDDate, Literal(row.time_end, datatype=XSD.date)))
    # dct:created
    graph.add((term, DCT.created, Literal(row.created, datatype=XSD.date)))
    # dct:modified
    if row.modified:
        graph.add((term, DCT.modified, Literal(row.modified, datatype=XSD.date)))
    # sw:term_status
    graph.add((term, SW.term_status, Literal(row.status, lang='en')))
    # dct:creator
    if row.contributors:
        authors = [a.strip() for a in row.contributors.split(',')]
        for author in authors:
            graph.add((term, DCT.creator, Literal(author, datatype=XSD.string)))
serialize_graph(graph, f'{EXPORT_DPV_LEGAL_MODULE_PATH}/eu_adequacy')
DPV_LEGAL_GRAPH += graph
if proposed:
    proposed_terms['EU_Adequacy'] = proposed

DPV_LEGAL_GRAPH.load('ontology_metadata/dpv-owl-legal.ttl', format='turtle')
serialize_graph(DPV_LEGAL_GRAPH, f'{EXPORT_DPV_LEGAL_PATH}/dpv-legal')
if proposed_terms:
    with open(f'{EXPORT_DPV_LEGAL_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_LEGAL_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPV-LEGAL')

# #############################################################################

# DPV-TECH #

DPV_TECH_CSV_FILES = [
    f'{IMPORT_CSV_PATH}/dpv-tech.csv',
    f'{IMPORT_CSV_PATH}/dpv-tech_properties.csv',
    ]

BASE = NAMESPACES['dpv-tech']
DPV_TECH_GRAPH = Graph()
proposed_terms = []
DEBUG('------')
DEBUG(f'Processing DPV-TECH')
for prefix, namespace in NAMESPACES.items():
    DPV_TECH_GRAPH.namespace_manager.bind(prefix, namespace)
classes = extract_terms_from_csv(DPV_TECH_CSV_FILES[0], DPV_Class)
properties = extract_terms_from_csv(DPV_TECH_CSV_FILES[1], DPV_Property)
DEBUG(f'there are {len(classes)} classes and {len(properties)} properties in {name}')
returnval = add_triples_for_classes(classes, DPV_TECH_GRAPH)
if returnval:
        proposed_terms.extend(returnval)
returnval = add_triples_for_properties(properties, DPV_TECH_GRAPH)
if returnval:
        proposed_terms.extend(returnval)
if proposed_terms:
    with open(f'{EXPORT_DPV_TECH_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_TECH_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPV-TECH')
# serialize
DPV_TECH_GRAPH.load('ontology_metadata/dpv-owl-tech.ttl', format='turtle')

for prefix, namespace in NAMESPACES.items():
    DPV_TECH_GRAPH.namespace_manager.bind(prefix, namespace)
serialize_graph(DPV_TECH_GRAPH, f'{EXPORT_DPV_TECH_PATH}/dpv-tech')

# #############################################################################