###################### schema

import vocab_funcs

'''adds schema for each CSV'''
SCHEMA = {}
def get_schema(name):
    return SCHEMA[name]

_common_annotations = {
    'Label': vocab_funcs.construct_label,
    'Definition': vocab_funcs.contruct_definition,
    'RelatedTerms': vocab_funcs.construct_related_terms,
    'Relation': None,
    'Usage': vocab_funcs.construct_scope_note,
    'Value': vocab_funcs.construct_value,
    'Source': vocab_funcs.construct_source,
    'Created': vocab_funcs.construct_date_created,
    'Modified': vocab_funcs.construct_date_modified,
    'Status': vocab_funcs.construct_status,
    'Contributors': vocab_funcs.construct_contributors,
    'Resolution': vocab_funcs.construct_resolution, 
}

SCHEMA['classes'] = {
    '_description': 'lorem ipsum',
    'Term': vocab_funcs.construct_class,
    'ParentTerm': vocab_funcs.construct_parent,
    'ParentType': None,
}
SCHEMA['classes'].update(_common_annotations)

SCHEMA['taxonomy'] = {
    '_description': 'lorem ipsum',
    'Term': vocab_funcs.construct_class,
    'Label': vocab_funcs.construct_label,
    'Definition': vocab_funcs.contruct_definition,
    'ParentTerm': None,
    'ParentType': vocab_funcs.construct_parent_taxonomy,
    'Value': vocab_funcs.construct_value,
    'RelatedTerms': vocab_funcs.construct_related_terms,
    'Relation': None,
    'Usage': vocab_funcs.construct_scope_note,
    'Source': vocab_funcs.construct_source,
    'Created': vocab_funcs.construct_date_created,
    'Modified': vocab_funcs.construct_date_modified,
    'Status': vocab_funcs.construct_status,
    'Contributors': vocab_funcs.construct_contributors,
    'Resolution': vocab_funcs.construct_resolution, 
}

SCHEMA['properties'] = {
    '_description': 'lorem ipsum',
    'Term': vocab_funcs.construct_property,
    'Label': vocab_funcs.construct_label,
    'Definition': vocab_funcs.contruct_definition,
    'domain': vocab_funcs.construct_domain,
    'range': vocab_funcs.construct_range,
    'ParentProperty': vocab_funcs.construct_parent_property,
    'RelatedTerms': vocab_funcs.construct_related_terms,
    'Relation': None,
    'Usage': vocab_funcs.construct_scope_note,
    'Source': vocab_funcs.construct_source,
    'Created': vocab_funcs.construct_date_created,
    'CreationDate': vocab_funcs.construct_date_created, #DUPLICATE of Created 
    'Modified': vocab_funcs.construct_date_modified,
    'Status': vocab_funcs.construct_status,
    'Contributors': vocab_funcs.construct_contributors,
    'Resolution': vocab_funcs.construct_resolution, 
}

SCHEMA['legal_basis_rights_mapping'] = {
    "Term": None,
    "A13": vocab_funcs.construct_legal_basis_rights_mapping,
    "A14": vocab_funcs.construct_legal_basis_rights_mapping,
    "A15": vocab_funcs.construct_legal_basis_rights_mapping,
    "A16": vocab_funcs.construct_legal_basis_rights_mapping,
    "A17": vocab_funcs.construct_legal_basis_rights_mapping,
    "A18": vocab_funcs.construct_legal_basis_rights_mapping,
    "A20": vocab_funcs.construct_legal_basis_rights_mapping,
    "A21": vocab_funcs.construct_legal_basis_rights_mapping,
    "A22": vocab_funcs.construct_legal_basis_rights_mapping,
    "A7-3": vocab_funcs.construct_legal_basis_rights_mapping,
    "A77": vocab_funcs.construct_legal_basis_rights_mapping,
    'Status': None,
}

SCHEMA['locations'] = {
    'Term': vocab_funcs.construct_class,
    'Label': vocab_funcs.construct_label,
    'ParentTerm': None,
    'ParentType': vocab_funcs.construct_parent_taxonomy,
    'ISO-3166-Alpha2': vocab_funcs.construct_iso_3166_alpha2,
    'ISO-3166-Alpha3': vocab_funcs.construct_iso_3166_alpha3,
    'ISO-3166-Numeric': vocab_funcs.construct_iso_3166_numeric,
    'UN-M49': vocab_funcs.construct_un_m49,
    'Created': vocab_funcs.construct_date_created,
    'Modified': vocab_funcs.construct_date_modified,
    'Status': vocab_funcs.construct_status,
    'Contributors': vocab_funcs.construct_contributors,
    'Resolution': vocab_funcs.construct_resolution, 
}

SCHEMA['memberships'] = {
    'Term': vocab_funcs.construct_class,
    'Label': vocab_funcs.construct_label,
    'ParentTerm': None,
    'ParentType': vocab_funcs.construct_parent_taxonomy,
    'Members': vocab_funcs.construct_skos_narrower,
    'Start': vocab_funcs.construct_temporal_duration,
    'End': None,
    'Usage': vocab_funcs.construct_scope_note,
    'Created': vocab_funcs.construct_date_created,
    'Modified': vocab_funcs.construct_date_modified,
    'Status': vocab_funcs.construct_status,
    'Contributors': vocab_funcs.construct_contributors,
    'Resolution': vocab_funcs.construct_resolution, 
}

SCHEMA['laws'] = {
    'Term': vocab_funcs.construct_class,
    'Label': vocab_funcs.construct_label,
    'Type': vocab_funcs.construct_instance,
    'Jurisdictions': vocab_funcs.construct_jurisdiction,
    'Webpage': vocab_funcs.construct_webpage,
    'Laws': vocab_funcs.construct_law,
    'Start': vocab_funcs.construct_temporal_duration,
    'End': None,
    'Created': vocab_funcs.construct_date_created,
    'Modified': vocab_funcs.construct_date_modified,
    'Status': vocab_funcs.construct_status,
    'Contributors': vocab_funcs.construct_contributors,
    'Resolution': vocab_funcs.construct_resolution, 
}

SCHEMA['examples'] = {
    'Term': vocab_funcs.construct_example,
    'Title': vocab_funcs.construct_dct_title,
    'Description': vocab_funcs.construct_dct_description,
    'Source': None,
    'SourceFormat': None,
    'SourceType': vocab_funcs.construct_example_source,
    'Concepts': vocab_funcs.add_example_concepts,
    'Reference': None,
    'Status': vocab_funcs.construct_status,
    'Date': vocab_funcs.construct_date_created,
    'Contributor': vocab_funcs.construct_contributors,
}
