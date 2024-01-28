#!/usr/bin/env python3
#author: Harshvardhan J. Pandit 

"""
Generates documentation for DPV
"""

# This script reads RDF, creates an in-memory `dict` holding
# all concepts, and then uses it to produce HTML by using
# Jinja templates - which is essentially HTML with some logic
# that Jinja uses to populate based on passed data.

import json
from rdflib import Graph, Namespace, BNode, Literal
from rdflib import RDF, RDFS, OWL, SKOS
from rdflib import URIRef
import shutil
import logging
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

# [[vocab_management.py]] contains:
# [namespaces](vocab_management.html#namespaces),
# [RDF contents and paths](vocab_management.html#csv-files),
# [criteria for accepted terms](vocab_management.html#term-statuses),
# [serialisation export configuration](vocab_management.html#serialisations),
# [translation import configuration](vocab_management.html#translations),
# [export paths and configuration](vocab_management.html#export)
from vocab_management import *

# == DATA class ==

class DATA(object):
    """
    The DATA class holds the data loaded from RDF files and makes it
    accessible as python dicts. It also provides functions to load the
    data at vocab and module levels.
    """

    # === data-dicts ===

    # `data` holds a dict for each vocabulary
    data = {}
    # `modules` holds a dict for each vocabulary and then a dict for
    # modules within that vocabulary
    modules = {}
    # `schemes` holds concept schemes (this isn't currently used)
    schemes = {}
    # `concepts` is a dict acting as a lookup table for all concepts
    # parsed - they keys are full IRI and prefixed notation with
    # the same dict as value
    concepts = {}
    # concepts_prefixed = {}
    
    # === load-vocab ===
    @staticmethod
    def load_vocab(filepath:str, vocab:str) -> None:
        """
        loads the RDF triples from specified filepath and saves it
        in DATA dicts under the vocab namespace
        """
        INFO(f'loading {vocab} data from {filepath}')
        graph = Graph()
        graph.parse(filepath)
        graph.ns = { k:v for k,v in NAMESPACES.items() }
        vocab_data = {}
        for s, p, o in graph:
            # ==== parse-subject ====

            # check if this is the vocab IRI
            # if len(s) < len(NAMESPACES[vocab]): continue
            # n3 gets prefix:term using the n3 notation
            # which makes it easier to directly look up terms
            # rather than using the full IRIs
            term = s.n3(graph.namespace_manager)
            if term not in DATA.concepts: # first occurence
                # DATA.concepts is a dict holding all concepts that 
                # are parsed. Keys are IRIs and prefixed notations -
                # duplicates with reference to the same dict as value,
                # to make it easy to lookup terms by either way.
                # Each entry value contains:
                DATA.concepts[term] = {
                    # `iri`: the full IRI
                    'iri': s,
                    # `prefixed`: the prefixed form i.e. ns:Term
                    'prefixed': term, 
                    # `prefix`: the prefix i.e ns
                    'prefix': term.split(':')[0],
                    # `term`: the term i.e. IRI without ns
                    'term': term.split(':')[1],
                    # `vocab`: vocab name as passed in param
                    'vocab': vocab,
                    # `namespace`: ns IRI i.e. without the term
                    'namespace': s.replace(term.split(':')[1], ''),
                    # `_dpvterm`: boolean stating if term is in any DPV vocab
                    '_dpvterm': s.startswith('https://w3id.org/dpv'),
                    # `_termsource`: vocabs where this term is used
                    '_termsource': set(),
                    '_ignored': term in IGNORED_TERMS,
                }
                # for DPV terms, the `term` is set to non-prefixed 'Term'
                # and for non-DPV terms, it is set to prefixed 'ns:Term'
                # to visually see they are external
                # if DATA.concepts[term]['_dpvterm'] is False:
                #     DATA.concepts[term]['term'] = term
                DATA.concepts[s] = DATA.concepts[term]
            term = DATA.concepts[term]
            term['_termsource'].add(vocab)
            vocab_data[term['prefixed']] = term

            if f'{s}#' == NAMESPACES[vocab]:
                term['_type'] = 'metadata'
                term['vocab'] = vocab
                term['namespace'] = NAMESPACES[vocab]
                term['prefix'] = vocab
                DATA.data[f'{vocab}-metadata'] = term

            # ==== parse-predicate ====

            # For properties and objects, the term dict contains the
            # prefixed form as key, e.g. skos:prefLabel of Term will
            # be saved as `ns:Term: { 'skos:prefLabel': <value> }`.
            rel = p.n3(graph.namespace_manager)
            if p in term:
                # If there are multiple values for a given property,
                # then they are stored as a list under the same key.
                if type(term[p]) is list:
                    # There are two variations for the keys,
                    # full IRI and prefixed form - so that the
                    # term's properties can be accessed using both
                    # the IRI and the prefixed forms as keys
                    term[p].append(o)
                    term[rel].append(o)
                else:
                    term[p] = [term[p], o]
                    term[rel] = [term[rel], o]
            else:
                term[p] = o
                term[rel] = o

            # ==== parse-object ====

            # Objects can be DPV terms, external terms, or literals.
            if type(o) is not Literal:
                obj = o.n3(graph.namespace_manager)
                # For DPV and existing terms - they may already be present
                # in the data dicts or this could be their first occurence,
                # in which case they won't have any metadata.
                # Whenever their declaration is parsed, the existing dict 
                # gets updated with the metadata (label, etc.).
                # For new concepts, the metadata stored is the same as 
                # the earlier new term metadata
                if obj not in DATA.concepts:
                    DATA.concepts[obj] = {
                        'iri': o,
                        'prefixed': obj,
                        'prefix': obj.split(':')[0],
                        'term': obj.split(':')[1],
                        'vocab': vocab,
                        'namespace': o.replace(obj.split(':')[1], ''),
                        '_dpvterm': o.startswith('https://w3id.org/dpv'),
                        '_termsource': set(),
                        '_ignored': obj in IGNORED_TERMS,
                    }
                    DATA.concepts[obj]['_termsource'].add(vocab)
                    # If this is an external concept, the term should
                    # be used with prefixed notation
                    # if DATA.concepts[obj]['_dpvterm'] is False:
                    #     DATA.concepts[obj]['term'] = obj
                    DATA.concepts[o] = DATA.concepts[obj]
                if p == RDF.type and o == RDFS.Class:
                    term['_type'] = "class"
                elif p == RDF.type and o == RDF.Property:
                    term['_type'] = "property" 
                elif p == SKOS.inScheme:
                    if obj not in DATA.schemes:
                        DATA.schemes[obj] = {}
                    DATA.schemes[obj][term['prefixed']] = term
            else: # obj is a literal
                if type(o) == BNode:
                    # TODO: handling BNodes is icky at the moment
                    obj = o
                else:
                    obj = str(o)

        # `vocab_data` is the collection of terms in a vocab,
        # stored under `vocab` key in `DATA.data`
        DATA.data[vocab] = vocab_data
        for concept in vocab_data.values():
            if '_type' not in concept: # term is neither class/property
                concept['_type'] = 'notcp'
            # For literals with text, there can be multiple languages.
            # For each term's properties with multiple languages,
            # construct `{prop: {'lang': 'value'}}`
            for prop in (
                    'skos:prefLabel', 'skos:definition', 'skos:scopeNote'):
                if prop not in concept: continue # unsupported text
                concept[prop] = ensure_list(concept[prop])
                languages = {}
                for prop_value in concept[prop]:
                    if prop_value.language is None: # default lang is EN
                        concept[f'{prop}-en'] = concept[prop]
                        continue
                    if prop_value.language in languages: continue
                    else:
                        languages[prop_value.language] = prop_value
                for language, value in languages.items():
                    concept[f'{prop}-{language}'] = value
                concept[prop] = languages['en']

    # ==== load-module ====
    @staticmethod
    def load_module(filepath:str, module:str, vocab:str) -> None:
        """
        loads the RDF triples from specified filepath and saves it
        in DATA dicts under the vocab/module namespace
        """
        INFO(f'loading {vocab}:{module} data from {filepath}')
        graph = Graph()
        graph.parse(filepath)
        graph.ns = { k:v for k,v in NAMESPACES.items() }
        module_data_temp = {}
        # For modules, only the list of concepts is to be generated,
        # since all the actual data needed would have been parsed from
        # the `load_vocab` and be available in the dicts.
        # Modules are a 'grouping of concepts' - they are useful to
        # generate the HTML sections and dedicated pages.
        # Each module contains the specified structure
        module_data = {
            # `metadata`: about the module with prefix to use
            'metadata': {'prefix': vocab, 'name': {module}},
            # `classes`: list of classes in module
            'classes': {},
            # `properties`: list of properties in module
            'properties': {},
            # `schemes`: list of concept schemes in module
            'schemes': {},
        }
        # Modules are stored under the `vocab` they belong to
        # such that `DATA.modules[vocab]` gives all the modules
        # within that vocab
        if vocab not in DATA.modules:
            DATA.modules[vocab] = {}
        DATA.modules[vocab][module] = module_data
        # Populate the classes/properties in module
        for s, _, _ in graph:
            if len(s) < len(NAMESPACES[vocab]): continue # vocab IRI
            term = s.n3(graph.namespace_manager)
            if term.startswith('_'): # BNode
                continue
            term = DATA.concepts[term]
            # Each term records which modules it belongs to via `module`
            if 'module' not in term:
                term['module'] = []
            if module not in term['module']:
                term['module'].append(module)
            if term['_type'] == 'class':
                module_data['classes'][term['prefixed']] = term
            elif term['_type'] == 'property':
                module_data['properties'][term['prefixed']] = term
        # Populate the concept schemes
        if f'{vocab}:{module}-classes' in DATA.schemes:
            scheme = DATA.schemes[f'{vocab}:{module}-classes']
            module_data['schemes']['classes'] = scheme
        if f'{vocab}:{module}-properties' in DATA.schemes:
            scheme = DATA.schemes[f'{vocab}:{module}-properties']


