#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''This script parses CSV files and generates RDF serialisations from it'''

import csv
from collections import namedtuple
import json
# [RDFLib](https://rdflib.readthedocs.io/en/stable/) library required
from rdflib import Graph, Namespace
from rdflib import RDF, RDFS, OWL, SKOS, DCTERMS, SDO, VANN
from rdflib.compare import graph_diff
from rdflib.term import Literal, URIRef, BNode

import logging
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

# [[vocab_management.py]] contains:
# [namespaces](vocab_management.html#namespaces),
# [CSV contents and paths](vocab_management.html#csv-files),
# [criteria for accepted terms](vocab_management.html#term-statuses),
# [serialisation export configuration](vocab_management.html#serialisations),
# [translation import configuration](vocab_management.html#translations),
# [export paths and configuration](vocab_management.html#export)
from vocab_management import *

# [[vocab_schemas.py]] contains information 
# on how the spreadsheets are structured and how to parse them 
# using python functions defined in [[vocab_funcs.py]]
import vocab_schemas

# == DATA ==

# `PROPOSED` will hold the proposed concepts.
PROPOSED = {}
# E.g. structure
__examples = { '<vocab>': ['dpv:Concept']}

# === translations ===
TRANSLATIONS = {}
# The languages to be translated are
# as per [vocab_management.IMPORT_TRANSLATIONS
# ](vocab_management.html#translations).
# Example  of translated concept -
__example = { 'dpv:Concept': ['<ISO 3166-2 code>'] }

# === translations-missing ===
MISSING_TRANSLATIONS = {}
# `MISSING_TRANSLATIONS` will hold concepts that don't
# have translations, saved to file as per [vocab_management
# ](vocab_management.html#translations)
# Example  of missing concept -
__example = {
    'dpv:Concept': {
        '<ISO 3166-2 code>': {
            'label': 'translated label',
            'definition': 'translated definition',
            'usage': 'translated usage note', # if it exists
            'status': '[verified or unverified]'
        }
    }
}

### Loading Data

#### Load CSV Data
def load_CSV(filepath:str) -> (list, dict):
    '''`load_CSV` will parse CSV and return header (schema) and other rows,
    with cleaned fields (strips out empty space) and truncating cells
    in rows to what is defined in the header. Google Sheets export has an
    issue where empty cells are added in rows (e.g. ",,,,") - to correct
    this, for each row only the number of columns as per the header row
    are extracted and used. The returned data contains header list with
    field names from header row, and a dict with keys as header fields
    and values as the row values'''
    with open(filepath) as fd:
        csvreader = csv.reader(fd)
        # First row contains header/labels, which give the count of 
        # attributes to extract from each row.
        # CAUTION: Google Sheets mangles the CSV where there are empty 
        # columns in the row towards the end. To fix this, we presume
        # there are no empty headers in the CSV.
        header = [x for x in next(csvreader) if x]
        count = len(header)
        terms = []
        for row in csvreader:
            if len(row) == 0 or not row[0].strip(): # skip empty rows
                continue
            row = [
                term.strip() 
                for term in row[:count]] # extract nos of header columns
            rowdata = {}
            for index, item in enumerate(row):
                rowdata[header[index]] = row[index] # dict of rows values
            terms.append(rowdata)
    return header, terms


#### Load Translations from CSV
# This module-level code loads the translated concepts
# from the spreadsheets into [translations](#translations). The languages
# and filepaths are taken from 
# [vocab_management](vocab_management.html#translations)
# where `lang` is the ISO 3166-2 code and `lang_data_ contains the
# `lang` language name (e.g. English), `prod` to denote translations
# that are verified, and `verify` for unverified translations.
for lang, lang_data in IMPORT_TRANSLATIONS.items():
    def _convert(term:dict) -> dict:
        '''`_convert` is a convenience function that refactors
        common code to extract translations'''
        translated = {}
        translated['label'] = term['Label_translated']
        translated['definition'] = term['Definition_translated']
        if term['Usage_translated'] != 'N/A':
            translated['usage'] = term['Usage_translated']
        return translated

    # Add production-ready translations with `status: verified`
    header, csvdata_prod = load_CSV(lang_data['prod'])
    for term in csvdata_prod:
        if term['Term'] not in TRANSLATIONS:
            TRANSLATIONS[term['Term']] = {}
        TRANSLATIONS[term['Term']][lang] = _convert(term)
        TRANSLATIONS[term['Term']][lang]['status'] = 'verified'
    # Add production-ready translations with `status: unverified`
    header, csvdata_verify = load_CSV(lang_data['verify'])
    for term in csvdata_verify:
        if term['Term'] not in TRANSLATIONS:
            TRANSLATIONS[term['Term']] = {}
        TRANSLATIONS[term['Term']][lang] = _convert(term)
        TRANSLATIONS[term['Term']][lang]['status'] = 'unverified'
    INFO(f"Loaded translations for {lang_data['lang']}: {len(csvdata_prod)} verified, {len(csvdata_verify)} unverified")


