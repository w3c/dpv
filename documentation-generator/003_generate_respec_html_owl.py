#!/usr/bin/env python3
#author: Harshvardhan J. Pandit 

'''Generates ReSpec documentation for DPV using RDF and SPARQL'''

# The vocabularies are modular

IMPORT_DPV_PATH = '../dpv-owl/dpv.ttl'
IMPORT_DPV_MODULES_PATH = '../dpv-owl/modules'
EXPORT_DPV_HTML_PATH = '../dpv-owl'
IMPORT_DPV_GDPR_PATH = '../dpv-owl/dpv-gdpr/dpv-gdpr.ttl'
IMPORT_DPV_GDPR_MODULES_PATH = '../dpv-owl/dpv-gdpr/modules'
EXPORT_DPV_GDPR_HTML_PATH = '../dpv-owl/dpv-gdpr'
IMPORT_DPV_PD_PATH = '../dpv-owl/dpv-pd/dpv-pd.ttl'
EXPORT_DPV_PD_HTML_PATH = '../dpv-owl/dpv-pd'
IMPORT_DPV_LEGAL_PATH = '../dpv-owl/dpv-legal/dpv-legal.ttl'
IMPORT_DPV_LEGAL_MODULES_PATH = '../dpv-owl/dpv-legal/modules'
EXPORT_DPV_LEGAL_HTML_PATH = '../dpv-owl/dpv-legal'

from rdflib import Graph, Namespace
from rdflib import RDF, RDFS, OWL
from rdflib import URIRef
from rdform import DataGraph, RDFS_Resource
import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug

TEMPLATE_DATA = {}

G = DataGraph()

with open('./jinja2_resources/links_label.json', 'r') as fd:
    import json
    LINKS_LABELS = json.load(fd)

with open(f'{EXPORT_DPV_HTML_PATH}/proposed.json') as fd:
    TEMPLATE_DATA['proposed'] = json.load(fd)

def load_data(label, filepath):
    DEBUG(f'loading data for {label}')
    g = Graph()
    g.load(filepath, format='turtle')
    G = DataGraph()
    G.load(g)
    G.graph.ns = { k:v for k,v in G.graph.namespaces() }
    TEMPLATE_DATA[f'{label}_classes'] = G.get_instances_of('owl_Class')
    TEMPLATE_DATA[f'{label}_properties'] = G.get_instances_of('rdf_Property')


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


def fragment_this(item):
    if '#' not in item:
        return item
    return item.split('#')[-1]


def get_subclasses(item):
    return G.subclasses(item)


def saved_label(item):
    if type(item) is RDFS_Resource:
        item = item.iri
    if not type(item) is str:
        item = str(item)
    if item in LINKS_LABELS:
        return LINKS_LABELS[item]
    return item


# JINJA2 for templating and generating HTML
from jinja2 import FileSystemLoader, Environment
JINJA2_FILTERS = {
    'fragment_this': fragment_this,
    'prefix_this': prefix_this,
    'subclasses': get_subclasses,
    'saved_label': saved_label,
}

template_loader = FileSystemLoader(searchpath='./jinja2_resources')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)
template_env.filters.update(JINJA2_FILTERS)


# LOAD DATA
load_data('core', f'{IMPORT_DPV_MODULES_PATH}/base.ttl')
load_data('personaldata', f'{IMPORT_DPV_MODULES_PATH}/personal_data.ttl')
load_data('purpose', f'{IMPORT_DPV_MODULES_PATH}/purposes.ttl')
load_data('processing', f'{IMPORT_DPV_MODULES_PATH}/processing.ttl')
load_data('technical_organisational_measures', f'{IMPORT_DPV_MODULES_PATH}/technical_organisational_measures.ttl')
load_data('entities', f'{IMPORT_DPV_MODULES_PATH}/entities.ttl')
load_data('entities_authority', f'{IMPORT_DPV_MODULES_PATH}/entities_authority.ttl')
load_data('entities_legalrole', f'{IMPORT_DPV_MODULES_PATH}/entities_legalrole.ttl')
load_data('entities_organisation', f'{IMPORT_DPV_MODULES_PATH}/entities_organisation.ttl')
load_data('entities_datasubject', f'{IMPORT_DPV_MODULES_PATH}/entities_datasubject.ttl')
load_data('context', f'{IMPORT_DPV_MODULES_PATH}/context.ttl')
load_data('risk', f'{IMPORT_DPV_MODULES_PATH}/risk.ttl')
load_data('processing_context', f'{IMPORT_DPV_MODULES_PATH}/processing_context.ttl')
load_data('jurisdictions', f'{IMPORT_DPV_MODULES_PATH}/jurisdictions.ttl')
load_data('legal_basis', f'{IMPORT_DPV_MODULES_PATH}/legal_basis.ttl')
load_data('consent', f'{IMPORT_DPV_MODULES_PATH}/consent.ttl')
g = Graph()
g.load(f'{IMPORT_DPV_PATH}', format='turtle')
G.load(g)

