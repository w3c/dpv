#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''
SHACL validation tests
'''

# Path to data files to be validated.
# Only the .ttl files are included for convenience in debugging.
from vocab_management import EXPORT_PATH
# OVERRIDE
# EXPORT_PATH = '../2.0'

DATA_PATHS = [
    f'{EXPORT_PATH}/ai/ai.ttl',
    f'{EXPORT_PATH}/dpv/dpv.ttl',
    f'{EXPORT_PATH}/examples/dex.ttl',
    f'{EXPORT_PATH}/justifications/justifications.ttl',
    f'{EXPORT_PATH}/legal/at/legal-at.ttl',
    f'{EXPORT_PATH}/legal/be/legal-be.ttl',
    f'{EXPORT_PATH}/legal/bg/legal-bg.ttl',
    f'{EXPORT_PATH}/legal/cy/legal-cy.ttl',
    f'{EXPORT_PATH}/legal/cz/legal-cz.ttl',
    f'{EXPORT_PATH}/legal/de/legal-de.ttl',
    f'{EXPORT_PATH}/legal/dk/legal-dk.ttl',
    f'{EXPORT_PATH}/legal/ee/legal-ee.ttl',
    f'{EXPORT_PATH}/legal/es/legal-es.ttl',
    f'{EXPORT_PATH}/legal/eu/aiact/eu-aiact.ttl',
    f'{EXPORT_PATH}/legal/eu/dga/eu-dga.ttl',
    f'{EXPORT_PATH}/legal/eu/ehds/eu-ehds.ttl',
    f'{EXPORT_PATH}/legal/eu/gdpr/eu-gdpr.ttl',
    f'{EXPORT_PATH}/legal/eu/nis2/eu-nis2.ttl',
    f'{EXPORT_PATH}/legal/eu/rights/eu-rights.ttl',
    f'{EXPORT_PATH}/legal/eu/legal-eu.ttl',
    f'{EXPORT_PATH}/legal/fi/legal-fi.ttl',
    f'{EXPORT_PATH}/legal/fr/legal-fr.ttl',
    f'{EXPORT_PATH}/legal/gb/legal-gb.ttl',
    f'{EXPORT_PATH}/legal/gr/legal-gr.ttl',
    f'{EXPORT_PATH}/legal/hk/legal-hk.ttl',
    f'{EXPORT_PATH}/legal/hr/legal-hr.ttl',
    f'{EXPORT_PATH}/legal/hu/legal-hu.ttl',
    f'{EXPORT_PATH}/legal/ie/legal-ie.ttl',
    f'{EXPORT_PATH}/legal/in/legal-in.ttl',
    f'{EXPORT_PATH}/legal/is/legal-is.ttl',
    f'{EXPORT_PATH}/legal/it/legal-it.ttl',
    f'{EXPORT_PATH}/legal/jp/legal-jp.ttl',
    f'{EXPORT_PATH}/legal/kr/legal-kr.ttl',
    f'{EXPORT_PATH}/legal/li/legal-li.ttl',
    f'{EXPORT_PATH}/legal/lt/legal-lt.ttl',
    f'{EXPORT_PATH}/legal/lu/legal-lu.ttl',
    f'{EXPORT_PATH}/legal/lv/legal-lv.ttl',
    f'{EXPORT_PATH}/legal/mo/legal-mo.ttl',
    f'{EXPORT_PATH}/legal/mt/legal-mt.ttl',
    f'{EXPORT_PATH}/legal/my/legal-my.ttl',
    f'{EXPORT_PATH}/legal/nl/legal-nl.ttl',
    f'{EXPORT_PATH}/legal/no/legal-no.ttl',
    f'{EXPORT_PATH}/legal/ph/legal-ph.ttl',
    f'{EXPORT_PATH}/legal/pl/legal-pl.ttl',
    f'{EXPORT_PATH}/legal/pt/legal-pt.ttl',
    f'{EXPORT_PATH}/legal/ro/legal-ro.ttl',
    f'{EXPORT_PATH}/legal/se/legal-se.ttl',
    f'{EXPORT_PATH}/legal/sg/legal-sg.ttl',
    f'{EXPORT_PATH}/legal/si/legal-si.ttl',
    f'{EXPORT_PATH}/legal/sk/legal-sk.ttl',
    f'{EXPORT_PATH}/legal/th/legal-th.ttl',
    f'{EXPORT_PATH}/legal/tw/legal-tw.ttl',
    f'{EXPORT_PATH}/legal/us/legal-us.ttl',
    f'{EXPORT_PATH}/legal/legal.ttl',
    f'{EXPORT_PATH}/loc/loc.ttl',
    f'{EXPORT_PATH}/pd/pd.ttl',
    f'{EXPORT_PATH}/risk/risk.ttl',
    f'{EXPORT_PATH}/sector/education/sector-education.ttl',
    f'{EXPORT_PATH}/sector/finance/sector-finance.ttl',
    f'{EXPORT_PATH}/sector/health/sector-health.ttl',
    f'{EXPORT_PATH}/sector/infra/sector-infra.ttl',
    f'{EXPORT_PATH}/sector/law/sector-law.ttl',
    f'{EXPORT_PATH}/sector/publicservices/sector-publicservices.ttl',
    f'{EXPORT_PATH}/sector/sector.ttl',
    f'{EXPORT_PATH}/standards/p7012/p7012.ttl',
    f'{EXPORT_PATH}/tech/tech.ttl',
]

# Combine all files into a common single graph
from rdflib import Graph
data_graph = Graph()
for file in DATA_PATHS:
    data_graph.parse(file)

# Shapes to use as validation tests.
# There can be multiple shapes e.g. associated with specific modules.
SHAPES = [
    './shacl_shapes/term_metadata.ttl',
    './shacl_shapes/vocab_metadata.ttl',
    ]
shacl_graph = Graph()
for file in SHAPES:
    shacl_graph.parse(file)

# Apply the shapes iteratively to the data graph
from pyshacl import validate
conforms, results_graph, results_text = validate( 
    # returns (conforms:boolean, results_graph, results_text)
    data_graph=data_graph,
    shacl_graph=shacl_graph,
    ont_graph=None,
    inference='none',
    abort_on_first=False,
    )

# Load namespaces into the graph so that outputs are
# convenient to handle e.g. dpv:Concept
from vocab_management import NAMESPACES
for k, v in NAMESPACES.items():
    if k not in results_graph.namespaces():
        results_graph.bind(k, v)

# for ns in results_graph.namespaces():
#     print(ns)
# import sys
# sys.exit(0)

# If errors exist, parse them to produce actionable messages.
SPARQL_ERROR_MESSAGE = """
    prefix sh: <http://www.w3.org/ns/shacl#>
    SELECT ?node ?message ?component ?shape
    WHERE {
        ?report a sh:ValidationResult .
        ?report sh:focusNode ?node .
        ?report sh:resultMessage ?message .
        ?report sh:sourceConstraintComponent ?component ;
        sh:sourceShape ?shape ;
    }
    """
errors = results_graph.query(SPARQL_ERROR_MESSAGE)

# Ignore these errors.
# Format is for vocab, ignore specific error shapes
IGNORE_ERRORS = {
    # legal concepts e.g. laws have no definition
    'legal': ['ex:Require_SKOS_Definition'],
    'legal-at': ['ex:Require_SKOS_Definition'],
    'legal-be': ['ex:Require_SKOS_Definition'],
    'legal-bg': ['ex:Require_SKOS_Definition'],
    'legal-cy': ['ex:Require_SKOS_Definition'],
    'legal-cz': ['ex:Require_SKOS_Definition'],
    'legal-de': ['ex:Require_SKOS_Definition'],
    'legal-dk': ['ex:Require_SKOS_Definition'],
    'legal-ee': ['ex:Require_SKOS_Definition'],
    'legal-es': ['ex:Require_SKOS_Definition'],
    'legal-eu': ['ex:Require_SKOS_Definition'],
    'legal-fi': ['ex:Require_SKOS_Definition'],
    'legal-fr': ['ex:Require_SKOS_Definition'],
    'legal-gb': ['ex:Require_SKOS_Definition'],
    'legal-gr': ['ex:Require_SKOS_Definition'],
    'legal-hk': ['ex:Require_SKOS_Definition'],
    'legal-hr': ['ex:Require_SKOS_Definition'],
    'legal-hu': ['ex:Require_SKOS_Definition'],
    'legal-ie': ['ex:Require_SKOS_Definition'],
    'legal-in': ['ex:Require_SKOS_Definition'],
    'legal-is': ['ex:Require_SKOS_Definition'],
    'legal-it': ['ex:Require_SKOS_Definition'],
    'legal-jp': ['ex:Require_SKOS_Definition'],
    'legal-kr': ['ex:Require_SKOS_Definition'],
    'legal-li': ['ex:Require_SKOS_Definition'],
    'legal-lt': ['ex:Require_SKOS_Definition'],
    'legal-lu': ['ex:Require_SKOS_Definition'],
    'legal-lv': ['ex:Require_SKOS_Definition'],
    'legal-mo': ['ex:Require_SKOS_Definition'], 
    'legal-mt': ['ex:Require_SKOS_Definition'],
    'legal-my': ['ex:Require_SKOS_Definition'],
    'legal-nl': ['ex:Require_SKOS_Definition'],
    'legal-no': ['ex:Require_SKOS_Definition'],
    'legal-ph': ['ex:Require_SKOS_Definition'],
    'legal-pl': ['ex:Require_SKOS_Definition'],
    'legal-pt': ['ex:Require_SKOS_Definition'],
    'legal-ro': ['ex:Require_SKOS_Definition'],
    'legal-se': ['ex:Require_SKOS_Definition'],
    'legal-sg': ['ex:Require_SKOS_Definition'],
    'legal-si': ['ex:Require_SKOS_Definition'],
    'legal-sk': ['ex:Require_SKOS_Definition'],
    'legal-th': ['ex:Require_SKOS_Definition'],
    'legal-tw': ['ex:Require_SKOS_Definition'],
    'legal-us': ['ex:Require_SKOS_Definition'],
    '<https': ['ex:VocabTitleShape'],
    'dex': ['ex:ValidTermsShape-rdf-type'],
}

# Collate errors.
# Format is: collate by vocab, then collate by error type
vocabs = {}

for node, message, component, shape in errors:
    # Ignore errors for external concepts
    if node.startswith('http'):
        if not node.startswith('https://w3id.org/dpv'):
            continue
    # Organise errors under vocabs and then by concepts
    node = node.n3(results_graph.namespace_manager)
    if ':' in node:
        vocab, term = node.split(':')
    else:
        vocab = 'default'
        term = node
    shape = shape.n3(results_graph.namespace_manager)
    if vocab in IGNORE_ERRORS and shape in IGNORE_ERRORS[vocab]:
        continue
    if vocab not in vocabs: vocabs[vocab] = {}
    if message not in vocabs[vocab]: vocabs[vocab][message] = []
    # Add error message
    vocabs[vocab][message].append(term)

# Render errors in a HTML file so it is easily accessible
# for anyone without requiring browsing the code.
OUTPUT_FILE = 'validation.html'
with open(OUTPUT_FILE, 'w') as fd:
    from jinja2 import FileSystemLoader, Environment
    template_loader = FileSystemLoader(searchpath='jinja2_resources')
    template_env = Environment(
        loader=template_loader, 
        autoescape=True, trim_blocks=True, lstrip_blocks=True)
    template = template_env.get_template('validation.jinja2')
    with open(f'{OUTPUT_FILE}', 'w+') as fd:
        if not vocabs:
            print('Validation PASSED')
            fd.write(template.render(data=vocabs,errors=False))
        else:
            print('Validation FAILED')
            fd.write(template.render(data=vocabs,errors=True))

import sys
sys.exit(1)