# == Helper Functions ==

def get_concept_list(term:list) -> list:
    """
    get list of concepts for the list of terms provided - 
    the concepts are sorted by IRI
    """
    if not term:
        return []
    if not type(term) is list:
        term = [term]
    return sorted(
        [DATA.concepts[item] for item in term], 
        key=lambda x: x['iri'])

# === Hierarchy ===

def get_hierarchy(term:dict, relation:str) -> list:
    """
    Generic function to return the hierarchy emanating from the
    term based on the provided relation. For parents the relation is `skos:broader`, and for children it is `skos:narrower`.
    """
    if relation not in term: return []
    terms = term[relation]
    terms = ensure_list(terms)

    # The documentation assumes relation=parents/ancestor to write
    # the algorithm. Otherwise relation can also be children.
    # `ancestor_set` ensures each ancestor is only 'found' once as there
    # can be multiple paths to the same ancestor from multiple parents
    ancestor_set = set()
    ancestory = []
    
    # `_get_ancestor` returns the last/highest ancestor for a given
    # concept, defined as a term with no further parents.
    # This allows accessing the 'top concept' within that term's 
    # taxonomy, and is useful to declare in term description tables.
    # The `ancestorlist` is a mutable list of parents/ancestors
    # passed in each recursion as the term checks its parents,
    # until there are no more parents - at which point the 'path'
    # from term to ancestor is in the `ancestorlist`, and which is
    # added to `ancestory`.
    def _get_ancestor(term:dict, ancestorlist:list) -> None:
        '''helper function to get list of ancestors for given term'''
        # If there are no parents, this is the ancestor.
        # Add the list of ancestors to ancestory and return.
        if relation not in DATA.concepts[term]:
            ancestory.append(ancestorlist)
            return
        # There are parents, so see if they have ancestors.
        # If there are multiple parents, there are multiple
        # possible ancestors - so copy the current ancestorlist
        # and delve deeper recursively for each parent
        parents = DATA.concepts[term][relation]
        if type(parents) is list:
            for parent in parents:
                ancestor_set.add(parent)
                parentlist = ancestorlist.copy()
                parentlist.append(parent)
                _get_ancestor(parent, parentlist)
        else:
            ancestorlist.append(parents)
            ancestor_set.add(parents)
            _get_ancestor(parents, ancestorlist)
    for parent in terms:
        _get_ancestor(parent, [parent])
    # To ensure only the unique paths are recorded, filter
    # the parentlists based on whether the first term has not 
    # already been registered as an parent/ancestor for another
    # term i.e. for a path A->B->C, ensure another path B->C 
    # doesn't show up as it would be a 'duplicate'.
    ancestorlist = [
        parentlist for parentlist in ancestory
        if parentlist[0] not in ancestor_set]
    ancestory = [] # retrieve parent concepts from DATA
    for parentlist in ancestorlist:
        ancestory.append([DATA.concepts[parent] for parent in parentlist])
    return ancestory


