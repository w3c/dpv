from rdflib.term import BNode, Literal
from vocab_management import *


def construct_class(item, data, namespace, header):
    triples = []
    # TODO: check for external terms
    # external terms are of type 'prefix:term'
    # They should not be declared as skos:
    item, namespace = _get_term_from_prefix_notation(item, namespace)
    triples.append((namespace[item], RDF.type, SKOS.Concept))
    triples.append((namespace[item], RDF.type, RDFS.Class))
    return triples


def construct_property(item, data, namespace, header):
    triples = []
    # TODO: check for external terms
    # external terms are of type 'prefix:term'
    # They should not be declared as skos:Concept
    item, namespace = _get_term_from_prefix_notation(item, namespace)
    triples.append((namespace[item], RDF.type, RDF.Property))
    triples.append((namespace[item], RDF.type, SKOS.Concept))
    return triples


def construct_label(item, data, namespace, header):
    triples = []
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    if ':' in data['Term'] and namespace.startswith('https://w3id.org/dpv'):
        return triples
    triples.append((namespace[term], SKOS.prefLabel, Literal(item, lang='en')))
    return triples

def contruct_definition(item, data, namespace, header):
    triples = []
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    annotation = SKOS.definition
    if data['Term'] != term: # e.g. dpv:Concept and Concept
        annotation = SKOS.scopeNote
    triples.append((namespace[term], annotation, Literal(item, lang='en')))
    return triples


def construct_parent(item, data, namespace, header):
    # parent will be of the form prefix:term
    triples = []
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    # TODO: remove dpv:Concept as a concept
    # TODO: handle taxonomy i.e. as instances of a topconcept 
    # TODO: create helper function for common parent code
    # this to avoid introducing regressions when one function
    # changes and I forget to make changes in the other
    parents = item.split(',')
    for parent in parents:
        parent = parent.strip()
        if parent == 'dpv:Concept':
            parent = NAMESPACES['skos']['Concept']
        else:
            # DEBUG(data)
            prefix, parentterm = parent.split(':')
            parent = NAMESPACES[prefix][parentterm]
        if data['ParentType'] == 'a':
            triples.append((namespace[term], RDF.type, parent))
            if parent.startswith('https://w3id.org/dpv'):
                    triples.append((namespace[term], SKOS.broader, parent))
                    if term.split(':')[0] == parent.split(':')[0]:
                        triples.append((parent, SKOS.narrower, namespace[term]))
        elif data['ParentType'] == 'sc':
            triples.append((namespace[term], RDFS.subClassOf, parent))
            if term.split(':')[0] == item.split(':')[0]: 
                triples.append((parent, RDFS.superClassOf, namespace[term]))
            if parent.startswith('https://w3id.org/dpv'):
                    triples.append((namespace[term], SKOS.broader, parent))
                    if term.split(':')[0] == item.split(':')[0]:
                        triples.append((parent, SKOS.narrower, namespace[term]))
    return triples


def construct_parent_taxonomy(item, data, namespace, header):
    # parent will be of the form prefix:term
    triples = []
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    # DEBUG(f'{term} parent taxonomy')
    # TODO: remove dpv:Concept as a concept
    
    # turn parents (if non-empty) into IRIs
    parents_raw = data['ParentTerm'].strip()
    parents_raw = parents_raw.split(',')
    parents = [] 
    for parent in parents_raw:
        parent = parent.strip()
        if not parent:
            continue
        if parent != 'dpv:Concept':
            # DEBUG(data)
            prefix, parentterm = parent.split(':')
            parent = NAMESPACES[prefix][parentterm]
        else:
            parent = RDFS.Class
        parents.append(parent)
    # DEBUG(f'parents: {parents}')
    # check type of parent to handle
    if item in ('a', 'sc'):
        for parent in parents:
            if item == 'a': # instance
                triples.append((namespace[term], RDF.type, parent))
                if parent.startswith('https://w3id.org/dpv'):
                    triples.append((namespace[term], SKOS.broader, parent))
                    if term.split(':')[0] == parent.split(':')[0]:
                        triples.append((parent, SKOS.narrower, namespace[term]))
            elif item == 'sc': # subclass
                triples.append((namespace[term], RDFS.subClassOf, parent))
                if term.split(':')[0] == parent.split(':')[0]:
                    triples.append((parent, RDFS.superClassOf, namespace[term]))
                if parent.startswith('https://w3id.org/dpv'):
                    triples.append((namespace[term], SKOS.broader, parent))
                    if term.split(':')[0] == parent.split(':')[0]:
                        triples.append((parent, SKOS.narrower, namespace[term]))
        return triples
    # parent is a topconcept
    if ',' in data['ParentType']:
        topconcepts = data['ParentType'].split(',')
    else:
        topconcepts = [data['ParentType']]
    for topconcept in topconcepts:
        prefix_top, topconcept = topconcept.split(':')
        topconcept = NAMESPACES[prefix_top][topconcept]
        triples.append((namespace[term], RDF.type, topconcept))
    # parent non-empty means not a top concept, state relation
    if not parents:
        for topconcept in topconcepts:
            prefix_top, topconcept = topconcept.split(':')
            topconcept = NAMESPACES[prefix_top][topconcept]
            triples.append((namespace[term], SKOS.broader, topconcept))
            if term.split(':')[0] == prefix_top:
                triples.append((topconcept, SKOS.narrower, namespace[term]))
            # DEBUG(f'skos {term} <-> {topconcept} topconcept')
        return triples
    for parent in parents:
        triples.append((namespace[term], SKOS.broader, parent))
        if term.split(':')[0] == parent.split(':')[0]:
            triples.append((parent, SKOS.narrower, namespace[term]))
        # DEBUG(f'skos {term} <-> {parent} parent')
    return triples


