#!/usr/bin/env python3
#author: Harshvardhan J. Pandit 

'''Generates ReSpec documentation for DPV using RDF and SPARQL'''

# The vocabularies are modular

EXPORT_HTML_PATH = '../guides'

import json
import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug

# JINJA2 for templating and generating HTML
from jinja2 import FileSystemLoader, Environment
JINJA2_FILTERS = {}
TEMPLATE_DATA = {}

template_loader = FileSystemLoader(searchpath='./jinja2_resources')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)
template_env.filters.update(JINJA2_FILTERS)

# Generate HTML

template = template_env.get_template('template_guides_index.jinja2')
with open(f'{EXPORT_HTML_PATH}/index.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote Guides index at f{EXPORT_HTML_PATH}/index.html')

template = template_env.get_template('template_guides_owl2.jinja2')
with open(f'{EXPORT_HTML_PATH}/dpv-owl.html', 'w+') as fd:
    fd.write(template.render(**TEMPLATE_DATA))
DEBUG(f'wrote Guide for DPV-OWL at f{EXPORT_HTML_PATH}/dpv-owl.html')

DEBUG('--- END ---')