# ==== Parent Hierarchy ====
def get_parent_hierarchy(term:dict) -> list:
    """
    get hierarchy of parents/ancestors for given term.
    Parents are defined using `skos:broader`
    """
    return get_hierarchy(term, 'skos:broader')


# ==== Children Hierarchy ==== 
def get_children_hierarchy(term):
    """
    Get a hierarchy of all children for the given term.
    Children are defined using `skos:narrower`
    """
    return get_hierarchy(term, 'skos:narrower')


# ==== Organise into hierarchy ====
def organise_hierarchy(terms:list, top:str=None) -> dict:
    """
    Organise the given list of terms into a hierarchy.
    `terms` is a list of terms to be organised into a hierarchy,
    `top` is the optional top concept - if provided then only
    those terms that are organised under it will be returned.
    returns `{ parent: { children: { grandchildren: { } } } }`
    """
    data = {}
    for term in terms:
        data[term] = { 'parents': [], 'children': [] }
    # Some metadata dicts have `prefix` added amongst
    # the list of concepts - remove that.
    if 'prefix' in data:
        del data['prefix'] # this isn't a term
    # From each term, populate parents and children lists
    for key, term in terms.items():
        if 'skos:broader' in term: # has parents
            parents = term['skos:broader'] # get parents
            parents = ensure_list(parents)
            for parent in parents: # check parents are not present in terms
                if prefix_from_iri(parent) in terms:
                    data[key]['parents'].append(prefix_from_iri(parent))
                    data[prefix_from_iri(parent)]['children'].append(key)
    # Based on top, filter out terms that are not under top (as parent)
    if top is None:
        results = {k:terms[k] for k,v in data.items() if not v['parents']}
    else:
        results = {k:terms[k] for k,v in data.items() if top in v['parents']}
    # Sort the terms by IRI and return them.
    return {k:results[k] for k in sorted(results.keys(), key=str.casefold)}