def construct_parent_property(item, data, namespace, header):
    # parent will be of the form prefix:term
    triples = []
    term = namespace[data['Term']]
    # TODO: remove dpv:Relation as a concept
    parents = item.split(',')
    for parent in parents:
        parent = parent.strip()
        if parent == 'dpv:Relation':
            continue
        else:
            prefix, parentterm = parent.split(':')
            parent = NAMESPACES[prefix][parentterm]
        triples.append((term, RDFS.subPropertyOf, parent))
        triples.append((term, SKOS.broader, parent))
        # if term.split(':')[0] == parent.split(':')[0]:
        #     triples.append((parent, RDFS.superPropertyOf, term))
        #     triples.append((parent, SKOS.narrower, term))
    return triples


def construct_domain(item, data, namespace, header):
    # domain and range are of type prefix:term
    triples = []
    domains = item.split(',')
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    for domain in domains:
        domain = domain.strip()
        if domain == "dpv:Concept":
            continue
        prefix, domainterm = domain.split(':')
        domain = NAMESPACES[prefix][domainterm]
        triples.append((namespace[term], DCAM.domainIncludes, domain))
        triples.append((namespace[term], SCHEMA.domainIncludes, domain))
    return triples


def construct_range(item, data, namespace, header):
    # range and range are of type prefix:term
    triples = []
    ranges = item.split(',')
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    for range in ranges:
        range = range.strip()
        if range == "dpv:Concept":
            continue
        prefix, rangeterm = range.split(':')
        range = NAMESPACES[prefix][rangeterm]
        triples.append((namespace[term], DCAM.rangeIncludes, range))
        triples.append((namespace[term], SCHEMA.rangeIncludes, range))
    return triples


def construct_value(item, data, namespace, header):
    triples = []
    if not item:
        return triples
    term = _term_with_namespace(data['Term'], namespace)
    triples.append((term, RDF.value, Literal(item)))
    return triples


def construct_related_terms(item, data, namespace, header):
    triples = []
    items = item.split(',')
    term = _term_with_namespace(data['Term'], namespace)
    for item in items:
        triples.append((term, SKOS.related, _term_with_namespace(item, None)))
    return triples


def construct_scope_note(item, data, namespace, header):
    triples = []
    term = _term_with_namespace(data['Term'], namespace)
    triples.append((term, SKOS.scopeNote, Literal(item, lang='en')))
    return triples


def construct_source(item, data, namespace, header):
    triples = []
    term = _term_with_namespace(data['Term'], namespace)
    items = item.split(',')
    if 'http' in item:
        iteritem = iter(items)
        for item in iteritem:
            label, url = item, next(iteritem)
            label = label.strip()
            url = url.strip()
            if label.startswith('('):
                label = label.replace('(', '', 1)
            if url.endswith(')'):
                url = url[::-1].replace(')', '', 1)[::-1] # reverse string
            node = BNode(hash_id(f'{label}{url}', 'web-', 32))
            triples.append((node, RDF.type, SCHEMA.WebPage))
            triples.append((node, SCHEMA.name, Literal(label)))
            triples.append((node, SCHEMA.url, Literal(url)))
            triples.append((term, DCT.source, node))
    else:
        for item in items:
            triples.append((term, DCT.source, Literal(item, lang='en')))
    return triples


def construct_date_created(item, data, namespace, header):
    triples = []
    term = _term_with_namespace(data['Term'], namespace)
    triples.append((term, DCT.created, Literal(item, datatype=XSD.date)))
    return triples


def construct_date_modified(item, data, namespace, header):
    triples = []
    if not item:
        return
    term = _term_with_namespace(data['Term'], namespace)
    triples.append((term, DCT.modified, Literal(item, datatype=XSD.date)))
    return triples


