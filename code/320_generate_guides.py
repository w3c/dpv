#!/usr/bin/env python3

from vocab_management import generate_author_affiliation, generate_authors_affiliations
from jinja2 import FileSystemLoader, Environment
import logging
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

OUTPUT_PATH = '../guides/'

GUIDES = {
    'index': {
        'template': 'template_guides_index.jinja2',
        'output': 'index.html',
    },
    'dpv-skos': {
        'template': 'template_guides_dpv_skos.jinja2',
        'output': 'dpv-skos.html',
    },
    'dpv-owl': {
        'template': 'template_guides_owl2.jinja2',
        'output': 'dpv-owl.html',
    },
    'dpv-misc': {
        'template': 'template_guides_dpv_miscformats.jinja2',
        'output': 'dpv-misc.html',
    },
    'dpv-odrl': {
        'template': 'template_guides_dpv_odrl.jinja2',
        'output': 'dpv-odrl.html',
    },
    'consent-27560': {
        'template': 'template_guides_consent_27560.jinja2',
        'output': 'consent-27560.html',
    },
    'privacy-notice-29184': {
        'template': 'template_guides_privacy_notice_29184.jinja2',
        'output': 'notice-29184.html',
    },
    'gdpr-ropa': {
        'template': 'template_guides_gdpr_ropa.jinja2',
        'output': 'gdpr-ropa.html',
    },
    'gdpr-dpia': {
        'template': 'template_guides_gdpr_dpia.jinja2',
        'output': 'gdpr-dpia.html',
    },
    'gdpr-data-breach': {
        'template': 'template_guides_gdpr_data_breach.jinja2',
        'output': 'gdpr-data-breach.html',
    },
    'rights': {
        'template': 'template_guides_rights.jinja2',
        'output': 'rights.html',
    },
}

template_loader = FileSystemLoader(searchpath='jinja2_resources')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)
template_env.filters.update({
    'generate_author_affiliation': generate_author_affiliation,
    'generate_authors_affiliations': generate_authors_affiliations,
    })

for guide, data in GUIDES.items():
    DEBUG(f'generating guide {guide}')
    template = data['template']
    filepath = f"{OUTPUT_PATH}{data['output']}"
    with open(filepath, 'w') as fd:
        template = template_env.get_template(template)
        fd.write(template.render())
    INFO(f"wrote guide {guide} at {filepath}")