# == export ==

def write_CSV_graph(graph, filepath: str, vocab: str, namespace: str) -> None:
    '''Write a CSV file for the given graph at filepath'''
    def _consolidate(item: list) -> list:
        items = set()
        for item in item.split(';'):
            if not item.startswith('https://w3id.org/dpv'): continue
            items.add(item)
        return ";".join(items)

    query_header = ('iri', 'label', 'definition', 
        'dpvtype', 'subclassof', 'hasbroader',
        'scopenote', 'created', 'modified')
    header = ('term', 'type', *query_header, 'vocab', 'namespace')
    with open(f'{filepath}.csv', 'w') as fd:
        writer = csv.writer(fd)
        writer.writerow(header)
        query = """
            SELECT ?iri ?label ?definition
                (group_concat(?type; separator=";") as ?types)
                (group_concat(DISTINCT STR(?parent); separator=";") as ?subclassof)
                (group_concat(DISTINCT STR(?broader); separator=";") as ?hasbroader)
                (group_concat(DISTINCT STR(?note); separator=";") as ?scopenote)
                ?created ?modified
            WHERE {
                ?iri a skos:Concept .
                ?iri skos:prefLabel ?label .
                ?iri rdf:type ?type .
                OPTIONAL { ?iri dct:created ?created } .
                OPTIONAL { ?iri skos:definition ?definition } .
                OPTIONAL { ?iri rdfs:subClassOf ?parent } .
                OPTIONAL { ?iri skos:broader ?broader } .
                OPTIONAL { ?iri skos:scopeNote ?note } .
                OPTIONAL { ?iri dct:modified ?modified } .
            } GROUP BY ?iri ?label ORDER BY ?iri
        """
        results = graph.query(query)
        for row in results:
            if not row[0].startswith('https://w3id.org/dpv'): continue
            value = {
                'term': prefix_from_iri(row[0]).split(':')[1],
                'vocab': prefix_from_iri(row[0]).split(':')[0],
                'namespace': row[0].split('#')[0],
                }
            for index, item in enumerate(row):
                value[query_header[index]] = item
            if 'rdf-schema#Class' in value['dpvtype']:
                value['type'] = 'class'
            elif 'rdf-syntax-ns#Property' in value['dpvtype']:
                value['type'] = 'property'
            else:
                raise Exception(f"Unknown type: {value['dpvtype']} in {value['term']}")
            for key in (('dpvtype', 'subclassof', 'hasbroader')):
                value[key] = _consolidate(value[key])

            writer.writerow((value[x] for x in header))
    INFO(f'wrote {filepath}.csv')


def write_rights_mapping_CSV_graph(graph, filepath: str, vocab: str, namespace: str) -> None:
    '''Write a CSV file for the given graph at filepath'''
    header = ('legal_basis', 'right')
    with open(f'{filepath}.csv', 'w') as fd:
        writer = csv.writer(fd)
        writer.writerow(header)
        query = """
            SELECT ?legal_basis ?right
            WHERE {
                ?legal_basis dpv:hasRight ?right
            } ORDER BY ?legal_basis ?right
        """
        results = graph.query(query)
        for row in results:
            writer.writerow(row)
    INFO(f'wrote {filepath}.csv')