# === Other Helper Functions

def get_sources(sourcestring:str) -> list:
    """
    Source strings are organised as (link,label),(link2,label2)...
    This function extracts them and returns them as a list of tuples
    containing (link,label) for each
    """
    sourcestring = sourcestring.replace('(', '').replace(')', '').split(',')
    sources = []
    for i in range(1, len(sourcestring), 2):
        sources.append((sourcestring[i], sourcestring[i-1]))
    return sources


def ensure_list(item) -> list:
    """
    Simple function that ensures item is a list or puts it in one
    """
    if type(item) is not list:
        item = [item]
    return item


def ensure_list_unique(item) -> list:
    """
    Simple function that ensures item is a list or puts it in one
    """
    item = ensure_list(item)
    if type(item[0]) != dict:
        return set(item)
    items = {}
    for x in item:
        items[x['iri']] = x
    return list(items.values())


def filter_type(itemlist:list, itemtype:str, vocab:str=None) -> list:
    """
    Filters itemlist for items that match itemtype and optionally
    limits them to specified vocab
    """
    results = []
    for item in itemlist:
        if type(item) is not dict:
            item = DATA.concepts[item]
        itemvocab = item['vocab']
        if vocab != itemvocab or 'rdf:type' not in item:
            if vocab is not None:
                continue
        parents = ensure_list(item['rdf:type'])
        for p in parents:
            prefixed = prefix_from_iri(p)
            if prefixed == itemtype:
                results.append(item)
    return results


def get_prop_with_term_domain(term:dict, vocab:str) -> list:
    """
    Retrieves properties where specified term is in the domain.
    Property domain can be the term or the term's parents/types
    """
    props = set()
    term_types = term['rdf:type']
    term_types = [str(x) for x in term_types]
    term_types.append(str(term['iri']))
    for prop in DATA.concepts.values():
        if '_type' not in prop: continue # not a useful term
        if prop['_type'] != 'property': continue
        if 'dcam:domainIncludes' not in prop: continue
        for domain in ensure_list(prop['dcam:domainIncludes']):
            for t in term_types:
                if str(domain) == t:
                    props.add(prop['prefixed'])
    return [DATA.concepts[c] for c in props]


def get_prop_with_term_range(term:dict, vocab:str) -> list:
    """
    Retrieves properties where specified term is in the range.
    Property range can be the term or the term's parents/types
    """
    props = set()
    term_types = get_parent_hierarchy(term)
    term_types = {x['iri'] for y in term_types for x in y}
    term_types.add((term['iri']))
    for prop in DATA.concepts.values():
        if '_type' not in prop: continue # not a useful term
        if prop['_type'] != 'property': continue
        if 'dcam:rangeIncludes' not in prop: continue
        for domain in ensure_list(prop['dcam:rangeIncludes']):
            for t in term_types:
                if domain == t:
                    props.add(prop['prefixed'])
    return [DATA.concepts[c] for c in props]


