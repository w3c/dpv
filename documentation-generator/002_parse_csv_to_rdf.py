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

# CONTRIBUTION: If anyone is willing to turn these scripts into
# an equivalent RML/R2RML or similar mappings, please let us know
########################################

IMPORT_CSV_PATH = './vocab_csv'
EXPORT_DPV_PATH = '../dpv'
EXPORT_DPV_MODULE_PATH = '../dpv/modules'
EXPORT_DPV_GDPR_PATH = '../dpv-gdpr'
EXPORT_DPV_GDPR_MODULE_PATH = '../dpv-gdpr/modules'
EXPORT_DPV_PD_PATH = '../dpv-pd'
EXPORT_DPV_LEGAL_PATH = '../dpv-legal'
EXPORT_DPV_LEGAL_MODULE_PATH = '../dpv-legal/modules'
EXPORT_DPV_TECH_PATH = '../dpv-tech'
EXPORT_DPV_TECH_MODULE_PATH = '../dpv-tech/modules'
EXPORT_RISK_PATH = '../risk'
EXPORT_RISK_MODULE_PATH = '../risk/modules'
EXPORT_RIGHTS_EU_PATH = '../rights/eu'

import csv
from collections import namedtuple
import json

from rdflib import Graph, Namespace
from rdflib.compare import graph_diff
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
BASE = DPV

# the field labels are based on what they should be translated to