# === serialise-RDF ===
def serialize_graph(triples:list, filepath:str, vocab:str, hook:str=None) -> None:
    '''`serialize_graph` serializes triples at filepath with defined 
    formats from `vocab_management.RDF_SERIALIZATIONS`. `hook` defines
    a string key which is used to retrieve SPARQL queries for the
    provided graph e.g. to add/delete/update triples'''
    graph = Graph()
    for prefix, namespace in NAMESPACES.items():
        graph.namespace_manager.bind(prefix, namespace)
    for triple in triples:
        graph.add(triple)

    # **Hooks** are SPARQL queries associated with specific vocabs or modules.
    # If any are present, they are called here to update the graph.
    # Hooks can insert, update, or delete triples in the graph.
    if hook in RDF_EXPORT_HOOK:
        for data in RDF_EXPORT_HOOK[hook]:
                DEBUG(f"Applying hook {data['title']} for {vocab}")
                graph.update(data['query'])
        DEBUG(f"Updated graph with {len(RDF_EXPORT_HOOK[hook])} queries")

    # Add **ontology metadata**, retrieve manual metadata from `RDF_VOCABS`
    # in [[vocab_management.py]] and programmatically add other metadata.
    metadata = RDF_VOCABS[vocab]['metadata']
    vocab_iri = URIRef(str(NAMESPACES[vocab])[:-1]) # strip last character
    graph.add((vocab_iri, RDF.type, OWL.Ontology))
    graph.add((vocab_iri, OWL.versionIRI, URIRef(vocab_iri.replace('https://w3id.org/dpv', f'https://w3id.org/dpv/{DPV_VERSION}'))))
    graph.add((vocab_iri, DCTERMS.source, URIRef("https://www.w3.org/groups/cg/dpvcg/")))
    graph.add((vocab_iri, DCTERMS.title, Literal(metadata['dct:title'], lang='en')))
    # https://github.com/oeg-upm/fair_ontologies/issues/108
    # bibo:status needs a literal to not fail FOOPS!
    graph.add((vocab_iri, BIBO.status, Literal(BIBO[f'status/{metadata["bibo:status"]}'])))
    graph.add((vocab_iri, RDFS.Label, Literal(vocab.upper(), lang='en')))
    graph.add((vocab_iri, DCTERMS.description, Literal(metadata['dct:description'], lang='en')))
    graph.add((vocab_iri, DCTERMS.created, Literal(metadata['dct:created'], lang='en')))
    graph.add((vocab_iri, DCTERMS.issued, Literal(metadata['dct:created'], lang='en')))
    if 'dct:modified' in metadata:
        graph.add((vocab_iri, DCTERMS.modified, Literal(metadata['dct:modified'], lang='en')))
    for creator in metadata['dct:creator'].split(','):
        graph.add((vocab_iri, DCTERMS.creator, Literal(creator.strip(), lang='en')))
    graph.add((vocab_iri, SDO.version, Literal(metadata['schema:version'])))
    graph.add((vocab_iri, OWL.versionInfo, Literal(metadata['schema:version'])))
    graph.add((vocab_iri, DCTERMS.identifier, Literal(vocab_iri)))
    graph.add((vocab_iri, DCTERMS.conformsTo, Literal(str(RDFS)[:-1])))
    graph.add((vocab_iri, DCTERMS.conformsTo, Literal(str(SKOS)[:-1])))
    graph.add((vocab_iri, BIBO.doi, Literal("10.5281/zenodo.12505841")))
    graph.add((vocab_iri, DCTERMS.bibliographicCitation, Literal("Data Privacy Vocabulary (DPV) -- Version 2. Harshvardhan J. Pandit, Beatriz Esteves, Georg P. Krog, Paul Ryan, Delaram Golpayegani, Julian Flake https://doi.org/10.48550/arXiv.2404.13426")))
    graph.add((vocab_iri, DCTERMS.publisher, URIRef("https://www.w3.org/")))
    graph.add((vocab_iri, FOAF.logo, URIRef("https://w3id.org/dpv/media/logo.png")))
    for lang in IMPORT_TRANSLATIONS:
        graph.add((vocab_iri, DCTERMS.language, Literal(lang)))
    # Contributor are collected from all concept contributors
    contributors = set()
    results = list(graph.triples((None, NAMESPACES['dct'].contributor, None)))
    for _, _, persons in results:
        persons = persons.replace(';', ',')
        for person in persons.split(','):
            contributors.add(person.strip())
    for person in contributors:
        graph.add((vocab_iri, DCTERMS.contributor, Literal(person)))
    # TODO: dct:hasFormat/dct:isFormatOf - defined for each serialisation
    # TODO: dct:hasVersion/dct:isVersionOf - between RDFS/SKOS and OWL variants
    graph.add((
        vocab_iri, DCTERMS.license, 
        URIRef('https://www.w3.org/copyright/document-license-2023/')))
    graph.add((vocab_iri, VANN.preferredNamespacePrefix, Literal(vocab)))
    graph.add((vocab_iri, VANN.preferredNamespaceUri, Literal(NAMESPACES[vocab])))
    # Profile metadata
    graph.add((vocab_iri, RDF.type, PROFILE.Profile))
    graph.add((vocab_iri, PROFILE.isProfileOf, RDFS['']))
    graph.add((vocab_iri, PROFILE.isProfileOf, SKOS['']))
    if metadata['profile:isProfileOf']:
        graph.add((vocab_iri, PROFILE.isProfileOf, URIRef(str(NAMESPACES[metadata['profile:isProfileOf']])[:-1])))
    # Add links to guides, primer, examples
    graph.add((vocab_iri, PROFILE.hasResource, URIRef('https://w3id.org/dpv/primer')))
    graph.add((URIRef('https://w3id.org/dpv/primer'), PROFILE.hasRole, ROLE.guidance))
    graph.add((URIRef('https://w3id.org/dpv/primer'), RDF.type, PROFILE.ResourceDescriptor))
    graph.add((URIRef('https://w3id.org/dpv/primer'), PROFILE.hasArtifact, URIRef('https://w3id.org/dpv/primer')))
    graph.add((URIRef('https://w3id.org/dpv/primer'), DCTERMS.title, Literal("Primer for Data Privacy Vocabulary")))
    graph.add((URIRef('https://w3id.org/dpv/primer'), DCTERMS.format, URIRef("https://www.iana.org/assignments/media-types/text/html")))
    graph.add((URIRef('https://w3id.org/dpv/primer'), DCTERMS.conformsTo, URIRef("https://www.w3.org/TR/html/")))

    graph.add((vocab_iri, PROFILE.hasResource, URIRef('https://w3id.org/dpv/guides')))
    graph.add((URIRef('https://w3id.org/dpv/guides'), RDF.type, PROFILE.ResourceDescriptor))
    graph.add((URIRef('https://w3id.org/dpv/guides'), PROFILE.hasRole, ROLE.guidance))
    graph.add((URIRef('https://w3id.org/dpv/guides'), PROFILE.hasArtifact, URIRef('https://w3id.org/dpv/guides')))
    graph.add((URIRef('https://w3id.org/dpv/guides'), DCTERMS.title, Literal("Guides for Data Privacy Vocabulary")))
    graph.add((URIRef('https://w3id.org/dpv/guides'), DCTERMS.format, URIRef("https://www.iana.org/assignments/media-types/text/html")))
    graph.add((URIRef('https://w3id.org/dpv/guides'), DCTERMS.conformsTo, URIRef("https://www.w3.org/TR/html/")))

    graph.add((vocab_iri, PROFILE.hasResource, URIRef('https://w3id.org/dpv/examples')))
    graph.add((URIRef('https://w3id.org/dpv/examples'), RDF.type, PROFILE.ResourceDescriptor))
    graph.add((URIRef('https://w3id.org/dpv/examples'), PROFILE.hasRole, ROLE.guidance))
    graph.add((URIRef('https://w3id.org/dpv/examples'), PROFILE.hasArtifact, URIRef('https://w3id.org/dpv/examples')))
    if vocab != 'dex':
        graph.add((URIRef('https://w3id.org/dpv/examples'), DCTERMS.title, Literal(RDF_VOCABS['dex']['metadata']['dct:title'])))
    graph.add((URIRef('https://w3id.org/dpv/examples'), DCTERMS.format, URIRef("https://www.iana.org/assignments/media-types/text/html")))
    graph.add((URIRef('https://w3id.org/dpv/examples'), DCTERMS.conformsTo, URIRef("https://www.w3.org/TR/html/")))

    # HTML specification
    artifact = URIRef(vocab_iri + f'#serialisation-html')
    graph.add((artifact, RDF.type, PROFILE.ResourceDescriptor))
    graph.add((vocab_iri, PROFILE.hasResource, artifact))
    graph.add((artifact, PROFILE.hasRole, ROLE.specification))
    graph.add((artifact, PROFILE.hasArtifact, URIRef(f'{vocab_iri}/{vocab}.html')))
    graph.add((artifact, DCTERMS.format, URIRef(IANA_TYPES['html']['format'])))
    graph.add((artifact, DCTERMS.conformsTo, URIRef(IANA_TYPES['html']['standard'])))
    graph.add((artifact, DCTERMS.title, Literal(f"{metadata['dct:title']} - {IANA_TYPES['html']['title']} serialiation")))
    # RDF resources
    for ext, format in RDF_SERIALIZATIONS.items():
        artifact = URIRef(vocab_iri + f'#serialisation-{ext}')
        graph.add((vocab_iri, PROFILE.hasResource, artifact))
        graph.add((artifact, RDF.type, PROFILE.ResourceDescriptor))
        graph.add((artifact, PROFILE.hasRole, ROLE.vocabulary))
        if vocab == 'dpv':
            graph.add((artifact, PROFILE.hasArtifact, URIRef(f'{vocab_iri}/{vocab}/{vocab}.{ext}')))
        else:
            graph.add((artifact, PROFILE.hasArtifact, URIRef(f'{vocab_iri}/{vocab}.{ext}')))
        graph.add((artifact, DCTERMS.format, URIRef(IANA_TYPES[ext]['format'])))
        graph.add((artifact, DCTERMS.conformsTo, URIRef(IANA_TYPES[ext]['standard'])))
        graph.add((artifact, DCTERMS.title, Literal(f"{metadata['dct:title']} - {IANA_TYPES[ext]['title']} serialiation")))
    # Serialise the graph in specific formats defined in `RDF_SERIALIZATIONS`
    # from [[vocab_management.py]]
    for ext, format in RDF_SERIALIZATIONS.items():
        graph.serialize(f'{filepath}.{ext}', format=format)
    INFO(f'wrote {filepath}.[{",".join(RDF_SERIALIZATIONS)}]')

    if vocab == 'eu-gdpr' and 'legal_basis_rights_mapping' in filepath:
        write_rights_mapping_CSV_graph(graph, filepath, vocab, vocab_iri)
    elif vocab == 'dex':
        pass
    else:
        write_CSV_graph(graph, filepath, vocab, vocab_iri)

    ##### Serialise in OWL
    # - TODO: Decide format for serialising OWL variant
    # - TODO: convert to manchester syntax via external tool
    # - TODO: What IRI to use for OWL variant?
    # - TODO: Add `skos:exactMatch` between default and OWL concepts
    # - TODO: Correctly declare `AnnotationProperty` e.g. `dpv:hasName`
    # - TODO: Add domain/range values or hints
    
    # Options for IRI:

    # 1. same IRI e.g. `https://w3id.org/dpv/pd#Concept`
    # 2. different IRI e.g. `https://w3id.org/dpv/pd/owl/#Concept`
    #    where `/owl` is the suffix to distinguish owl variant
    # 3. current IRI e.g. `https://w3id.org/dpv/dpv-owl/pd#Concept`
    #    where `/dpv-owl` is the prefix to distinguish owl variant
    
    # Current implementation is #1 with the same IRI, where OWL is
    # generated at same filepath with extension {name}-owl.[ttl,owl]

    # Going with #2 above - replace IRI with suffix /owl
    graph_temp = Graph()
    
    def replace_iri_owl(iri):
        if not type(iri) == URIRef: return iri
        if not iri.startswith('https://w3id.org/dpv'): return iri
        if not '#' in iri: return iri
        # DEBUG(iri)
        namespace, term = iri.split('#')
        return URIRef(f"{namespace}/owl#{term}")

    for s, p, o in graph:
            graph_temp.add((
                replace_iri_owl(s), replace_iri_owl(p), replace_iri_owl(o)))
    graph = graph_temp
    for prefix, namespace in NAMESPACES.items():
        graph.namespace_manager.bind(prefix, namespace)

    ##### OWL semantics
    # For reference, see [Using OWL and SKOS (May 2008)
    # ](https://www.w3.org/2006/07/SWD/SKOS/skos-and-owl/master.html)

    # remove conformance with SKOS, replace with conformance to OWL2
    graph.update(f"""
        DELETE {{ <{str(vocab_iri)}> dct:conformsTo <{str(SKOS)[:-1]}> }}
        INSERT {{ 
            <{str(vocab_iri)}> dct:conformsTo <{str(OWL)[:-1]}> . 
            <{str(vocab_iri)}> dct:hasVersion <{str(vocab_iri)}> }}
        WHERE {{ <{str(vocab_iri)}> dct:conformsTo ?o }}
        """)

    # for classes, `skos:Concept` is converted to `owl:Class`
    graph.update("""
        DELETE { ?s rdf:type skos:Concept }
        INSERT { ?s rdf:type owl:Class }
        WHERE { ?s rdf:type rdfs:Class }
        """)
    # for properties, `skos:Concept` is converted to `owl:ObjectProperty`
    # - this is not correct for annotation properties such as `dpv:hasName`
    graph.update("""
        DELETE { ?s rdf:type skos:Concept }
        INSERT { ?s rdf:type owl:ObjectProperty }
        WHERE { ?s rdf:type rdf:Property }
        """)
    # remove SKOS schemes and memberships
    graph.update("""
        DELETE { ?s skos:inScheme ?o }
        WHERE { ?s skos:inScheme ?o }
        """)
    graph.update("""
        DELETE { ?s rdf:type skos:ConceptScheme }
        WHERE { ?s rdf:type skos:ConceptScheme }
        """)
    # for classes, replace `skos:broader` with `rdfs:subClassOf`
    # and `skos:narrower` with `rdfs:superClassOf` (made up relation)
    graph.update("""
        INSERT { ?s rdfs:subClassOf ?o . }
        WHERE { ?s a rdfs:Class . ?s skos:broader ?o }
        """)
    # for properties, replace `skos:broader` with `rdfs:subPropertyOf`
    # and `skos:narrower` with `rdfs:superPropertyOf` (made up relation)
    graph.update("""
        INSERT { ?s rdfs:subPropertyOf ?o . }
        WHERE { ?s a rdf:Property . ?s skos:broader ?o }
        """)
    # Delete any hanging `skos:narrower` and `skos:broader`
    graph.update("""
        DELETE { ?s skos:narrower ?o }
        WHERE { ?s skos:narrower ?o }
        """)
    graph.update("""
        DELETE { ?s skos:broader ?o }
        WHERE { ?s skos:broader ?o }
        """)
    # Update profile metadata
    graph.update(f"""
        DELETE {{ ?s profile:isProfileOf ?o }}
        INSERT {{ 
            ?s profile:isProfileOf <{str(OWL)[:-1]}> .
            ?s profile:isProfileOf <{str(vocab_iri)}> .
        }}
        WHERE {{ ?s profile:isProfileOf ?o }}
        """)
    if metadata['profile:isProfileOf']:
        graph.update(f"""
            INSERT {{ 
                ?s profile:isProfileOf <{str(NAMESPACES[metadata['profile:isProfileOf']+'-owl'])[:-1]}>
            }}
            WHERE {{ ?s profile:isProfileOf ?o }}
            """)
    # replace main vocab iri with owl vocab iri
    vocab_owl_iri = URIRef(NAMESPACES[vocab+'-owl'][:-1])
    graph.update(f"""
        DELETE {{ ?s owl:versionIRI ?o }}
        INSERT {{ <{str(vocab_owl_iri)}> owl:versionIRI <{vocab_owl_iri.replace('https://w3id.org/dpv', f'https://w3id.org/dpv/{DPV_VERSION}')}> }}
        WHERE {{  ?s owl:versionIRI ?o }}
        """)
    graph.update(f"""
        DELETE {{ <{str(vocab_iri)}> ?p ?o }}
        INSERT {{ <{str(vocab_owl_iri)}> ?p ?o }}
        WHERE {{  <{str(vocab_iri)}> ?p ?o }}
        """)
    graph.update(f"""
        DELETE {{ ?s ?p <{str(vocab_iri)}> }}
        INSERT {{ ?s ?p <{str(vocab_owl_iri)}> }}
        WHERE {{  ?s ?p <{str(vocab_iri)}> }}
        """)
    # replace artifact iris
    # graph.update(f"""
    #     DELETE {{ ?s profile:hasArtifact ?o }}
    #     WHERE {{  ?s profile:hasArtifact ?o }}
    #     """)
    for s, p, o in graph.triples((None, PROFILE.hasArtifact, None)):
        graph.remove((s, p, o))
        graph.add((s, p, URIRef(o.replace(f'{vocab}.', f'{vocab}-owl.'))))

    # For domain/range, the semantically correct use would be to
    # declare `owl:unionOf` with a `rdf:Collection` containing all
    # the possible values - HOWEVER, collections are a pain to deal
    # with, and will muck up all the code in `300 HTML` script.
    # RDFLib has covenience functions that can assist with getting
    # collections as pythonic lists - and since OWL serialisation
    # doesn't yet have a separate page and isn't parsed, this can be 
    # done here without any _damage_ as such. The question is how to
    # get the union values i.e. how to retrieve all the possible
    # values for a property's domain/range when they are spread
    # across domains and ranges.
    # Can SPARQL CONSTRUCT be used to create domain/range values
    # from existing dcam:domainIncludes/rangeIncludes?

    # Serialising OWL is done as per `vocab_management.OWL_SERIALIZATIONS`
    for ext, format in OWL_SERIALIZATIONS.items():
        graph.serialize(f'{filepath}-owl.{ext}', format=format)
    INFO(f'wrote {filepath}-owl.[{",".join(OWL_SERIALIZATIONS)}]')