# DPV: generate HTML

template = template_env.get_template('template_dpv_owl.jinja2')
with open(f'{EXPORT_DPV_HTML_PATH}/index.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV spec at f{EXPORT_DPV_HTML_PATH}/index.html')
with open(f'{EXPORT_DPV_HTML_PATH}/dpv.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV spec at f{EXPORT_DPV_HTML_PATH}/dpv.html')

# DPV-GDPR: generate HTML

with open(f'{EXPORT_DPV_GDPR_HTML_PATH}/proposed.json', 'r') as fd:
    TEMPLATE_DATA['proposed'] = json.load(fd)  
    
load_data('legal_basis', f'{IMPORT_DPV_GDPR_MODULES_PATH}/legal_basis.ttl')
load_data('rights', f'{IMPORT_DPV_GDPR_MODULES_PATH}/rights.ttl')
load_data('data_transfers', f'{IMPORT_DPV_GDPR_MODULES_PATH}/data_transfers.ttl')
g = Graph()
g.load(f'{IMPORT_DPV_GDPR_PATH}', format='turtle')
G.load(g)

template = template_env.get_template('template_dpv_gdpr_owl.jinja2')
with open(f'{EXPORT_DPV_GDPR_HTML_PATH}/index.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV-GDPR spec at f{EXPORT_DPV_GDPR_HTML_PATH}/index.html')
with open(f'{EXPORT_DPV_GDPR_HTML_PATH}/dpv-gdpr.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV-GDPR spec at f{EXPORT_DPV_GDPR_HTML_PATH}/dpv-gdpr.html')


# DPV-PD: generate HTML

with open(f'{EXPORT_DPV_PD_HTML_PATH}/proposed.json') as fd:
    TEMPLATE_DATA['proposed'] = json.load(fd)  

load_data('dpv_pd', f'{IMPORT_DPV_PD_PATH}')
g = Graph()
g.load(f'{IMPORT_DPV_PD_PATH}', format='turtle')
G.load(g)

template = template_env.get_template('template_dpv_pd_owl.jinja2')
with open(f'{EXPORT_DPV_PD_HTML_PATH}/index.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV-PD spec at f{EXPORT_DPV_PD_HTML_PATH}/index.html')
with open(f'{EXPORT_DPV_PD_HTML_PATH}/dpv-pd.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV-PD spec at f{EXPORT_DPV_PD_HTML_PATH}/dpv-pd.html')


# DPV-LEGAL: generate HTML

with open(f'{EXPORT_DPV_LEGAL_HTML_PATH}/proposed.json') as fd:
    TEMPLATE_DATA['proposed'] = json.load(fd)  

def load_legal_data(label, filepath):
    DEBUG(f'loading data for {label}')
    g = Graph()
    g.load(filepath, format='turtle')
    G = DataGraph()
    G.load(g)
    G.graph.ns = { k:v for k,v in G.graph.namespaces() }
    # TODO: Take the instance variable so that template has contextual info
    # e.g. Law can specify jurisdiction label, authorities, etc.,
    TEMPLATE_DATA[f'{label}_terms'] = G.get_instances_of('owl_NamedIndividual')

# load_legal_data('ontology', f'{IMPORT_DPV_LEGAL_MODULES_PATH}/ontology.ttl')
load_legal_data('locations', f'{IMPORT_DPV_LEGAL_MODULES_PATH}/locations.ttl')
load_legal_data('laws', f'{IMPORT_DPV_LEGAL_MODULES_PATH}/laws.ttl')
load_legal_data('authorities', f'{IMPORT_DPV_LEGAL_MODULES_PATH}/authorities.ttl')
load_legal_data('EU_EEA', f'{IMPORT_DPV_LEGAL_MODULES_PATH}/eu_eea.ttl')
load_legal_data('EU_Adequacy', f'{IMPORT_DPV_LEGAL_MODULES_PATH}/eu_adequacy.ttl')
g = Graph()
g.load(f'{IMPORT_DPV_LEGAL_PATH}', format='turtle')
G.load(g)

template = template_env.get_template('template_dpv_legal_owl.jinja2')
with open(f'{EXPORT_DPV_LEGAL_HTML_PATH}/index.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV-LEGAL spec at f{EXPORT_DPV_LEGAL_HTML_PATH}/index.html')
with open(f'{EXPORT_DPV_LEGAL_HTML_PATH}/dpv-legal.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote DPV-LEGAL spec at f{EXPORT_DPV_LEGAL_HTML_PATH}/dpv-legal.html')

DEBUG('--- END ---')