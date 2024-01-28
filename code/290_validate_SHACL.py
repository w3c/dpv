#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''
SHACL validation tests
'''

# Path to data files to be validated.
# Only the .ttl files are included for convenience in debugging.
DATA_PATHS = [
    '../dpv/dpv.ttl',
    '../pd/pd.ttl',
    '../loc/loc.ttl',
    '../legal/legal.ttl',
    '../legal/us/legal-us.ttl',
    '../legal/gb/legal-gb.ttl',
    '../legal/de/legal-de.ttl',
    '../legal/ie/legal-ie.ttl',
    '../legal/eu/legal-eu.ttl',
    '../legal/eu/gdpr/eu-gdpr.ttl',
    '../legal/eu/dga/eu-dga.ttl',
    '../legal/eu/rights/eu-rights.ttl',
    '../tech/tech.ttl',
    '../risk/risk.ttl',
]

# Combine all files into a common single graph
from rdflib import Graph
data_graph = Graph()
for file in DATA_PATHS:
    data_graph.parse(file)

# Shapes to use as validation tests.
# There can be multiple shapes e.g. associated with specific modules.
SHAPES = [
    './shacl_shapes/shapes.ttl',
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

# Parse results.
# If graph conforms, exit.
if conforms:
    print('Validation PASSED')
    import sys
    sys.exit(0)
else:
    print('Validation FAILED')

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
    'legal-eu': ['ex:Require_SKOS_Definition'],
    'legal-de': ['ex:Require_SKOS_Definition'],
    'legal-us': ['ex:Require_SKOS_Definition'],
    'legal-gb': ['ex:Require_SKOS_Definition'],
    'legal-ie': ['ex:Require_SKOS_Definition'],
}

# Collate errors.
# Format is: collate by vocab, then collate by error type
vocabs = {}

for node, message, component, shape in errors:
    # Ignore errors for external concepts
    if not node.startswith('https://w3id.org/dpv'): continue
    # Organise errors under vocabs and then by concepts
    node = node.n3(results_graph.namespace_manager)
    vocab, term = node.split(':')
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
        fd.write(template.render(data=vocabs))

import sys
sys.exit(1)