# === translations-rdf ===
def add_translations_for_concept(concept):
    triples = []
    term = prefix_from_iri(concept)
    # See [translations](#translations) for terms used.
    # If term is not present in `TRANSLATIONS`, then all translations
    # are missing
    if term not in TRANSLATIONS:
        # If term is not present in `MISSING_TRANSLATIONS`, then
        # translations for all languages are missing
        if term not in MISSING_TRANSLATIONS:
            # If so, add the term with all languages as missing
            MISSING_TRANSLATIONS[term] = list(IMPORT_TRANSLATIONS.keys())
        return []

    # Term has some translations
    lang_data = TRANSLATIONS[term]
    for lang, translations in lang_data.items():
        # For unverified translations, the suffix _machine-translated_
        # is added to distinguish verified and unverified terms
        if translations['status'] == 'unverified':
            note = " (machine-translated)"
        else:
            note = ""
        triples.append((concept, SKOS.prefLabel, 
            Literal(f"{translations['label']}{note}", lang=lang)))
        triples.append((concept, SKOS.definition, 
            Literal(f"{translations['definition']}{note}", lang=lang)))
        if 'usage' in translations:
            triples.append((
                concept, SKOS.scopeNote, 
                Literal(f"{translations['usage']}{note}", lang=lang)))
    # Check if term has any missing translations for declared languages
    for lang in IMPORT_TRANSLATIONS:
        if lang not in lang_data:
            if term not in MISSING_TRANSLATIONS:
                MISSING_TRANSLATIONS[term] = []
            MISSING_TRANSLATIONS[term].append(lang)
    return triples