def expand_time_interval(term:dict, prop:str) -> str:
    """
    Takes a time interval (declared using TIME vocabulary) and
    returns a string representation. The time interval is associated
    with the `term` using the specified `prop` relation
    """
    if prop not in term:
        return ''
    intervals = ensure_list(term[prop]) # this would be a BNode
    returnset = set()
    for interval in intervals:
        interval = DATA.concepts[interval]
        returnval = ''
        # Interval starting point or N/A if none exists
        if 'time:hasBeginning' in interval:
            start = DATA.concepts[interval['time:hasBeginning']]['time:inXSDDate']
            returnval = str(start)
        else:
            returnval = 'N/A'
        returnval += '/'
        # Interval ending point or N/A if none exists
        if 'time:hasEnd' in interval:
            end = DATA.concepts[interval['time:hasEnd']]['time:inXSDDate']
            returnval += str(end)
        else:
            returnval += 'ongoing'
        returnset.add(returnval)
    return ','.join(returnset)


def sort_iris(items:list) -> list:
    """
    Helper function to sort list of IRIs
    """
    return sorted(items, key=str)


def resolve_concepts(items:str | list) -> str | list:
    """
    Helper function to take a list of IRIs or prefixed terms
    and return a list with their data from the lookup table
    """
    if type(items) is list:
        if type(items[0]) is dict: # concepts are already resolved
            return items
        return [DATA.concepts[x] for x in items]
    return DATA.concepts[items]


def retrieve_example(exampleID:str) -> tuple:
    """
    Retrieves the example specified by provided ID.
    The example contents are read from the associated file if needed.
    """
    ex = DATA.data['dex'][exampleID]
    if 'dct:source' in ex:
        with open(f"../examples/{ex['dct:source']}", 'r') as fd:
            contents = fd.read()
    else:
        contents = ex['rdf:value']
    return ex, contents


def retrieve_example_for_concept(concept:dict) -> list:
    """
    Retrieves list of examples associated with concept
    """
    if 'vann:example' not in concept:
        return []
    # Get associated examples from concept's data
    examples = ensure_list(concept['vann:example'])
    # Get prefixed notation for examples
    examples = [prefix_from_iri(ex) for ex in examples]
    # Retrieve example data
    examples = [DATA.data['dex'][ex] for ex in examples]
    # Sort examplese by IRI
    examples.sort(key=lambda x: x['iri'])
    return examples


def translation_message(concept:dict, field:str, lang:str) -> str:
    """
    Retrieves `lang` translation for `concept[field]` if present,
    otherwise returns EN text with suffix 'translation missing'
    """
    if field not in concept: return None
    if f'{field}-{lang}' not in concept:
        return f'{concept[field]} (translation missing)'
    return concept[f'{field}-{lang}']


# == HTML Export ==

# === Jinja setup ===
from jinja2 import FileSystemLoader, Environment
template_loader = FileSystemLoader(searchpath=f'{TEMPLATE_PATH}')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)

JINJA2_FILTERS = {
    'prefix_this': prefix_from_iri,
    'generate_author_affiliation': generate_author_affiliation,
    'get_concept_list': get_concept_list,
    'get_parent_hierarchy': get_parent_hierarchy,
    'get_children_hierarchy': get_children_hierarchy,
    'organise_hierarchy': organise_hierarchy,
    'get_sources': get_sources,
    'ensure_list': ensure_list,
    'ensure_list_unique': ensure_list_unique,
    'filter_type': filter_type,
    'get_prop_with_term_domain': get_prop_with_term_domain,
    'get_prop_with_term_range': get_prop_with_term_range,
    'expand_time_interval': expand_time_interval,
    'sort_iris': sort_iris,
    'resolve_concepts': resolve_concepts,
    'retrieve_example': retrieve_example,
    'retrieve_example_for_concept': retrieve_example_for_concept,
    'translation_message': translation_message,
}
template_env.filters.update(JINJA2_FILTERS)

