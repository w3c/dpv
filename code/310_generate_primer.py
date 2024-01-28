#!/usr/bin/env python3

from vocab_management import generate_author_affiliation, generate_authors_affiliations

OUTPUT_FILE = '../primer/index.html'
with open(OUTPUT_FILE, 'w') as fd:
    from jinja2 import FileSystemLoader, Environment
    template_loader = FileSystemLoader(searchpath='jinja2_resources')
    template_env = Environment(
        loader=template_loader, 
        autoescape=True, trim_blocks=True, lstrip_blocks=True)
    template_env.filters.update({
        'generate_author_affiliation': generate_author_affiliation,
        'generate_authors_affiliations': generate_authors_affiliations,
        })
    template = template_env.get_template('template_primer.jinja2')
    with open(f'{OUTPUT_FILE}', 'w+') as fd:
        fd.write(template.render())