def construct_contributors(item, data, namespace, header):
    triples = []
    # TODO: make contributor be URI or a literal (if website available)
    term = _term_with_namespace(data['Term'], namespace)
    item = item.replace(';',',')
    for person in item.split(','):
        triples.append((term, DCT.contributor, PERSON_DICT(person)['person']))
        for triple in PERSON_DICT(person)['triples']:
            triples.append(triple)
    return triples


def construct_resolution(item, data, namespace, header):
    return []


def construct_status(item, data, namespace, header):
    if ':' in data['Term']:
        return [] # external term
    if item not in VOCAB_TERM_ACCEPT:
        return [] # status is not acceptable
    term = _term_with_namespace(data['Term'], namespace)
    return [(term, SW.term_status, Literal(item, lang='en'))]


def construct_legal_basis_rights_mapping(item, data, namespace, header):
    clause = data['Term']
    right = header
    applicable = item.strip() == 'Y'
    triples = []
    if not applicable:
        return triples
    # DEBUG(f'{clause} has right {right}')
    triples.append((namespace[clause], DPV.hasRight, namespace[right]))
    return triples



def _get_term_from_prefix_notation(term, namespace):
    if ':' in term:
        prefix, term = term.split(':')
        namespace = NAMESPACES[prefix]
    return term, namespace


def _term_with_namespace(term, namespace):
    if ':' in term:
        namespace = NAMESPACES[term.split(':')[0].strip()]
        term = namespace[term.split(':')[1].strip()]
    else:
        term = namespace[term]
    return term


def construct_iso_3166_alpha2(term, data, namespace, header):
    results = [(namespace[data['Term']], LOC.iso_alpha2, Literal(term))]
    results.append((
        namespace[data['Term']], SKOS.exactMatch, 
        Literal(f"https://www.iso.org/obp/ui/#iso:code:3166:{term}", datatype=XSD.anyURI)))
    return results


def construct_iso_3166_alpha3(term, data, namespace, header):
    results = [(namespace[data['Term']], LOC.iso_alpha3, Literal(term))]
    results.append((
        namespace[data['Term']], SKOS.exactMatch, 
        Literal(f"https://op.europa.eu/web/eu-vocabularies/concept/-/resource?uri=http://publications.europa.eu/resource/authority/country/{term}", datatype=XSD.anyURI)))
    return results


def construct_iso_3166_numeric(term, data, namespace, header):
    return [(namespace[data['Term']], LOC.iso_numeric, Literal(term))]


def construct_un_m49(term, data, namespace, header):
    return [(namespace[data['Term']], LOC.un_m49, Literal(term))]


def construct_instance(term, data, namespace, header):
    triples = []
    for parent in term.split(','):
        parent = NAMESPACES[parent.split(':')[0]][parent.split(':')[1]]
        triples.append((namespace[data['Term']], RDF.type, parent))
        triples.append((namespace[data['Term']], SKOS.broader, parent))
        triples.append((namespace[data['Term']], RDF.type, SKOS.Concept))
    return triples


def construct_skos_narrower(term, data, namespace, header):
    triples = []
    for item in term.split(','):
        item_iri = NAMESPACES[item.split(':')[0]][item.split(':')[1]]
        triples.append((namespace[data['Term']], SKOS.narrower, item_iri))
        if term.split(':')[0] == item.split(':')[0]:
            triples.append((item_iri, SKOS.broader, namespace[data['Term']]))
    return triples


def construct_skos_broader(term, data, namespace, header):
    triples = []
    for item in term.split(','):
        item_iri = NAMESPACES[item.split(':')[0]][item.split(':')[1]]
        triples.append((namespace[data['Term']], SKOS.broader, item_iri))
        if term.split(':')[0] == item.split(':')[0]:
            triples.append((item_iri, SKOS.narrower, namespace[data['Term']]))
    return triples


def construct_jurisdiction(term, data, namespace, header):
    triples = []
    for loc in term.split(','):
        loc = NAMESPACES[loc.split(':')[0]][loc.split(':')[1]]
        triples.append((namespace[data['Term']], DPV.hasJurisdiction, loc))
    return triples


def construct_webpage(term, data, namespace, header):
    triples = []
    for page in term.split(','):
        triples.append((
            namespace[data['Term']], FOAF.homepage, 
            Literal(page, datatype=XSD.anyURI)))
    return triples


def construct_law(term, data, namespace, header):
    triples = []
    for law in term.split(','):
        law = NAMESPACES[law.split(':')[0]][law.split(':')[1]]
        triples.append((
            namespace[data['Term']], DPV.hasApplicableLaw, law))
        triples.append((namespace[data['Term']], SKOS.broader, DPV.Law))
    return triples