# === generate-triples ===
global_triples = []
# iterate over all CSV files for specific vocab e.g. dpv
for vocab, vocab_data in CSVFILES.items():
    namespace = NAMESPACES[vocab]
    INFO('-'*40)
    INFO(f'VOCAB: {vocab} ({namespace})')
    INFO('-'*40)
    vocab_triples = []
    PROPOSED[vocab] = {}
    # Each 'module' corresponds to a CSV, and is combined
    # together into a 'vocab' as per [[vocab_management.py]].
    # The file generated at the end will be for each vocab,
    # and for each module in the vocab.
    for module, module_data in vocab_data.items():
        # get schemas and data for each csv in module
        module_triples = []
        PROPOSED[vocab][module] = []
        for schema_name, filepath in module_data.items():
            # Each module (CSV) has a schema declared for how the
            # CSV is organised, which dictates which functions to
            # call to handle each row within that CSV
            schema = vocab_schemas.get_schema(schema_name)
            INFO(f'MODULE: {module}')
            INFO(f'parsing {filepath} with schema: {schema_name}')
            header, csvdata = load_CSV(filepath)
            header = [x.strip() for x in header]
            # csvdata is a list of dicts containing column:value
            for row in csvdata:
                if not row['Term']: # skip empty rows
                    continue
                row = {x.strip():y.strip() for x,y in row.items()}
                # If there is no 'Status' column in the row, then skip -
                # because it might be empty row (quirk of Google export)
                # or it might be working notes not meant to be in RDF
                if 'Status' not in row:
                    continue
                # Filter out proposed concepts - they are to be collected
                # and listed separately in another file
                if row['Status'] == 'proposed':
                    # TODO: skip rows if they don't have a status
                    PROPOSED[vocab][module].append(row['Term'])
                    continue
                # skip empty rows, annotations, deprecated concepts
                if row['Status'] not in VOCAB_TERM_ACCEPT:
                    continue
                # For each row value, call the assigned function from
                # [[vocab_schema.py]]
                for index, item in enumerate(row.values()):
                    if not item:
                        continue
                    func = schema[header[index]]
                    if func is None:
                        continue
                    module_triples += func(item, row, namespace, header[index])
        classes = []
        properties = []

        # Iterate over triples and collect lists of classes and properties.
        # Also link examples if present for the concept.
        for s, p, o in module_triples:
            if p != RDF.type: continue
            if o == RDFS.Class: classes.append(s)
            elif o == RDF.Property: properties.append(s)
            if o not in (RDFS.Class, RDF.Property): continue
            # Only add examples and translations for classes and properties
            if s in EXAMPLES:
                for ex in EXAMPLES[s]:
                    module_triples.append((s, VANN.example, DEX[ex]))
            module_triples += add_translations_for_concept(s)
            module_triples.append((s, RDFS.isDefinedBy, namespace['']))
        # Add class concepts to a ConceptScheme
        if classes:
            module_triples.append((namespace[f"{module.replace('_','-')}-classes"], RDF.type, SKOS.ConceptScheme))
            for c in classes:
                module_triples.append((c, SKOS.inScheme, namespace[f"{module.replace('_','-')}-classes"]))
        # Add property concepts to a ConceptScheme
        if properties:
            module_triples.append((namespace[f"{module.replace('_','-')}-properties"], RDF.type, SKOS.ConceptScheme))
            for p in properties:
                module_triples.append((p, SKOS.inScheme, namespace[f"{module.replace('_','-')}-properties"]))
        INFO(f'Triples: {len(module_triples)} accepted for {len(classes)} classes and {len(properties)} properties, with {len(PROPOSED[vocab][module])} proposed')

        # export module triples
        exportpath = RDF_STRUCTURE[vocab]['modules']
        filepath = f'{exportpath}/{module}'
        serialize_graph(module_triples, filepath, vocab, hook=f'{vocab}-{module}')
        vocab_triples += module_triples

    # export vocab triples
    exportpath = RDF_STRUCTURE[vocab]['main']
    filepath = f'{exportpath}/{vocab}'
    serialize_graph(vocab_triples, filepath, vocab, hook=vocab)
    INFO(f'VOCAB triples: {len(vocab_triples)} accepted, {sum((len(m) for m in PROPOSED[vocab].values()))} proposed')
    global_triples += vocab_triples

INFO('-'*40)
INFO(f'TOTAL triples: {len(global_triples)} accepted')
INFO('-'*40)

# === collated-collections ===
INFO('Creating collated collections')
INFO('-'*40)

# "collated collections" are different related concepts grouped together
# in a single RDF file for convenience. The collations are declared in
# [vocab_management.py](vocab_management.html#exports)
for collation in RDF_COLLATIONS:
    INFO(f"Collating {collation['name']}")
    triples = Graph()
    for filepath in collation['input']:
        triples.parse(filepath)
    serialize_graph(triples, collation['output'], vocab=collation['name'], hook=f'collation-{collation}')
    INFO(f"Collected {len(triples)} triples into {collation['output']}")

# === serialise-missing-translations ===
# INFO('-'*40)
# DEBUG(f"Missing translations for {len(MISSING_TRANSLATIONS)} concepts")
# with open(f"{TRANSLATIONS_MISSING_FILE}", 'w') as fd:
#     import json
#     json.dump(MISSING_TRANSLATIONS, fd, indent=2)

INFO('-'*40)