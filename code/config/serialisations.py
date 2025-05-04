from version import DOCUMENT_STATUS

if DOCUMENT_STATUS == 'CG-FINAL':
    RDF_SERIALIZATIONS = {
        'rdf': 'xml', 
        'ttl': 'turtle', 
        'n3': 'n3',
        'jsonld': 'json-ld'
        }
    OWL_SERIALIZATIONS = RDF_SERIALIZATIONS
elif DOCUMENT_STATUS == 'CG-DRAFT':
    RDF_SERIALIZATIONS = {
        'ttl': 'turtle', 
    }
    OWL_SERIALIZATIONS = RDF_SERIALIZATIONS
else:
    raise ValueError(f"unknown {DOCUMENT_STATUS=}")

IANA_TYPES = {
    'html': {
        'title': 'HTML',
        'format': 'https://www.iana.org/assignments/media-types/text/html',
        'standard': 'https://www.w3.org/TR/html/',
    },
    'rdf': {
        'title': 'RDF/XML',
        'format': 'https://www.iana.org/assignments/media-types/application/rdf+xml',
        'standard': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    },
    'ttl': {
        'title': 'Turtle',
        'format': 'https://www.iana.org/assignments/media-types/text/turtle',
        'standard': 'https://www.w3.org/TR/turtle/',
    },
    'n3': {
        'title': 'N3',
        'format': 'https://www.iana.org/assignments/media-types/text/n3',
        'standard': 'https://www.w3.org/TeamSubmission/n3/',
    },
    'jsonld': {
        'title': 'JSON-LD',
        'format': 'https://www.iana.org/assignments/media-types/application/ld+json',
        'standard': 'https://www.w3.org/TR/json-ld11/',
    },
    'owl': {
        'title': 'OWL',
        'format': 'https://www.iana.org/assignments/media-types/application/rdf+xml',
        'standard': 'http://www.w3.org/2002/07/owl#',
    },
}