def construct_temporal_duration(term, data, namespace, header):
    '''adds temporal duration as
    dct:temporal [ a time:ProperInterval ;
            time:hasBeginning [ 
                time:inXSDDate "YYYY-MM-DD"^^xsd:date ] ;
            time:hasEnd [
                time:inXSDDate "YYYY-MM-DD"^^xsd:date ] ; ]'''
    if not term: # no start, so no end either
        return []
    triples = []
    start = term
    end = data['End']
    interval = BNode()
    triples.append((namespace[data['Term']], DCT.temporal, interval))
    triples.append((interval, RDF.type, TIME.ProperInterval))
    dct_date = BNode()
    triples.append((interval, TIME.hasBeginning, dct_date))
    triples.append((
        dct_date, TIME.inXSDDate, Literal(term, datatype=XSD.date)))
    if end:
        dct_date = BNode()
        triples.append((interval, TIME.hasEnd, dct_date))
        triples.append((
            dct_date, TIME.inXSDDate, Literal(end, datatype=XSD.date)))
    return triples


def construct_example(term, data, namespace, header):
    return [(namespace[term], RDF.type, DEX.Example)]


def construct_dct_title(term, data, namespace, header):
    return [(namespace[data['Term']], DCT.title, Literal(term))]


def construct_dct_description(term, data, namespace, header):
    return [(namespace[data['Term']], DCT.description, Literal(term))]


def construct_example_source(term, data, namespace, header):
    source_data = data['Source']
    source_format = data['SourceFormat']
    if source_format == 'ttl':
        source_format = 'text/turtle'
    elif source_format == 'json-ld':
        source_format = 'application/ld+json'
    source_type = term
    term = namespace[data['Term']]
    triples = []
    if source_type == 'file': # source is a filepath
        triples.append((term, DCT.source, Literal(source_data, datatype=XSD.anyURI)))
    else: # source is data content
        triples.append((term, RDF.value, Literal(source_data)))
    triples.append((term, DCT['format'], Literal(source_format)))
    return triples


def add_example_concepts(term, data, namespace, header):
    concepts = term.split(',')
    triples = []
    if not concepts: return [] # return 0 triples
    for concept in concepts:
        # add concept as dct:subject of the example
        concept_namespace, concept_term = concept.split(':')
        concept_namespace = NAMESPACES[concept_namespace]
        concept = concept_namespace[concept_term]
        triples.append((namespace[data['Term']], DCT.subject, concept))
        if concept not in EXAMPLES: # add to list of examples by concept
            EXAMPLES[concept] = []
        EXAMPLES[concept].append(data['Term'])
    return triples

def construct_risk_parent_CIA(term, data, namespace, header):
    triples = []
    if 'CIA' not in data: return triples
    if 'C' in data['CIA']:
        triples.append((namespace[data['Term']], RDF.type, RISK.ConfidentialityConcept))
    if 'I' in data['CIA']:
        triples.append((namespace[data['Term']], RDF.type, RISK.IntegrityConcept))
    if 'A' in data['CIA']:
        triples.append((namespace[data['Term']], RDF.type, RISK.AvailabilityConcept))
    return triples    


def construct_risk_parent_Role(term, data, namespace, header):
    triples = []
    if 'Role' not in data: return triples
    if 'S' in data['Role']:
        triples.append((namespace[data['Term']], RDF.type, RISK.PotentialRiskSource))
    if 'R' in data['Role']:
        triples.append((namespace[data['Term']], RDF.type, RISK.PotentialRisk))
    if 'C' in data['Role']:
        triples.append((namespace[data['Term']], RDF.type, RISK.PotentialConsequence))
    if 'I' in data['Role']:
        triples.append((namespace[data['Term']], RDF.type, RISK.PotentialImpact))
    return triples    


def contruct_gdpr_right_justification(term, data, namespace, header):
    triples = []
    rights = [namespace[x.strip()] for x in term.split(',')]
    for right in rights:
        triples.append((right, DPV.hasJustification, namespace[data['Term']]))
    return triples


def p7012_term_rule(term, data, namespace, header):
    triples = []
    subject = namespace[data['Term']]
    if header == 'Permits':
        rule = DPV.hasPermission
    elif header == 'Prohibits':
        rule = DPV.hasProhibition
    elif header == 'Obligates':
        rule = DPV.hasObligation
    else:
        raise Exception(f"Unknown rule {header} in P7012 spreadsheet column")

    for item in term.split(','):
        item_namespace, item_label = item.split(':')
        item_namespace = NAMESPACES[item_namespace]
        item = item_namespace[item_label]
        triples.append((subject, rule, item))
    return triples