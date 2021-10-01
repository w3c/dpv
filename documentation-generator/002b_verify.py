#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

# ensure the output of SHACL conformance tests is true

#############################################################

# this is where the data to be validated is situated in
# file is expected to be executed from the documentation-generator folder
# (parent of folder containing this file)
# (because its less typing of cd & cd ..)
DATA_PATHS = [
    '../dpv',
    '../dpv/rdf',
    '../dpv-gdpr',
    '../dpv-gdpr/rdf',
]

# this is the list of shapes to be validated against
SHAPES = [
    './shacl_shapes/shapes.ttl',
    ]

# note that this has parameters for filepath
from os import getenv
from os import path
SHACLROOT = getenv('SHACLROOT', None)
if SHACLROOT is None:
    raise Exception('declare SHACLROOT to path containing shaclvalidate.sh')
SHACL_VALIDATION_COMMAND = {
        'shaclbinary': path.join(SHACLROOT, 'shaclvalidate.sh'),
        'shapeparam': '-shapesfile',
        # set this variable to the file containing constraints
        'shapesfile': '{param}',
        'dataparam': '-datafile',
        # set this variable to the file to be validated
        'datafile': '{param}',
        }

#############################################################

from rdflib import Graph, Namespace

SHACL = Namespace('http://www.w3.org/ns/shacl#')
SPARQL_ERROR_MESSAGE = """
    prefix sh: <http://www.w3.org/ns/shacl#>
    SELECT ?node ?message
    WHERE {
        ?report a sh:ValidationResult .
        ?report sh:focusNode ?node .
        ?report sh:resultMessage ?message .
    }
    """

def get_shacl_results(output):
    '''for each output of the SHACL validation process,
    load the graph, retrieve errors, and display messages'''
    graph = Graph()
    graph.parse(data=output, format='turtle')
    results = graph.query(SPARQL_ERROR_MESSAGE)
    print(f'{len(results)} errors found')
    for node, message in results:
        print(f'{node.n3(graph.namespace_manager)} :: {message}')



from os import walk
import subprocess


def test_shacl(folder, shape):
    print(folder)
    _, _, files = next(walk(folder))
    for file in files:
        if not file.endswith('.ttl'):
            # skip non-turtle files
            continue
        print(f'validating {file} with constraints in {shape}')
        file = path.join(folder, file)
        SHACL_VALIDATION_COMMAND['shapesfile'] = shape
        SHACL_VALIDATION_COMMAND['datafile'] = file
        # print(f'command: {" ".join(SHACL_VALIDATION_COMMAND.values())}')
        output = subprocess.run(SHACL_VALIDATION_COMMAND.values(), stdout=subprocess.PIPE)
        output = output.stdout.decode('utf-8')
        get_shacl_results(output)


#############################################################

for folder in DATA_PATHS:
    for shape in SHAPES:
        test_shacl(folder, shape)

