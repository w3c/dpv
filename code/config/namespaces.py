from filepaths import FILEPATH_CSV

NAMESPACE_CSV = (
    f'{FILEPATH_CSV}/Namespaces.csv',
    f'{FILEPATH_CSV}/Namespaces_Other.csv',
)

NAMESPACES = {}
for csvfile in NAMESPACE_CSV:
    # DEBUG(f'Extracting namespaces from {csvfile}')
    with open(csvfile, 'r') as fd:
        csvreader = csv.reader(fd)
        next(csvreader)
        for row in csvreader:
            prefix, iri = row[0], row[1]
            variable = prefix.upper().replace('-', '_')
            namespace = Namespace(iri)
            globals()[variable] = namespace
            NAMESPACES[prefix] = namespace
            if iri.startswith('https://w3id.org/dpv'):
                NAMESPACES[f'{prefix}-owl'] = Namespace(iri.replace('#', '/owl#'))
            # DEBUG(f'{prefix} namespace with IRI {iri}')

from rdflib import Graph
NS = Graph()
NS.ns = { k:v for k,v in NAMESPACES.items() }