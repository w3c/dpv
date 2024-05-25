#!/usr/bin/env python3

from vocab_management import generate_author_affiliation, generate_authors_affiliations
from jinja2 import FileSystemLoader, Environment
import logging
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

OUTPUT_PATH = '../examples/'

GUIDES = {
    'index': {
        'template': 'template_examples.jinja2',
        'output': 'index.html',
    },
}

template_loader = FileSystemLoader(searchpath='jinja2_resources')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)
from vocab_management import prefix_from_iri
template_env.filters.update({
    'prefix_this': prefix_from_iri,
    'generate_author_affiliation': generate_author_affiliation,
    'generate_authors_affiliations': generate_authors_affiliations,
    })

for doc, data in GUIDES.items():
    DEBUG(f'generating examples document {doc}')
    template = data['template']
    filepath = f"{OUTPUT_PATH}{data['output']}"
    with open(filepath, 'w') as fd:
        template = template_env.get_template(template)
        fd.write(template.render())
    INFO(f"wrote examples document {doc} at {filepath}")