DPV_Class = namedtuple('DPV_Class', [
            'term', 'skos_prefLabel', 'skos_definition', 'dpv_isSubTypeOf',
            'parent_type', 'rdf_value', 
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

EXAMPLES_GRAPH = Graph()
EXAMPLES_GRAPH.load('../examples/examples.ttl', format='ttl')


def get_examples_for_concept(concept):
    concepts = list(EXAMPLES_GRAPH.triples((None, DCT.subject, concept)))
    if concepts:
        concepts = [s for s, _, _ in concepts]
    return concepts


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
    # examples
    examples = get_examples_for_concept(BASE[f'{term.term}'])
    if examples:
        for ex in examples:
            graph.add((BASE[f'{term.term}'], VANN.example, ex))

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
        if cls.sw_termstatus == 'sunset':
            graph.add((
                BASE[f'{cls.term}'], SKOS.editorialNote, Literal(
                "WARNING: This concept will be deprecated in future releases", lang='en')))
        # rdf:type
        DEBUG(cls.term)
        graph.add((BASE[f'{cls.term}'], RDF.type, DPV.Concept))
        # rdfs:subClassOf
        if cls.dpv_isSubTypeOf:
            parents = [p.strip() for p in cls.dpv_isSubTypeOf.split(',')]
            for parent in parents:
                if parent == "dpv:Concept":
                    continue
                prefix, term = parent.split(':')
                # gets the namespace from registered ones and create URI
                # will throw an error if namespace is not registered
                # dpv terms are expected to have prefixes i.e. dpv:term
                parent = NAMESPACES[prefix][f'{term}']
                if cls.parent_type == 'sc':
                    graph.add((BASE[f'{cls.term}'], DPV.isSubTypeOf, parent))
                elif cls.parent_type == 'a':
                    graph.add((BASE[f'{cls.term}'], DPV.isInstanceOf, parent))
                else:
                    raise Exception(f'Parent Type Unknown: {cls.parent_type} ')
                graph.add((BASE[f'{cls.term}'], SKOS.broader, parent))
                graph.add((parent, SKOS.narrower, BASE[f'{cls.term}']))
        # rdf:value
        if cls.rdf_value:
            value, datatype = cls.rdf_value.split(',')
            namespace, literal = datatype.split(':')
            datatype = NAMESPACES[namespace.strip()][literal.strip()]
            graph.add((
                BASE[f'{cls.term}'], RDF.value, 
                Literal(value.strip(), datatype=datatype)))
        
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
        if prop.sw_termstatus == 'sunset':
            graph.add((
                BASE[f'{prop.term}'], SKOS.editorialNote, Literal(
                "WARNING: This concept will be deprecated in future releases", lang='en')))
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
            graph.add((BASE[f'{prop.term}'], DPV.hasDomain, link))
        # rdfs:range
        if prop.rdfs_range:
            # assuming something like rdfs:Resource
            prefix, label = prop.rdfs_range.split(':')
            # gets the namespace from registered ones and create URI
            # will throw an error if namespace is not registered
            # dpv internal terms are expected to have the prefix i.e. dpv:term
            link = NAMESPACES[prefix][f'{label}']
            graph.add((BASE[f'{prop.term}'], DPV.hasRange, link))
        # rdfs:subPropertyOf
        if prop.rdfs_subpropertyof:
            parents = [p.strip() for p in prop.rdfs_subpropertyof.split(',')]
            for parent in parents:
                if parent.startswith('http'):
                    graph.add((BASE[f'{prop.term}'], DPV.isSubTypeOf, URIRef(parent)))
                    graph.add((BASE[f'{prop.term}'], SKOS.broader, parent))
                    graph.add((parent, SKOS.narrower, BASE[f'{prop.term}']))
                elif ':' in parent:
                    if parent == "dpv:Relation":
                        continue
                    # assuming something like rdfs:Resource
                    prefix, term = parent.split(':')
                    # gets the namespace from registered ones and create URI
                    # will throw an error if namespace is not registered
                    # dpv internal terms are expected to have the prefix i.e. dpv:term
                    parent = NAMESPACES[prefix][f'{term}']
                    graph.add((BASE[f'{prop.term}'], DPV.isSubTypeOf, parent))
                    graph.add((BASE[f'{prop.term}'], SKOS.broader, parent))
                    graph.add((parent, SKOS.narrower, BASE[f'{prop.term}']))
                else:
                    graph.add((BASE[f'{prop.term}'], DPV.isSubTypeOf, Literal(parent, datatype=XSD.string)))
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
    'consent_types': {
        'classes': f'{IMPORT_CSV_PATH}/ConsentTypes.csv',
        # 'properties': f'{IMPORT_CSV_PATH}/Consent_properties.csv',
        'model': 'ontology',
    },
    'consent_status': {
        'classes': f'{IMPORT_CSV_PATH}/ConsentStatus.csv',
        # 'properties': f'{IMPORT_CSV_PATH}/Consent_properties.csv',
        'model': 'ontology',
    },
    'rules': {
        'classes': f'{IMPORT_CSV_PATH}/Rules.csv',
        'properties': f'{IMPORT_CSV_PATH}/Rules_properties.csv',
        'model': 'ontology',
    },
    'rights': {
        'classes': f'{IMPORT_CSV_PATH}/Rights.csv',
        'properties': f'{IMPORT_CSV_PATH}/Rights_properties.csv',
        'model': 'ontology',
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
    graph.add((BASE[f'{name.title()}Concepts'], SKOS.prefLabel, Literal(f'{name.title()} Concepts', datatype=XSD.string)))
    for concept, _, _ in graph.triples((None, RDF.type, SKOS.Concept)):
        graph.add((BASE[f'{name.title()}Concepts'], SKOS.member, concept))
        DPV_GRAPH.add((concept, SKOS.inScheme, DPV['']))
    # serialize
    graph.parse('ontology_metadata/dpv-semantics.ttl', format='turtle')
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
graph.parse('ontology_metadata/dpv.ttl', format='turtle')
graph.parse('ontology_metadata/dpv-semantics.ttl', format='turtle')
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
    'legal_basis_special': {
        'classes': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis_SpecialCategory.csv',
        },
    'legal_basis_data_transfer': {
        'classes': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis_DataTransfer.csv',
        },
    'rights': {
        'classes': f'{IMPORT_CSV_PATH}/GDPR_LegalRights.csv',
        },
    'data_transfers': {
        'classes': f'{IMPORT_CSV_PATH}/GDPR_DataTransfers.csv',
        },
    'dpia': {
        'classes': f'{IMPORT_CSV_PATH}/GDPR_DPIA.csv',
        },
    'compliance': {
        'classes': f'{IMPORT_CSV_PATH}/GDPR_compliance.csv',
        }
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
    graph.add((BASE[f'{name.title()}Concepts'], SKOS.prefLabel, Literal(f'{name.title()} Concepts', datatype=XSD.string)))
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
graph.parse('ontology_metadata/dpv-gdpr.ttl', format='turtle')
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
DPV_PD_GRAPH.add((BASE[f'PersonalDataConcepts'], SKOS.prefLabel, Literal(f'Personal Data Concepts', datatype=XSD.string)))
for concept, _, _ in DPV_PD_GRAPH.triples((None, RDF.type, SKOS.Concept)):
    DPV_PD_GRAPH.add((BASE[f'PersonalDataConcepts'], SKOS.member, concept))
if proposed_terms:
    with open(f'{EXPORT_DPV_PD_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_PD_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPV-PD')
# serialize
DPV_PD_GRAPH.parse('ontology_metadata/dpv-pd.ttl', format='turtle')

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

BASE = NAMESPACES['dpv-legal']
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
# DPV_LEGAL_GRAPH.add((BASE[f'LegalConcepts'], RDF.type, SKOS.Collection))
# DPV_LEGAL_GRAPH.add((BASE[f'LegalConcepts'], SKOS.prefLabel, Literal(f'Legal Concepts', datatype=XSD.string)))
# for concept, _, _ in DPV_LEGAL_GRAPH.triples((None, RDF.type, SKOS.Concept)):
#     DPV_LEGAL_GRAPH.add((BASE[f'LegalConcepts'], SKOS.member, concept))
properties = extract_terms_from_csv(
    f'{IMPORT_CSV_PATH}/legal_properties.csv', DPV_Property)
DEBUG(f'there are {len(properties)} properties in DPV-LEGAL')
returnval = add_triples_for_properties(properties, graph)
if returnval:
    proposed_terms['ontology'] = returnval
# serialize
# DPV_LEGAL_GRAPH.parse('ontology_metadata/dpv-legal.ttl', format='turtle')
serialize_graph(graph, f'{EXPORT_DPV_LEGAL_MODULE_PATH}/ontology')
DPV_LEGAL_GRAPH += graph
if proposed:
    proposed_terms['location'] = proposed

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
    parent = DPV[row.ParentTerm.replace("dpv:", "")]
    graph.add((term, RDF.type, DPV.Concept))
    graph.add((term, RDF.type, SKOS.Concept))
    graph.add((term, DPV.isInstanceOf, parent))
    graph.add((term, RDFS.isDefinedBy, BASE['']))
    graph.add((term, SKOS.prefLabel, Literal(row.Label, lang='en')))
    graph.add((term, SKOS.prefLabel, Literal(row.Label, lang='en')))
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
        graph.add((term, DPV.isSubTypeOf, parent))
        graph.add((term, SKOS.broader, parent))
        graph.add((parent, SKOS.narrower, term))
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
    graph.add((BASE['LocationConcepts'], SKOS.member, term))
graph.add((BASE['LocationConcepts'], RDF.type, SKOS.Collection))
serialize_graph(graph, f'{EXPORT_DPV_LEGAL_MODULE_PATH}/locations')
DPV_LEGAL_GRAPH += graph
if proposed:
    proposed_terms['vocab'] = proposed

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
        proposed.append(row.term)
        continue
    term = BASE[row.term]
    graph.add((term, RDF.type, DPV.Concept))
    graph.add((term, RDF.type, SKOS.Concept))
    graph.add((term, DPV.isInstanceOf, DPV.Law))
    graph.add((term, RDFS.isDefinedBy, BASE['']))
    graph.add((term, SKOS.prefLabel, Literal(row.label_en, lang='en')))
    graph.add((term, SKOS.prefLabel, Literal(row.label_en, lang='en')))
    if row.label_de:
        graph.add((term, SKOS.prefLabel, Literal(row.label_de, lang='de')))
        graph.add((term, SKOS.prefLabel, Literal(row.label_de, lang='de')))
    for loc in row.jurisdictions.split(','):
        loc = loc.replace("dpv-legal:", "")
        graph.add((term, DPV.hasJurisdiction, BASE[f'{loc}']))
        graph.add((BASE[f'{loc}'], DPV.hasLaw, term))
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
    graph.add((BASE['LawConcepts'], SKOS.member, term))
graph.add((BASE['LawConcepts'], RDF.type, SKOS.Collection))
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
    graph.add((term, RDF.type, DPV.Concept))
    graph.add((term, RDF.type, SKOS.Concept))
    graph.add((term, RDFS.isDefinedBy, BASE['']))
    graph.add((term, DPV.isInstanceOf, DPV[f'{row.type.replace("dpv:","")}']))
    graph.add((term, SKOS.prefLabel, Literal(row.label_en, lang='en')))
    graph.add((term, SKOS.prefLabel, Literal(row.label_en, lang='en')))
    if row.label_de:
        graph.add((term, SKOS.prefLabel, Literal(row.label_de, lang='de')))
        graph.add((term, SKOS.prefLabel, Literal(row.label_de, lang='de')))
    for loc in row.jurisdictions.split(','):
        loc = loc.replace("dpv-legal:", "")
        graph.add((term, DPV.hasJurisdiction, BASE[f'{loc}']))
        graph.add((BASE[f'{loc}'], DPV.hasAuthority, term))
    for law in row.laws.split(','):
        law = law.replace("dpv-legal:", "")
        graph.add((term, DPV.hasLaw, BASE[f'{law}']))
        graph.add((BASE[f'{law}'], DPV.hasAuthority, term))
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
    graph.add((BASE['AuthoritiesConcepts'], SKOS.member, term))
graph.add((BASE['AuthoritiesConcepts'], RDF.type, SKOS.Collection))
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
    graph.add((term, RDF.type, DPV.Concept))
    graph.add((term, RDF.type, SKOS.Concept))
    graph.add((term, RDFS.isDefinedBy, BASE['']))
    graph.add((term, DPV.isInstanceOf, DPV[f'{row.type.replace("dpv:","")}']))
    graph.add((term, SKOS.prefLabel, Literal(row.label, lang='en')))
    if row.broader:
        graph.add((term, SKOS.broader, BASE[f'{row.broader.replace("dpv-legal:","")}']))
        graph.add((BASE[f'{row.broader.replace("dpv-legal:","")}'], SKOS.narrower, term))
    for loc in row.members.split(','):
        loc = loc.replace("dpv-legal:", "")
        graph.add((term, DPV.hasCountry, BASE[f'{loc}']))
        graph.add((term, SKOS.narrower, BASE[f'{loc}']))
        graph.add((BASE[f'{loc}'], SKOS.broader, term))
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
    graph.add((BASE['EUEEAConcepts'], SKOS.member, term))
graph.add((BASE['EUEEAConcepts'], RDF.type, SKOS.Collection))
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
    graph.add((term, RDF.type, DPV.Concept))
    graph.add((term, RDF.type, SKOS.Concept))
    graph.add((term, RDFS.isDefinedBy, BASE['']))
    graph.add((term, DPV.isInstanceOf, DPV_GDPR['A45-3']))
    graph.add((term, SKOS.prefLabel, Literal(row.label, lang='en')))
    graph.add((term, FOAF.homepage, Literal(row.webpage, datatype=XSD.anyURI)))
    graph.add((term, DPV.hasJurisdiction, BASE[f'{row.countryA.replace("dpv-legal:","")}']))
    graph.add((term, DPV.hasJurisdiction, BASE[f'{row.countryB.replace("dpv-legal:","")}']))
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
    graph.add((BASE['AdequacyConcepts'], SKOS.member, term))
graph.add((BASE['AdequacyConcepts'], RDF.type, SKOS.Collection))
serialize_graph(graph, f'{EXPORT_DPV_LEGAL_MODULE_PATH}/eu_adequacy')
DPV_LEGAL_GRAPH += graph
if proposed:
    proposed_terms['EU_Adequacy'] = proposed

DPV_LEGAL_GRAPH.parse('ontology_metadata/dpv-legal.ttl', format='turtle')
serialize_graph(DPV_LEGAL_GRAPH, f'{EXPORT_DPV_LEGAL_PATH}/dpv-legal')
if proposed_terms:
    with open(f'{EXPORT_DPV_LEGAL_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_LEGAL_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPV-LEGAL')

# #############################################################################

# DPV-TECH #

BASE = NAMESPACES['dpv-tech']
DPV_TECH_CSV_FILES = {
    'core': {
        'classes': f'{IMPORT_CSV_PATH}/tech-core.csv',
        'properties': f'{IMPORT_CSV_PATH}/tech-core-properties.csv',
        'model': 'ontology',
    },
    'data': {
        'classes': f'{IMPORT_CSV_PATH}/tech-data.csv',
        'model': 'taxonomy',
        'topconcept': BASE['DataTechnology'],
    },
    'ops': {
        'classes': f'{IMPORT_CSV_PATH}/tech-ops.csv',
        'model': 'taxonomy',
        'topconcept': BASE['OperationalTechnology'],
    },
    'security': {
        'classes': f'{IMPORT_CSV_PATH}/tech-security.csv',
        'model': 'taxonomy',
        'topconcept': BASE['SecurityTechnology'],
    },
    'surveillance': {
        'classes': f'{IMPORT_CSV_PATH}/tech-surveillance.csv',
        'model': 'taxonomy',
        'topconcept': BASE['SurveillanceTechnology'],
    },
    'provision': {
        'classes': f'{IMPORT_CSV_PATH}/tech-provision.csv',
        'properties': f'{IMPORT_CSV_PATH}/tech-provision-properties.csv',
        'model': 'ontology',
    },
    'actors': {
        'classes': f'{IMPORT_CSV_PATH}/tech-actors.csv',
        'properties': f'{IMPORT_CSV_PATH}/tech-actors-properties.csv',
        'model': 'ontology',
    },
    'comms': {
        'classes': f'{IMPORT_CSV_PATH}/tech-comms.csv',
        'model': 'ontology',
    },
    'provision': {
        'classes': f'{IMPORT_CSV_PATH}/tech-provision.csv',
        'properties': f'{IMPORT_CSV_PATH}/tech-provision-properties.csv',
        'model': 'ontology',
    },
    'tools': {
        'classes': f'{IMPORT_CSV_PATH}/tech-tools.csv',
        'model': 'taxonomy',
    },   
}

DPV_TECH_GRAPH = Graph()
proposed_terms = []
DEBUG('------')
DEBUG(f'Processing DPV-TECH')
for prefix, namespace in NAMESPACES.items():
    DPV_TECH_GRAPH.namespace_manager.bind(prefix, namespace)
for name, module in DPV_TECH_CSV_FILES.items():
    graph = Graph()
    proposed = []
    DEBUG('------')
    model = module['model']
    topconcept = module.get('topconcept')
    DEBUG(f'Processing {name} {model}')
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
    graph.add((BASE[f'{name.title()}Concepts'], SKOS.prefLabel, Literal(f'{name.title()} Concepts', datatype=XSD.string)))
    for concept, _, _ in graph.triples((None, RDF.type, SKOS.Concept)):
        graph.add((BASE[f'{name.title()}Concepts'], SKOS.member, concept))
        DPV_GRAPH.add((concept, SKOS.inScheme, DPV['']))
    # serialize
    serialize_graph(graph, f'{EXPORT_DPV_TECH_MODULE_PATH}/{name}')
    if topconcept:
        DPV_TECH_GRAPH.add((BASE[''], SKOS.hasTopConcept, URIRef(topconcept)))
    DPV_TECH_GRAPH += graph

if proposed_terms:
    with open(f'{EXPORT_DPV_TECH_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_DPV_TECH_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in DPV-TECH')

# add information about ontology
# this is assumed to be in file dpv-ontology-metadata.ttl
graph = Graph()
graph.parse('ontology_metadata/dpv-tech.ttl', format='turtle')
DPV_TECH_GRAPH += graph

serialize_graph(DPV_TECH_GRAPH, f'{EXPORT_DPV_TECH_PATH}/dpv-tech')

##############################################################################

# Risk #

RISK_CSV_FILES = {
    'risk_consequences': {
        'classes': f'{IMPORT_CSV_PATH}/RiskConsequences.csv',
        },
    'risk_levels': {
        'classes': f'{IMPORT_CSV_PATH}/RiskLevels.csv',
        },
    'risk_matrix': {
        'classes': f'{IMPORT_CSV_PATH}/RiskMatrix.csv',
        },
    'risk_controls': {
        'classes': f'{IMPORT_CSV_PATH}/RiskControls.csv',
        },
    'risk_assessment': {
        'classes': f'{IMPORT_CSV_PATH}/RiskAssessmentTechniques.csv',
        },
    'risk_methodology': {
        'classes': f'{IMPORT_CSV_PATH}/RiskMethodology.csv',
        },
    }

BASE = NAMESPACES['risk']
RISK_GRAPH = Graph()
proposed_terms = {}
RISK_GRAPH.add((BASE[''], RDF.type, SKOS.ConceptScheme))

for name, module in RISK_CSV_FILES.items():
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
    graph.add((BASE[f'{name.title()}Concepts'], SKOS.prefLabel, Literal(f'{name.title()} Concepts', datatype=XSD.string)))
    for concept, _, _ in graph.triples((None, RDF.type, SKOS.Concept)):
        graph.add((BASE[f'{name.title()}Concepts'], SKOS.member, concept))
        RISK_GRAPH.add((concept, SKOS.inScheme, RISK['']))
    # serialize
    if name == 'risk_matrix':
        graph_extra = Graph()
        graph_extra.parse('rdf_inputs/risk-matrix-nodes.ttl', format='ttl')
        graph += graph_extra
    serialize_graph(graph, f'{EXPORT_RISK_MODULE_PATH}/{name}')
    if 'topconcept' in module:
        RISK_GRAPH.add((BASE[''], SKOS.hasTopConcept, module['topconcept']))
    RISK_GRAPH += graph

if proposed_terms:
    with open(f'{EXPORT_RISK_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_RISK_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in RISK')
graph = Graph()
graph.parse('ontology_metadata/risk.ttl', format='turtle')
RISK_GRAPH += graph

for prefix, namespace in NAMESPACES.items():
    RISK_GRAPH.namespace_manager.bind(prefix, namespace)
serialize_graph(RISK_GRAPH, f'{EXPORT_RISK_PATH}/risk')

##############################################################################

# RIGHTS-EU #

RIGHTS_EU_CSV_FILES = [
    f'{IMPORT_CSV_PATH}/EUFundamentalRights.csv',
    ]

BASE = NAMESPACES['rights-eu']
RIGHTS_EU_GRAPH = Graph()
proposed_terms = []
DEBUG('------')
DEBUG(f'Processing RIGHTS-EU')
for prefix, namespace in NAMESPACES.items():
    RIGHTS_EU_GRAPH.namespace_manager.bind(prefix, namespace)
classes = extract_terms_from_csv(RIGHTS_EU_CSV_FILES[0], DPV_Class)
DEBUG(f'there are {len(classes)} classes in {name}')
returnval = add_triples_for_classes(classes, RIGHTS_EU_GRAPH)
if returnval:
        proposed_terms.extend(returnval)
# returnval = add_triples_for_properties(properties, RIGHTS_EU_GRAPH)
# if returnval:
#         proposed_terms.extend(returnval)
# add collection representing concepts
RIGHTS_EU_GRAPH.add((BASE[f'EUFundamentalRightsConcepts'], RDF.type, SKOS.Collection))
RIGHTS_EU_GRAPH.add((BASE[f'EUFundamentalRightsConcepts'], SKOS.prefLabel, Literal(f'EU Fundamental Rights Concepts', datatype=XSD.string)))
for concept, _, _ in RIGHTS_EU_GRAPH.triples((None, RDF.type, SKOS.Concept)):
    RIGHTS_EU_GRAPH.add((BASE[f'EUFundamentalRightsConcepts'], SKOS.member, concept))
if proposed_terms:
    with open(f'{EXPORT_RIGHTS_EU_PATH}/proposed.json', 'w') as fd:
        json.dump(proposed_terms, fd)
    DEBUG(f'exported proposed terms to {EXPORT_RIGHTS_EU_PATH}/proposed.json')
else:
    DEBUG('no proposed terms in RIGHTS-EU')
# serialize
RIGHTS_EU_GRAPH.parse('ontology_metadata/rights-eu.ttl', format='turtle')

for prefix, namespace in NAMESPACES.items():
    RIGHTS_EU_GRAPH.namespace_manager.bind(prefix, namespace)
serialize_graph(RIGHTS_EU_GRAPH, f'{EXPORT_RIGHTS_EU_PATH}/rights-eu')

##############################################################################

# Save collected links as resource for generating HTML A HREF in JINJA2 templates
# file is in jinja2_resources/links_labels.json

import json
with open('jinja2_resources/links_label.json', 'w') as fd:
    fd.write(json.dumps(LINKS))