def _write_template(
    template:str, filepath:str, filename:str,
    vocab:str, index:bool=False, lang:str="en"):
    """
    Helper function to refactor jinja output function.
    `template` is the name of the template to load.
    `filepath` is the full path of the output file.
    `filename` is the name of the file to write.
    `vocab` is the vocab name whose data will be used in output.
    `index` (default False) controls creating copy with name `index-<lang>`
    `lang` is the language to use in output (default=EN).
    The `vocab` (without -lang suffix) page is only written for EN language.
    """
    params = {
        'data': DATA.data,
        'vocab': DATA.data[vocab],
        'modules': DATA.modules[vocab],
        'vocab_name': vocab,
        'lang': lang,
        'template': template_env.get_template(template),
    }
    template = template_env.get_template(template)
    with open(f'{filepath}/{filename}-{lang}.html', 'w+') as fd:
        fd.write(template.render(**params))
        INFO(f'wrote {filename} spec at {filepath}/{filename}-{lang}.html')
    if lang == "en":
        shutil.copy(
            f'{filepath}/{filename}-{lang}.html', # src
            f'{filepath}/{filename}.html') # dest
        INFO(f'wrote {filename} spec at {filepath}/{filename}.html')
    if index:
        shutil.copy(
            f'{filepath}/{filename}-{lang}.html', # src
            f'{filepath}/index-{lang}.html') # dest
        INFO(f'wrote {filename} spec at {filepath}/index-{lang}.html')
        if lang == "en":
            shutil.copy(
                f'{filepath}/{filename}-{lang}.html', # src
                f'{filepath}/index.html') # dest
            INFO(f'wrote {filename} spec at {filepath}/index.html')


# === Load RDF data ===
for vocab, vocab_data in RDF_VOCABS.items(): 
    # Load vocab RDF data into DATA dicts
    DATA.load_vocab(vocab_data['vocab'], vocab)
    module_data = {}
    DATA.modules[vocab] = {}
    # Load the module RDF data and store it in DATA dicts
    for module, filepath in vocab_data['modules'].items():
        DATA.load_module(filepath, module, vocab)
        module_name = module.split('-')[0] # e.g. consent-type = consent
        if module_name not in module_data:
            module_data[module_name] = {}
            module_data[module_name]['index'] = {}
        module_data[module_name][module] = DATA.modules[vocab][module]
        module_data[module_name]['prefix'] = vocab
        for data in DATA.modules[vocab][module].values():
            for k, v in data.items():
                module_data[module_name]['index'][k] = v

    # === Write Vocab HTML file ===
    _write_template(
        template=vocab_data['template'],
        filepath=vocab_data["export"], filename=vocab,
        index=True, vocab=vocab, lang="en")
    for lang in IMPORT_TRANSLATIONS:
        _write_template(
            template=vocab_data['template'],
            filepath=vocab_data["export"], filename=vocab,
            index=True, vocab=vocab, lang=lang)

    # === Write Module HTML file ===
    if 'module-template' not in vocab_data:
        continue # this vocab doesn't have module specific docs
    for module, data in module_data.items():
        if module not in vocab_data['module-template']:
            INFO(f'{module} has no template associated - skipping')
            continue
        INFO(f'exporting {module} page')
        _write_template(
            template=vocab_data['module-template'][module],
            filepath=f"{vocab_data['export']}/modules", filename=module,
            index=False, vocab=vocab, lang="en")
        for lang in IMPORT_TRANSLATIONS:
            _write_template(
            template=vocab_data['module-template'][module],
            filepath=f"{vocab_data['export']}/modules", filename=module,
            index=False, vocab=vocab, lang=lang)


# == Collate Missing Translations ==
import json
# [[vocab_management.py]] declares the languages for which
# translations should exist and the paths to save the data
with open(TRANSLATIONS_MISSING_FILE, 'r') as fd:
    data = json.load(fd)
if ':' in list(data.keys())[0]: # hack to detect repeated script call
    missing = {lang:{} for lang in IMPORT_TRANSLATIONS}
    # For each concept declared in the missing translations file,
    # collect the label, definition, and (if exists) scope note
    # and save it back to the missing translations file.
    for concept, languages in data.items():
        for lang in languages:
            namespace, term = concept.split(':')
            if namespace not in DATA.data:
                DEBUG(f"ignored translations missing - external concept {concept}")
                continue
            concept = DATA.data[namespace][concept]
            missing[lang][concept['prefixed']] = {
                'label': concept['skos:prefLabel']
                }
            if 'skos:definition' in concept:
                missing[lang][concept['prefixed']]['definition'] = concept['skos:definition']
            if 'skos:scopeNote' in concept:
                missing[lang][concept['prefixed']]['usage'] = concept['skos:scopeNote']
    with open(TRANSLATIONS_MISSING_FILE, 'w') as fd:
        json.dump(missing, fd, indent=2)
        INFO(F"missing translations collected in {TRANSLATIONS_MISSING_FILE}")

INFO('*'*40)
# DEBUG(DATA.data['dpv'].keys())