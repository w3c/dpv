#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''Data and configurations for vocabulary management'''

import csv
from rdflib import Namespace

import logging
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

# == data ==

# === serializations ===

# Serialisations are `key:value` where `key` is the file extension
# and `value` is the format passed to rdflib to serialise triples

RDF_SERIALIZATIONS = {
    'rdf': 'xml', 
    'ttl': 'turtle', 
    'n3': 'n3',
    'jsonld': 'json-ld'
    }
OWL_SERIALIZATIONS = {
    'rdf': 'xml', 
    'ttl': 'turtle', 
    'n3': 'n3',
    'jsonld': 'json-ld'
    }
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


## === term-statuses ===
VOCAB_TERM_ACCEPT = ('accepted', 'changed', 'modified', 'sunset')
VOCAB_TERM_REJECT = ('deprecated', 'removed')

## === term-ignored

IGNORED_TERMS = ('rdf:type', 'rdfs:Class', 'rdf:Property', 'skos:Concept')

# === namespaces ===
NAMESPACE_CSV = (
    'vocab_csv/Namespaces.csv',
    'vocab_csv/Namespaces_Other.csv',
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

# === Import/Export for RDF and HTML ===

# DPV Version
DPV_VERSION = "2.1-dev"
DPV_PUBLISH_DATE = "2024-10-22"
# Document status: should be one of CG-DRAFT or CG-FINAL
DOCUMENT_STATUS = "CG-DRAFT"

# Root folder to import RDF files from
IMPORT_PATH = f'../{DPV_VERSION}'
# Root folder to export HTML filese to
EXPORT_PATH = f'../{DPV_VERSION}'
# Root folder where Jinja2 templates are stored
TEMPLATE_PATH = './jinja2_resources'
# RDF to be stored in folder
EXPORT_RDF_PATH = f'../{DPV_VERSION}'

# === csv-files ===
IMPORT_CSV_PATH = './vocab_csv'
CSVFILES = {
    'dex': {
        'examples': {
            'examples': f'{IMPORT_CSV_PATH}/Example.csv',
        }
    },
    'dpv': {
        'process': {
            'classes': f'{IMPORT_CSV_PATH}/Process.csv',
            'properties': f'{IMPORT_CSV_PATH}/Process_properties.csv',
        },
        'personal_data': {
            'classes': f'{IMPORT_CSV_PATH}/PersonalData.csv',
            'properties': f'{IMPORT_CSV_PATH}/PersonalData_properties.csv',
        },
        'purposes': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Purpose.csv',
            'properties': f'{IMPORT_CSV_PATH}/Purpose_properties.csv',
        },
        'processing': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Processing.csv',
            'properties': f'{IMPORT_CSV_PATH}/Processing_properties.csv',
        },
        'TOM': {
            'taxonomy': f'{IMPORT_CSV_PATH}/TOM.csv',
            'properties': f'{IMPORT_CSV_PATH}/TOM_properties.csv',
        },
        'technical_measures': {
            'taxonomy': f'{IMPORT_CSV_PATH}/TechnicalMeasure.csv',
        },
        'organisational_measures': {
            'taxonomy': f'{IMPORT_CSV_PATH}/OrganisationalMeasure.csv',
        },
        'legal_measures': {
            'taxonomy': f'{IMPORT_CSV_PATH}/LegalMeasure.csv',
        },
        'physical_measures': {
            'taxonomy': f'{IMPORT_CSV_PATH}/PhysicalMeasure.csv',
        },
        'notice': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Notice.csv',
            'properties': f'{IMPORT_CSV_PATH}/Notice_properties.csv',
        },
        'entities': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Entities.csv',
            'properties': f'{IMPORT_CSV_PATH}/Entities_properties.csv',
        },
        'entities_authority': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Entities_Authority.csv',
            'properties': f'{IMPORT_CSV_PATH}/Entities_Authority_properties.csv',
        },
        'entities_legalrole': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Entities_LegalRole.csv',
            'properties': f'{IMPORT_CSV_PATH}/Entities_LegalRole_properties.csv',
        },
        'entities_organisation': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Entities_Organisation.csv',
        },
        'entities_datasubject': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Entities_DataSubject.csv',
            'properties': f'{IMPORT_CSV_PATH}/Entities_DataSubject_properties.csv',
        },
        'legal_basis': {
            'taxonomy': f'{IMPORT_CSV_PATH}/LegalBasis.csv',
            'properties': f'{IMPORT_CSV_PATH}/LegalBasis_properties.csv',
        },
        'legal_basis_status': {
            'taxonomy': f'{IMPORT_CSV_PATH}/LegalBasisStatus.csv',
        },
        'consent': {
            'properties': f'{IMPORT_CSV_PATH}/Consent_properties.csv',
        },
        'consent_types': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ConsentTypes.csv',
        },
        'consent_status': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ConsentStatus.csv',
        },
        'consent_controls': {
            'classes': f'{IMPORT_CSV_PATH}/ConsentControls.csv',
        },
        'contract_types': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ContractTypes.csv',
        },
        'contract_status': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ContractStatus.csv',
        },
        'contract_clause': {
            'classes': f'{IMPORT_CSV_PATH}/ContractClause.csv',
        },
        'contract_control': {
            'classes': f'{IMPORT_CSV_PATH}/ContractControl.csv',
        },
        'contract': {
            'properties': f'{IMPORT_CSV_PATH}/Contract_properties.csv',
        },
        'context': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Context.csv',
            'properties': f'{IMPORT_CSV_PATH}/Context_properties.csv',
        },
        'processing_context': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ProcessingContext.csv',
            'properties': f'{IMPORT_CSV_PATH}/ProcessingContext_properties.csv',
        },
        'processing_scale': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ProcessingScale.csv',
            'properties': f'{IMPORT_CSV_PATH}/ProcessingScale_properties.csv',
        },
        'status': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Status.csv',
            'properties': f'{IMPORT_CSV_PATH}/Status_properties.csv',
        },
        'risk': {
            'taxonomy': f'{IMPORT_CSV_PATH}/dpv-Risk.csv',
            'properties': f'{IMPORT_CSV_PATH}/dpv-Risk_properties.csv',
        },
        'jurisdiction': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Jurisdiction.csv',
            'properties': f'{IMPORT_CSV_PATH}/Jurisdiction_properties.csv',
        },
        'rights': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Rights.csv',
            'properties': f'{IMPORT_CSV_PATH}/Rights_properties.csv',
        },
        'rules': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Rules.csv',
            'properties': f'{IMPORT_CSV_PATH}/Rules_properties.csv',
        },
    },
    'pd': {
        'core': {
            'taxonomy': f'{IMPORT_CSV_PATH}/pd-core.csv',
        },
        'extended': {
            'taxonomy': f'{IMPORT_CSV_PATH}/pd-extended.csv',
        },
    },
    'tech': {
        'core': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-core.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-core-properties.csv',
        },
        'provision': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-provision.csv',
        },
        'actors': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-actors.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-actors-properties.csv',
        },
        'io': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-io.csv',
        },
        'comms': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-comms.csv',
        },
        'docs': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-docs.csv',
        },
        'status': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-status.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-status-properties.csv',
        },
        'tools': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-tools.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-tools-properties.csv',
        }, 
    },
    'ai': {
        'core': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ai-core.csv'
        },
        'techniques': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ai-techniques.csv'
        },
        'capabilities': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ai-capabilities.csv'
        },
        'risks': {
            'taxonomy-risk': f'{IMPORT_CSV_PATH}/ai-risks.csv'
        },
        'measures': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ai-measures.csv'
        },
    },
    'risk': {
        'core': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Risk.csv',
            'properties': f'{IMPORT_CSV_PATH}/Risk_properties.csv',
        },
        'risk_levels': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskLevels.csv',
        },
        'risk_matrix': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskMatrix.csv',
        },
        'risk_controls': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskControls.csv',
        },
        'risk_taxonomy': {
            'taxonomy-risk': f'{IMPORT_CSV_PATH}/RiskEvents.csv',
        },
        'incident': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Incident.csv',
        },
        'incident_status': {
            'taxonomy': f'{IMPORT_CSV_PATH}/IncidentStatus.csv',
        }
    },
    'justifications': {
        'justifications_notrequired': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Justifications_NotRequired.csv',
        },
        'justifications_nonfulfilment': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Justifications_NonFulfilment.csv',
        },
        'justifications_delay': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Justifications_Delay.csv',
        },
        'justifications_exercise': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Justifications_Exercise.csv',
        },
    },
    'loc': {
        'locations': {
            'locations': f'{IMPORT_CSV_PATH}/location.csv',
            'properties': f'{IMPORT_CSV_PATH}/location_properties.csv',
        },
        'memberships': {
            'memberships': f'{IMPORT_CSV_PATH}/location_memberships.csv',
        },
    },
    # Laws-Authorities
    'legal-at': {
        'at': {
            'laws': f'{IMPORT_CSV_PATH}/legal-at.csv',
        },
    },
    'legal-be': {
        'be': {
            'laws': f'{IMPORT_CSV_PATH}/legal-be.csv',
        },
    },
    'legal-bg': {
        'bg': {
            'laws': f'{IMPORT_CSV_PATH}/legal-bg.csv',
        },
    },
    'legal-cy': {
        'cy': {
            'laws': f'{IMPORT_CSV_PATH}/legal-cy.csv',
        },
    },
    'legal-cz': {
        'cz': {
            'laws': f'{IMPORT_CSV_PATH}/legal-cz.csv',
        },
    },
    'legal-de': {
        'de': {
            'laws': f'{IMPORT_CSV_PATH}/legal-de.csv',
        },
    },
    'legal-dk': {
        'dk': {
            'laws': f'{IMPORT_CSV_PATH}/legal-dk.csv',
        },
    },
    'legal-ee': {
        'ee': {
            'laws': f'{IMPORT_CSV_PATH}/legal-ee.csv',
        },
    },
    'legal-es': {
        'es': {
            'laws': f'{IMPORT_CSV_PATH}/legal-es.csv',
        },
    },
    'legal-eu': {
        'eu': {
            'laws': f'{IMPORT_CSV_PATH}/legal-eu.csv',
        },
    },
    'legal-fi': {
        'fi': {
            'laws': f'{IMPORT_CSV_PATH}/legal-fi.csv',
        },
    },
    'legal-fr': {
        'fr': {
            'laws': f'{IMPORT_CSV_PATH}/legal-fr.csv',
        },
    },
    'legal-gb': {
        'gb': {
            'laws': f'{IMPORT_CSV_PATH}/legal-gb.csv',
        },
    },
    'legal-gr': {
        'gr': {
            'laws': f'{IMPORT_CSV_PATH}/legal-gr.csv',
        },
    },
    'legal-hr': {
        'hr': {
            'laws': f'{IMPORT_CSV_PATH}/legal-hr.csv',
        },
    },
    'legal-hu': {
        'hu': {
            'laws': f'{IMPORT_CSV_PATH}/legal-hu.csv',
        },
    },
    'legal-ie': {
        'ie': {
            'laws': f'{IMPORT_CSV_PATH}/legal-ie.csv',
        },
    },
    'legal-in': {
        'in': {
            'laws': f'{IMPORT_CSV_PATH}/legal-in.csv',
        },
    },
    'legal-is': {
        'is': {
            'laws': f'{IMPORT_CSV_PATH}/legal-is.csv',
        },
    },
    'legal-it': {
        'it': {
            'laws': f'{IMPORT_CSV_PATH}/legal-it.csv',
        },
    },
    'legal-li': {
        'li': {
            'laws': f'{IMPORT_CSV_PATH}/legal-li.csv',
        },
    },
    'legal-lt': {
        'lt': {
            'laws': f'{IMPORT_CSV_PATH}/legal-lt.csv',
        },
    },
    'legal-lu': {
        'lu': {
            'laws': f'{IMPORT_CSV_PATH}/legal-lu.csv',
        },
    },
    'legal-lv': {
        'lv': {
            'laws': f'{IMPORT_CSV_PATH}/legal-lv.csv',
        },
    },
    'legal-mt': {
        'mt': {
            'laws': f'{IMPORT_CSV_PATH}/legal-mt.csv',
        },
    },
    'legal-nl': {
        'nl': {
            'laws': f'{IMPORT_CSV_PATH}/legal-nl.csv',
        },
    },
    'legal-no': {
        'no': {
            'laws': f'{IMPORT_CSV_PATH}/legal-no.csv',
        },
    },
    'legal-pl': {
        'pl': {
            'laws': f'{IMPORT_CSV_PATH}/legal-pl.csv',
        },
    },
    'legal-pt': {
        'pt': {
            'laws': f'{IMPORT_CSV_PATH}/legal-pt.csv',
        },
    },
    'legal-ro': {
        'ro': {
            'laws': f'{IMPORT_CSV_PATH}/legal-ro.csv',
        },
    },
    'legal-se': {
        'se': {
            'laws': f'{IMPORT_CSV_PATH}/legal-se.csv',
        },
    },
    'legal-si': {
        'si': {
            'laws': f'{IMPORT_CSV_PATH}/legal-si.csv',
        },
    },
    'legal-sk': {
        'sk': {
            'laws': f'{IMPORT_CSV_PATH}/legal-sk.csv',
        },
    },
    'legal-us': {
        'us': {
            'laws': f'{IMPORT_CSV_PATH}/legal-us.csv',
        },
    },

    # EU Regulations
    'eu-gdpr': {
        'legal_basis': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis.csv',
        },
        'legal_basis_special': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis_SpecialCategory.csv',
        },
        'legal_basis_data_transfer': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis_DataTransfer.csv',
        },
        'rights': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_LegalRights.csv',
        },
        'rights_impacts': {
            'taxonomy-risk': f'{IMPORT_CSV_PATH}/GDPR_LegalRights_Impacts.csv',
        },
        'data_transfers': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_DataTransfers.csv',
        },
        'dpia': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_DPIA.csv',
            'properties': f'{IMPORT_CSV_PATH}/GDPR_DPIA_properties.csv',
        },
        'data_breach': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_DataBreach.csv',
        },
        'compliance': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_compliance.csv',
        },
        'legal_basis_rights_mapping': {
            'legal_basis_rights_mapping': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis_Rights_Mapping.csv',
        },
        'entities': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_entities.csv',
            'properties': f'{IMPORT_CSV_PATH}/GDPR_entities_properties.csv',
        },
        'principles': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_principles.csv',
        },
    },
    'eu-dga': {
        'legal_basis': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_LegalBasis.csv',
        },
        'legal_rights': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_LegalRights.csv',
        },
        'services': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_Services.csv',
        },
        'registers': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_Registers.csv',
        },
        'toms': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_TOMs.csv',
        },
        'entities': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_entities.csv',
            'properties': f'{IMPORT_CSV_PATH}/DGA_properties.csv',
        },
        'compliance': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_compliance.csv',
        },
    },
    'eu-aiact': {
        'system': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-system.csv',
        },
        'capability': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-capability.csv',
        },
        'risk': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-risk.csv',
        },
        'data': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-data.csv',
        },
        'roles': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-roles.csv',
        },
        'docs': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-docs.csv',
        },
        'status': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-status.csv',
            'properties': f'{IMPORT_CSV_PATH}/aiact-status-properties.csv',
        },
        'misc': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-misc.csv',
        },
        'assessment': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-assessment.csv',
        },
        'compliance': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-compliance.csv',
        },
        'sector': {
            'taxonomy': f'{IMPORT_CSV_PATH}/aiact-sector.csv',
        },
    },
    'eu-nis2': {
        'notice': {
            'taxonomy': f'{IMPORT_CSV_PATH}/NIS2_Notice.csv',
        },
        'compliance': {
            'taxonomy': f'{IMPORT_CSV_PATH}/NIS2_compliance.csv',
        },
    },
    'eu-rights': {
        'fundamental': {
            'taxonomy': f'{IMPORT_CSV_PATH}/EUFundamentalRights.csv',
        },
        'impacts': {
            'taxonomy-risk': f'{IMPORT_CSV_PATH}/EUFundamentalRights_Impacts.csv',
        },
    },
}


# === translations ===
IMPORT_TRANSLATIONS = {
    # 'de': {
    #     'lang': 'German',
    #     'prod': f'{IMPORT_CSV_PATH}/DE_prod.csv',
    #     'verify': f'{IMPORT_CSV_PATH}/DE_verify.csv',
    # },
    # 'fr': {
    #     'lang': 'French',
    #     'prod': f'{IMPORT_CSV_PATH}/FR_prod.csv',
    #     'verify': f'{IMPORT_CSV_PATH}/FR_verify.csv',
    # },
    # 'it': {
    #     'lang': 'Italian',
    #     'prod': f'{IMPORT_CSV_PATH}/IT_prod.csv',
    #     'verify': f'{IMPORT_CSV_PATH}/IT_verify.csv',
    # },
    # 'es': {
    #     'lang': 'Spanish',
    #     'prod': f'{IMPORT_CSV_PATH}/ES_prod.csv',
    #     'verify': f'{IMPORT_CSV_PATH}/ES_verify.csv',
    # },
}
# This file will save the missing translations.
# The initial list is populated in [[200.py]] and then the data is 
# collected and overwritten in [[300.py]]
TRANSLATIONS_MISSING_FILE = f"{IMPORT_CSV_PATH}/translations_missing.json"

# === rdf-vocabs ===
# How to do this?
# load all vocabulary files - create a global dict
RDF_VOCABS = {
    'dex': {
        'vocab': f'{IMPORT_PATH}/examples/dex.ttl',
        'template': 'template_examples.jinja2',
        'export': f'{EXPORT_PATH}/examples',
        'modules': {},
        'module-template': {},
        # Metadata for RDF Vocabs.
        'metadata': {
        # Manually declared:
            "dct:title": "Examples for Data Privacy Vocabulary",
            "dct:description": "Examples for/using DPVCG vocabularies",
            "dct:created": "2022-08-18",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "",
            "bibo:status": "published",
        # Automatically added when serialising:
            # dct:identifier - the IRI
            # dct:conformsTo - for default serialisation: RDFS, SKOS; for OWL: OWL2
            # dct:language - EN and all languages defined
            # dct:contributor - collated from contributors defined in concepts
            # dct:hasFormat/dct:isFormatOf - defined for each serialisation
            # dct:hasVersion/dct:isVersionOf - between RDFS/SKOS and OWL variants
            # dct:license - https://www.w3.org/copyright/document-license-2023/
            # vann:preferredNamespacePrefix - dict key / vocab name
            # vann:preferredNamespaceUri - declared namespace for vocab
        },
    },
    'dpv': {
        'vocab': f'{IMPORT_PATH}/dpv/dpv.ttl',
        'template': 'template_dpv.jinja2',
        'export': f'{EXPORT_PATH}/dpv',
        'modules': {
            # 'core': f'{IMPORT_PATH}/dpv/modules/core.ttl',
            'process': f'{IMPORT_PATH}/dpv/modules/process.ttl',
            'personal_data': f'{IMPORT_PATH}/dpv/modules/personal_data.ttl',
            'purposes': f'{IMPORT_PATH}/dpv/modules/purposes.ttl',
            'processing': f'{IMPORT_PATH}/dpv/modules/processing.ttl',
            'TOM': f'{IMPORT_PATH}/dpv/modules/TOM.ttl',
            'TOM-technical': f'{IMPORT_PATH}/dpv/modules/technical_measures.ttl',
            'TOM-organisational': f'{IMPORT_PATH}/dpv/modules/organisational_measures.ttl',
            'TOM-legal': f'{IMPORT_PATH}/dpv/modules/legal_measures.ttl',
            'TOM-physical': f'{IMPORT_PATH}/dpv/modules/physical_measures.ttl',
            'TOM-notice': f'{IMPORT_PATH}/dpv/modules/notice.ttl',
            'entities': f'{IMPORT_PATH}/dpv/modules/entities.ttl',
            'entities-authority': f'{IMPORT_PATH}/dpv/modules/entities_authority.ttl',
            'entities-legalrole': f'{IMPORT_PATH}/dpv/modules/entities_legalrole.ttl',
            'entities-organisation': f'{IMPORT_PATH}/dpv/modules/entities_organisation.ttl',
            'entities-datasubject': f'{IMPORT_PATH}/dpv/modules/entities_datasubject.ttl',
            'legal_basis': f'{IMPORT_PATH}/dpv/modules/legal_basis.ttl',
            'legal_basis-consent': f'{IMPORT_PATH}/dpv/modules/consent.ttl',
            'legal_basis-consent-types': f'{IMPORT_PATH}/dpv/modules/consent_types.ttl',
            'legal_basis-consent-status': f'{IMPORT_PATH}/dpv/modules/consent_status.ttl',
            'legal_basis-consent-controls': f'{IMPORT_PATH}/dpv/modules/consent_controls.ttl',
            'legal_basis-contract': f'{IMPORT_PATH}/dpv/modules/contract.ttl',
            'legal_basis-contract-types': f'{IMPORT_PATH}/dpv/modules/contract_types.ttl',
            'legal_basis-contract-status': f'{IMPORT_PATH}/dpv/modules/contract_status.ttl',
            'legal_basis-contract-clause': f'{IMPORT_PATH}/dpv/modules/contract_clause.ttl',
            'legal_basis-contract-control': f'{IMPORT_PATH}/dpv/modules/contract_control.ttl',
            'legal_basis-status': f'{IMPORT_PATH}/dpv/modules/legal_basis_status.ttl',
            'processing-context': f'{IMPORT_PATH}/dpv/modules/processing_context.ttl',
            'processing-scale': f'{IMPORT_PATH}/dpv/modules/processing_scale.ttl',
            'context': f'{IMPORT_PATH}/dpv/modules/context.ttl',
            'context-status': f'{IMPORT_PATH}/dpv/modules/status.ttl',
            'context-jurisdiction': f'{IMPORT_PATH}/dpv/modules/jurisdiction.ttl',
            'risk': f'{IMPORT_PATH}/dpv/modules/risk.ttl',
            'rights': f'{IMPORT_PATH}/dpv/modules/rights.ttl',
            'rules': f'{IMPORT_PATH}/dpv/modules/rules.ttl',
        },
        'module-template': {
            'entities': 'template_dpv_entities.jinja2',
            'personal_data': 'template_dpv_personal_data.jinja2',
            'purposes': 'template_dpv_purposes.jinja2',
            'processing': 'template_dpv_processing.jinja2',
            'TOM': 'template_dpv_TOM.jinja2',
            'legal_basis': 'template_dpv_legal_basis.jinja2',
            'context': 'template_dpv_context.jinja2',
            'risk': 'template_dpv_risk.jinja2',
            'rights': 'template_dpv_rights.jinja2',
            'rules': 'template_dpv_rules.jinja2',
        },
        'metadata': {
            "dct:title": "Data Privacy Vocabulary (DPV)",
            "dct:description": "The Data Privacy Vocabulary (DPV) provides terms (classes and properties) to represent information about processing of personal data, for example - purposes, processing operations, personal data, technical and organisational measures.",
            "dct:created": "2022-08-18",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit, Beatriz Esteves, Georg P. Krog, Paul Ryan, Delaram Golpayegani, Julian Flake",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "",
            "bibo:status": "published",
        },
    },
    # EXTENSIONS
    'pd': {
        'vocab': f'{IMPORT_PATH}/pd/pd.ttl',
        'template': 'template_pd.jinja2',
        'export': f'{EXPORT_PATH}/pd',
        'modules': {
            'core': f'{IMPORT_PATH}/pd/modules/core.ttl',
            'extended': f'{IMPORT_PATH}/pd/modules/extended.ttl',
        },
        'metadata': {
            "dct:title": "Personal Data Categories",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing additional categories of personal data",
            "dct:created": "2022-04-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit, Axel Polleres, Beatriz Esteves, Georg P. Krog",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            "bibo:status": "published",
        },
    },
    'tech': {
        'vocab': f'{IMPORT_PATH}/tech/tech.ttl',
        'template': 'template_tech.jinja2',
        'export': f'{EXPORT_PATH}/tech',
        'modules': {
            'core': f'{IMPORT_PATH}/tech/modules/core.ttl',
            'provision': f'{IMPORT_PATH}/tech/modules/provision.ttl',
            'actors': f'{IMPORT_PATH}/tech/modules/actors.ttl',
            'comms': f'{IMPORT_PATH}/tech/modules/comms.ttl',
            'docs': f'{IMPORT_PATH}/tech/modules/docs.ttl',
            'status': f'{IMPORT_PATH}/tech/modules/status.ttl',
            'tools': f'{IMPORT_PATH}/tech/modules/tools.ttl',
        },
        'metadata': {
            "dct:title": "Technology Concepts",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing information about technologies and its provision",
            "dct:created": "2024-05-31",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit, Georg P Krog, Paul Ryan, Julian Flake, Delaram Golpayegani",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            "bibo:status": "published",
        },
    },
    'ai': {
        'vocab': f'{IMPORT_PATH}/ai/ai.ttl',
        'template': 'template_ai.jinja2',
        'export': f'{EXPORT_PATH}/ai',
        'modules': {
            'core': f'{IMPORT_PATH}/ai/modules/core.ttl',
            'techniques': f'{IMPORT_PATH}/ai/modules/techniques.ttl',
            'capabilities': f'{IMPORT_PATH}/ai/modules/capabilities.ttl',
            'risks': f'{IMPORT_PATH}/ai/modules/risks.ttl',
            'measures': f'{IMPORT_PATH}/ai/modules/measures.ttl',
            'bias': f'{IMPORT_PATH}/ai/modules/bias.ttl',
        },
        'metadata': {
            "dct:title": "AI Technology Concepts",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing information about AI technologies",
            "dct:created": "2024-05-31",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Delaram Golpayegani, Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "tech",
            "bibo:status": "draft",
        },
    },
    'risk': {
        'vocab': f'{IMPORT_PATH}/risk/risk.ttl',
        'template': 'template_risk.jinja2',
        'export': f'{EXPORT_PATH}/risk',
        'modules': {
            'core': f'{IMPORT_PATH}/risk/modules/core.ttl',
            'risk_taxonomy': f'{IMPORT_PATH}/risk/modules/risk_taxonomy.ttl',
            'risk_levels': f'{IMPORT_PATH}/risk/modules/risk_levels.ttl',
            'risk_matrix': f'{IMPORT_PATH}/risk/modules/risk_matrix.ttl',
            'risk_controls': f'{IMPORT_PATH}/risk/modules/risk_controls.ttl',
            'incident': f'{IMPORT_PATH}/risk/modules/incident.ttl',
            'incident_status': f'{IMPORT_PATH}/risk/modules/incident_status.ttl',
        },
        'metadata': {
            "dct:title": "Risk Concepts",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing information about risk assessment and risk management",
            "dct:created": "2022-08-14",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit, Georg P. Krog, Paul Ryan, Rob Brennan, Delaram Golpayegani, Beatriz Esteves, Julian Flake",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            "bibo:status": "published",
        },
    },
    'justifications': {
        'vocab': f'{IMPORT_PATH}/justifications/justifications.ttl',
        'template': 'template_justifications.jinja2',
        'export': f'{EXPORT_PATH}/justifications',
        'modules': {
            'justifications_notrequired': f'{IMPORT_PATH}/justifications/modules/justifications_notrequired.ttl',
            'justifications_nonfulfilment': f'{IMPORT_PATH}/justifications/modules/justifications_nonfulfilment.ttl',
            'justifications_delay': f'{IMPORT_PATH}/justifications/modules/justifications_delay.ttl',
            'justifications_exercise': f'{IMPORT_PATH}/justifications/modules/justifications_exercise.ttl',
        },
        'metadata': {
            "dct:title": "Justification Concepts",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing information about justifications",
            "dct:created": "2024-04-21",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Beatriz Esteves, Harshvardhan J. Pandit, Georg P. Krog, Paul Ryan",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            "bibo:status": "published",
        },
    },
    'loc': {
        'vocab': f'{IMPORT_PATH}/loc/loc.ttl',
        'template': 'template_locations.jinja2',
        'export': f'{EXPORT_PATH}/loc',
        'modules': {
            'locations': f'{IMPORT_PATH}/loc/modules/locations.ttl',
            'memberships': f'{IMPORT_PATH}/loc/modules/memberships.ttl',
        },
        'metadata': {
            "dct:title": "Location Concepts",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing (geo-political) locations and memberships",
            "dct:created": "2022-04-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            "bibo:status": "published",
        },
    },
    # LEGAL VOCABS
    'legal-eu': { # EU vocab needs to be loaded first as other vocabs contain references to it
        'vocab': f'{IMPORT_PATH}/legal/eu/legal-eu.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/eu/legal-eu.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for European Union (EU)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for European Union as jurisdiction",
            "dct:created": "2024-01-01",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/eu',
            "bibo:status": "published",
        },
    },
    'legal-at': {
        'vocab': f'{IMPORT_PATH}/legal/at/legal-at.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/at',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/at/legal-at.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Austria (AT)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Austria as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/at',
            "bibo:status": "published",
        },
    },
    'legal-be': {
        'vocab': f'{IMPORT_PATH}/legal/be/legal-be.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/be',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/be/legal-be.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Belgium (BE)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Belgium as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/be',
            "bibo:status": "published",
        },
    },
    'legal-bg': {
        'vocab': f'{IMPORT_PATH}/legal/bg/legal-bg.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/bg',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/bg/legal-bg.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Bulgaria (BG)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Bulgaria as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/bg',
            "bibo:status": "published",
        },
    },
    'legal-cy': {
        'vocab': f'{IMPORT_PATH}/legal/cy/legal-cy.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/cy',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/cy/legal-cy.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Cyprus (CY)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Cyprus as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/cy',
            "bibo:status": "published",
        },
    },
    'legal-cz': {
        'vocab': f'{IMPORT_PATH}/legal/cz/legal-cz.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/cz',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/cz/legal-cz.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Czech Republic (CZ)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Czech Republic as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/cz',
            "bibo:status": "published",
        },
    },
    'legal-de': {
        'vocab': f'{IMPORT_PATH}/legal/de/legal-de.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/de',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/de/legal-de.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Germany (DE)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Germany as jurisdiction",
            "dct:created": "2024-01-01",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/de',
            "bibo:status": "published",
        },
    },
    'legal-dk': {
        'vocab': f'{IMPORT_PATH}/legal/dk/legal-dk.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/dk',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/dk/legal-dk.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Denmark (DK)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Denmark as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/dk',
            "bibo:status": "published",
        },
    },
    'legal-ee': {
        'vocab': f'{IMPORT_PATH}/legal/ee/legal-ee.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/ee',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/ee/legal-ee.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Estonia (EE)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Estonia as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/ee',
            "bibo:status": "published",
        },
    },
    'legal-es': {
        'vocab': f'{IMPORT_PATH}/legal/es/legal-es.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/es',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/es/legal-es.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Spain (ES)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Spain as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/es',
            "bibo:status": "published",
        },
    },
    'legal-fi': {
        'vocab': f'{IMPORT_PATH}/legal/fi/legal-fi.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/fi',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/fi/legal-fi.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Finland (FI)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Finland as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/fi',
            "bibo:status": "published",
        },
    },
    'legal-fr': {
        'vocab': f'{IMPORT_PATH}/legal/fr/legal-fr.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/fr',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/fr/legal-fr.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for France (FR)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for France as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/fr',
            "bibo:status": "published",
        },
    },
    'legal-gb': {
        'vocab': f'{IMPORT_PATH}/legal/gb/legal-gb.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/gb',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/gb/legal-gb.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for United Kingdom of Great Britain and Northern Ireland (GB)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for United Kingdom of Great Britain and Northern Ireland  as jurisdiction",
            "dct:created": "2024-01-01",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/gb',
            "bibo:status": "published",
        },
    },
    'legal-gr': {
        'vocab': f'{IMPORT_PATH}/legal/gr/legal-gr.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/gr',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/gr/legal-gr.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Greece (GR)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Greece as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/gr',
            "bibo:status": "published",
        },
    },
    'legal-hr': {
        'vocab': f'{IMPORT_PATH}/legal/hr/legal-hr.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/hr',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/hr/legal-hr.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Crotia (HR)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Croatia as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/hr',
            "bibo:status": "published",
        },
    },
    'legal-hu': {
        'vocab': f'{IMPORT_PATH}/legal/hu/legal-hu.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/hu',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/hu/legal-hu.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Hungary (HU)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Hungary as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/hu',
            "bibo:status": "published",
        },
    },
    'legal-ie': {
        'vocab': f'{IMPORT_PATH}/legal/ie/legal-ie.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/ie',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/ie/legal-ie.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Ireland (IE)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Ireland as jurisdiction",
            "dct:created": "2024-01-01",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/ie',
            "bibo:status": "published",
        },
    },
    'legal-in': {
        'vocab': f'{IMPORT_PATH}/legal/in/legal-in.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/in',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/in/legal-in.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for India (IN)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for India as jurisdiction",
            "dct:created": "2024-01-01",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/in',
            "bibo:status": "published",
        },
    },
    'legal-is': {
        'vocab': f'{IMPORT_PATH}/legal/is/legal-is.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/is',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/is/legal-is.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Iceland (IS)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Iceland as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/is',
            "bibo:status": "published",
        },
    },
    'legal-it': {
        'vocab': f'{IMPORT_PATH}/legal/it/legal-it.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/it',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/it/legal-it.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Italy (IT)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Italy as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/it',
            "bibo:status": "published",
        },
    },
    'legal-li': {
        'vocab': f'{IMPORT_PATH}/legal/li/legal-li.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/li',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/li/legal-li.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Liechtenstein (LI)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Liechtenstein as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/li',
            "bibo:status": "published",
        },
    },
    'legal-lt': {
        'vocab': f'{IMPORT_PATH}/legal/lt/legal-lt.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/lt',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/lt/legal-lt.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Lithuania (LT)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Lithuania as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/lt',
            "bibo:status": "published",
        },
    },
    'legal-lu': {
        'vocab': f'{IMPORT_PATH}/legal/lu/legal-lu.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/lu',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/lu/legal-lu.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Luxembourg (LU)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Luxembourg as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/lu',
            "bibo:status": "published",
        },
    },
    'legal-lv': {
        'vocab': f'{IMPORT_PATH}/legal/lv/legal-lv.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/lv',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/lv/legal-lv.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Latvia(LV)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Latvia as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/lv',
            "bibo:status": "published",
        },
    },
    'legal-mt': {
        'vocab': f'{IMPORT_PATH}/legal/mt/legal-mt.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/mt',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/mt/legal-mt.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Malta (MT)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Malta as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/mt',
            "bibo:status": "published",
        },
    },
    'legal-nl': {
        'vocab': f'{IMPORT_PATH}/legal/nl/legal-nl.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/nl',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/nl/legal-nl.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Netherlands (NL)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Netherlands as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/nl',
            "bibo:status": "published",
        },
    },
    'legal-no': {
        'vocab': f'{IMPORT_PATH}/legal/no/legal-no.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/no',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/no/legal-no.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Norway (NO)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Norway as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/no',
            "bibo:status": "published",
        },
    },
    'legal-pl': {
        'vocab': f'{IMPORT_PATH}/legal/pl/legal-pl.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/pl',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/pl/legal-pl.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Poland (PL)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Poland as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/pl',
            "bibo:status": "published",
        },
    },
    'legal-pt': {
        'vocab': f'{IMPORT_PATH}/legal/pt/legal-pt.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/pt',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/pt/legal-pt.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Portugal (PT)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Portugal as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/pt',
            "bibo:status": "published",
        },
    },
    'legal-ro': {
        'vocab': f'{IMPORT_PATH}/legal/ro/legal-ro.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/ro',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/ro/legal-ro.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Romania (RO)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Romania as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/ro',
            "bibo:status": "published",
        },
    },
    'legal-se': {
        'vocab': f'{IMPORT_PATH}/legal/se/legal-se.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/se',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/se/legal-se.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Sweden (SE)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Sweden as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/se',
            "bibo:status": "published",
        },
    },
    'legal-si': {
        'vocab': f'{IMPORT_PATH}/legal/si/legal-si.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/si',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/si/legal-si.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Slovenia (SI)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Slovenia as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/si',
            "bibo:status": "published",
        },
    },
    'legal-sk': {
        'vocab': f'{IMPORT_PATH}/legal/sk/legal-sk.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/sk',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/sk/legal-sk.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for Slovakia (SK)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Slovakia as jurisdiction",
            "dct:created": "2024-08-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/sk',
            "bibo:status": "published",
        },
    },
    'legal-us': {
        'vocab': f'{IMPORT_PATH}/legal/us/legal-us.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/us',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/us/legal-us.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for United States of America (US)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for United States of America as jurisdiction",
            "dct:created": "2024-01-01",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal/us',
            "bibo:status": "published",
        },
    },
    'legal': {
        'vocab': f'{IMPORT_PATH}/legal/legal.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/legal.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information associated with specific jurisdictions",
            "dct:created": "2022-04-02",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            'iri': 'https://w3id.org/dpv/legal',
            "bibo:status": "published",
        },
    },
    # EU Laws
    'eu-gdpr': {
        'vocab': f'{IMPORT_PATH}/legal/eu/gdpr/eu-gdpr.ttl',
        'template': 'template_legal_eu_gdpr.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu/gdpr',
        'modules': {
            'legal_basis': f'{IMPORT_PATH}/legal/eu/gdpr/modules/legal_basis.ttl',
            'legal_basis-special': f'{IMPORT_PATH}/legal/eu/gdpr/modules/legal_basis_special.ttl',
            'legal_basis-data_transfer': f'{IMPORT_PATH}/legal/eu/gdpr/modules/legal_basis_data_transfer.ttl',
            'rights': f'{IMPORT_PATH}/legal/eu/gdpr/modules/rights.ttl',
            'rights-impacts': f'{IMPORT_PATH}/legal/eu/gdpr/modules/rights_impacts.ttl',
            'data_transfers': f'{IMPORT_PATH}/legal/eu/gdpr/modules/data_transfers.ttl',
            'dpia': f'{IMPORT_PATH}/legal/eu/gdpr/modules/dpia.ttl',
            'data_breach': f'{IMPORT_PATH}/legal/eu/gdpr/modules/data_breach.ttl',
            'compliance': f'{IMPORT_PATH}/legal/eu/gdpr/modules/compliance.ttl',
            'legal_basis-rights_mapping': f'{IMPORT_PATH}/legal/eu/gdpr/modules/legal_basis_rights_mapping.ttl',
            'entities': f'{IMPORT_PATH}/legal/eu/gdpr/modules/entities.ttl',
            'principles': f'{IMPORT_PATH}/legal/eu/gdpr/modules/principles.ttl',
        },
        'metadata': {
            "dct:title": "EU General Data Protection Regulation (GDPR)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing information associated with EU GDPR",
            "dct:created": "2019-06-18",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit, Georg P. Krog, Paul Ryan, Beatriz Esteves",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            "bibo:status": "published",
        },
    },
    'eu-dga': {
        'vocab': f'{IMPORT_PATH}/legal/eu/dga/eu-dga.ttl',
        'template': 'template_legal_eu_dga.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu/dga',
        'modules': {
            'entities': f'{IMPORT_PATH}/legal/eu/dga/modules/entities.ttl',
            'legal_basis': f'{IMPORT_PATH}/legal/eu/dga/modules/legal_basis.ttl',
            'legal_rights': f'{IMPORT_PATH}/legal/eu/dga/modules/legal_rights.ttl',
            'registers': f'{IMPORT_PATH}/legal/eu/dga/modules/registers.ttl',
            'services': f'{IMPORT_PATH}/legal/eu/dga/modules/services.ttl',
            'toms': f'{IMPORT_PATH}/legal/eu/dga/modules/toms.ttl',
            'compliance': f'{IMPORT_PATH}/legal/eu/dga/modules/compliance.ttl',
        },
        'metadata': {
            "dct:title": "EU Data Governance Act (DGA)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing  information associated with EU DGA",
            "dct:created": "2023-09-20",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Beatriz Esteves, Harshvardhan J. Pandit, Georg P. Krog",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            "bibo:status": "published",
        },
    },
    'eu-aiact': {
        'vocab': f'{IMPORT_PATH}/legal/eu/aiact/eu-aiact.ttl',
        'template': 'template_legal_eu_aiact.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu/aiact',
        'modules': {
            'system': f'{IMPORT_PATH}/legal/eu/aiact/modules/system.ttl',
            'capability': f'{IMPORT_PATH}/legal/eu/aiact/modules/capability.ttl',
            'risk': f'{IMPORT_PATH}/legal/eu/aiact/modules/risk.ttl',
            'data': f'{IMPORT_PATH}/legal/eu/aiact/modules/data.ttl',
            'roles': f'{IMPORT_PATH}/legal/eu/aiact/modules/roles.ttl',
            'docs': f'{IMPORT_PATH}/legal/eu/aiact/modules/docs.ttl',
            'status': f'{IMPORT_PATH}/legal/eu/aiact/modules/status.ttl',
            'misc': f'{IMPORT_PATH}/legal/eu/aiact/modules/misc.ttl',
            'assessment': f'{IMPORT_PATH}/legal/eu/aiact/modules/assessment.ttl',
            'compliance': f'{IMPORT_PATH}/legal/eu/aiact/modules/compliance.ttl',
        },
        'metadata': {
            "dct:title": "EU AI Act",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing  information associated with EU AI Act",
            "dct:created": "2024-04-10",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Delaram Golpayegani",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            "bibo:status": "draft",
        },
    },
    'eu-nis2': {
        'vocab': f'{IMPORT_PATH}/legal/eu/nis2/eu-nis2.ttl',
        'template': 'template_legal_eu_nis2.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu/nis2',
        'modules': {
            'notice': f'{IMPORT_PATH}/legal/eu/nis2/modules/notice.ttl',
            'compliance': f'{IMPORT_PATH}/legal/eu/nis2/modules/compliance.ttl',
        },
        'metadata': {
            "dct:title": "EU NIS2",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing  information associated with EU NIS2",
            "dct:created": "2024-05-19",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit, Georg P. Krog",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            "bibo:status": "published",
        },
    },
    'eu-rights': {
        'vocab': f'{IMPORT_PATH}/legal/eu/rights/eu-rights.ttl',
        'template': 'template_legal_eu_rights.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu/rights',
        'modules': {
            'fundamental': f'{IMPORT_PATH}/legal/eu/rights/modules/fundamental.ttl',
            'impacts': f'{IMPORT_PATH}/legal/eu/rights/modules/impacts.ttl',
        },
        'metadata': {
            "dct:title": "EU Fundamental Rights and Freedoms",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing information associated with EU's Fundamental Rights and Freedoms",
            "dct:created": "2022-08-15",
            "dct:modified": DPV_PUBLISH_DATE,
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": DPV_VERSION,
            "profile:isProfileOf": "dpv",
            "bibo:status": "draft",
        },
    },
}

# === exports ===
RDF_STRUCTURE = {
    'dpv': {
        'main': f'{EXPORT_RDF_PATH}/dpv',
        'modules': f'{EXPORT_RDF_PATH}/dpv/modules',
    },
    'pd': {
        'main': f'{EXPORT_RDF_PATH}/pd',
        'modules': f'{EXPORT_RDF_PATH}/pd/modules',
    },
    'tech': {
        'main': f'{EXPORT_RDF_PATH}/tech',
        'modules': f'{EXPORT_RDF_PATH}/tech/modules',
    },
    'ai': {
        'main': f'{EXPORT_RDF_PATH}/ai',
        'modules': f'{EXPORT_RDF_PATH}/ai/modules',
    },
    'risk': {
        'main': f'{EXPORT_RDF_PATH}/risk',
        'modules': f'{EXPORT_RDF_PATH}/risk/modules',
    },
    'justifications': {
        'main': f'{EXPORT_RDF_PATH}/justifications',
        'modules': f'{EXPORT_RDF_PATH}/justifications/modules',
    },
    'loc': {
        'main': f'{EXPORT_RDF_PATH}/loc',
        'modules': f'{EXPORT_RDF_PATH}/loc/modules',
    },
    'legal': {  # Consolidated graph of all legal data
        'main': f'{EXPORT_RDF_PATH}/legal',
    },
    'legal-at': {
        'main': f'{EXPORT_RDF_PATH}/legal/at', 
        'modules': f'{EXPORT_RDF_PATH}/legal/at/modules', 
    },
    'legal-be': {
        'main': f'{EXPORT_RDF_PATH}/legal/be', 
        'modules': f'{EXPORT_RDF_PATH}/legal/be/modules', 
    },
    'legal-bg': {
        'main': f'{EXPORT_RDF_PATH}/legal/bg', 
        'modules': f'{EXPORT_RDF_PATH}/legal/bg/modules', 
    },
    'legal-cy': {
        'main': f'{EXPORT_RDF_PATH}/legal/cy', 
        'modules': f'{EXPORT_RDF_PATH}/legal/cy/modules', 
    },
    'legal-cz': {
        'main': f'{EXPORT_RDF_PATH}/legal/cz', 
        'modules': f'{EXPORT_RDF_PATH}/legal/cz/modules', 
    },
    'legal-de': {
        'main': f'{EXPORT_RDF_PATH}/legal/de', 
        'modules': f'{EXPORT_RDF_PATH}/legal/de/modules', 
    },
    'legal-dk': {
        'main': f'{EXPORT_RDF_PATH}/legal/dk', 
        'modules': f'{EXPORT_RDF_PATH}/legal/dk/modules', 
    },
    'legal-ee': {
        'main': f'{EXPORT_RDF_PATH}/legal/ee', 
        'modules': f'{EXPORT_RDF_PATH}/legal/ee/modules', 
    },
    'legal-es': {
        'main': f'{EXPORT_RDF_PATH}/legal/es', 
        'modules': f'{EXPORT_RDF_PATH}/legal/es/modules', 
    },
    'legal-eu': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu', 
        'modules': f'{EXPORT_RDF_PATH}/legal/eu/modules', 
    },
    'legal-fi': {
        'main': f'{EXPORT_RDF_PATH}/legal/fi', 
        'modules': f'{EXPORT_RDF_PATH}/legal/fi/modules', 
    },
    'legal-fr': {
        'main': f'{EXPORT_RDF_PATH}/legal/fr', 
        'modules': f'{EXPORT_RDF_PATH}/legal/fr/modules', 
    },
    'legal-gb': {
        'main': f'{EXPORT_RDF_PATH}/legal/gb', 
        'modules': f'{EXPORT_RDF_PATH}/legal/gb/modules', 
    },
    'legal-gr': {
        'main': f'{EXPORT_RDF_PATH}/legal/gr', 
        'modules': f'{EXPORT_RDF_PATH}/legal/gr/modules', 
    },
    'legal-hr': {
        'main': f'{EXPORT_RDF_PATH}/legal/hr', 
        'modules': f'{EXPORT_RDF_PATH}/legal/hr/modules', 
    },
    'legal-hu': {
        'main': f'{EXPORT_RDF_PATH}/legal/hu', 
        'modules': f'{EXPORT_RDF_PATH}/legal/hu/modules', 
    },
    'legal-ie': {
        'main': f'{EXPORT_RDF_PATH}/legal/ie', 
        'modules': f'{EXPORT_RDF_PATH}/legal/ie/modules', 
    },
    'legal-in': {
        'main': f'{EXPORT_RDF_PATH}/legal/in', 
        'modules': f'{EXPORT_RDF_PATH}/legal/in/modules', 
    },
    'legal-is': {
        'main': f'{EXPORT_RDF_PATH}/legal/is', 
        'modules': f'{EXPORT_RDF_PATH}/legal/is/modules', 
    },
    'legal-it': {
        'main': f'{EXPORT_RDF_PATH}/legal/it', 
        'modules': f'{EXPORT_RDF_PATH}/legal/it/modules', 
    },
    'legal-li': {
        'main': f'{EXPORT_RDF_PATH}/legal/li', 
        'modules': f'{EXPORT_RDF_PATH}/legal/li/modules', 
    },
    'legal-lt': {
        'main': f'{EXPORT_RDF_PATH}/legal/lt', 
        'modules': f'{EXPORT_RDF_PATH}/legal/lt/modules', 
    },
    'legal-lu': {
        'main': f'{EXPORT_RDF_PATH}/legal/lu', 
        'modules': f'{EXPORT_RDF_PATH}/legal/lu/modules', 
    },
    'legal-lv': {
        'main': f'{EXPORT_RDF_PATH}/legal/lv', 
        'modules': f'{EXPORT_RDF_PATH}/legal/lv/modules', 
    },
    'legal-mt': {
        'main': f'{EXPORT_RDF_PATH}/legal/mt', 
        'modules': f'{EXPORT_RDF_PATH}/legal/mt/modules', 
    },
    'legal-nl': {
        'main': f'{EXPORT_RDF_PATH}/legal/nl', 
        'modules': f'{EXPORT_RDF_PATH}/legal/nl/modules', 
    },
    'legal-no': {
        'main': f'{EXPORT_RDF_PATH}/legal/no', 
        'modules': f'{EXPORT_RDF_PATH}/legal/no/modules', 
    },
    'legal-pl': {
        'main': f'{EXPORT_RDF_PATH}/legal/pl', 
        'modules': f'{EXPORT_RDF_PATH}/legal/pl/modules', 
    },
    'legal-pt': {
        'main': f'{EXPORT_RDF_PATH}/legal/pt', 
        'modules': f'{EXPORT_RDF_PATH}/legal/pt/modules', 
    },
    'legal-ro': {
        'main': f'{EXPORT_RDF_PATH}/legal/ro', 
        'modules': f'{EXPORT_RDF_PATH}/legal/ro/modules', 
    },
    'legal-se': {
        'main': f'{EXPORT_RDF_PATH}/legal/se', 
        'modules': f'{EXPORT_RDF_PATH}/legal/se/modules', 
    },
    'legal-si': {
        'main': f'{EXPORT_RDF_PATH}/legal/si', 
        'modules': f'{EXPORT_RDF_PATH}/legal/si/modules', 
    },
    'legal-sk': {
        'main': f'{EXPORT_RDF_PATH}/legal/sk', 
        'modules': f'{EXPORT_RDF_PATH}/legal/sk/modules', 
    },
    'legal-us': {
        'main': f'{EXPORT_RDF_PATH}/legal/us', 
        'modules': f'{EXPORT_RDF_PATH}/legal/us/modules', 
    },
    'eu-gdpr': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu/gdpr',
        'modules': f'{EXPORT_RDF_PATH}/legal/eu/gdpr/modules',
    },
    'eu-dga': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu/dga',
        'modules': f'{EXPORT_RDF_PATH}/legal/eu/dga/modules',
    },
    'eu-aiact': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu/aiact',
        'modules': f'{EXPORT_RDF_PATH}/legal/eu/aiact/modules',
    },
    'eu-nis2': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu/nis2',
        'modules': f'{EXPORT_RDF_PATH}/legal/eu/nis2/modules',
    },
    'eu-rights': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu/rights',
        'modules': f'{EXPORT_RDF_PATH}/legal/eu/rights/modules',
    },
    'dex': {
        'main': f'{EXPORT_RDF_PATH}/examples',
        'modules': f'{EXPORT_RDF_PATH}/examples/modules',
    }
}

# Collated concepts
RDF_COLLATIONS = ({
    'name': 'legal',
    'input': (
        f'{EXPORT_RDF_PATH}/legal/at/legal-at.ttl',
        f'{EXPORT_RDF_PATH}/legal/be/legal-be.ttl',
        f'{EXPORT_RDF_PATH}/legal/bg/legal-bg.ttl',
        f'{EXPORT_RDF_PATH}/legal/cy/legal-cy.ttl',
        f'{EXPORT_RDF_PATH}/legal/cz/legal-cz.ttl',
        f'{EXPORT_RDF_PATH}/legal/de/legal-de.ttl',
        f'{EXPORT_RDF_PATH}/legal/dk/legal-dk.ttl',
        f'{EXPORT_RDF_PATH}/legal/ee/legal-ee.ttl',
        f'{EXPORT_RDF_PATH}/legal/es/legal-es.ttl',
        f'{EXPORT_RDF_PATH}/legal/eu/legal-eu.ttl',
        f'{EXPORT_RDF_PATH}/legal/fi/legal-fi.ttl',
        f'{EXPORT_RDF_PATH}/legal/fr/legal-fr.ttl',
        f'{EXPORT_RDF_PATH}/legal/gb/legal-gb.ttl',
        f'{EXPORT_RDF_PATH}/legal/gr/legal-gr.ttl',
        f'{EXPORT_RDF_PATH}/legal/hr/legal-hr.ttl',
        f'{EXPORT_RDF_PATH}/legal/hu/legal-hu.ttl',
        f'{EXPORT_RDF_PATH}/legal/ie/legal-ie.ttl',
        f'{EXPORT_RDF_PATH}/legal/in/legal-in.ttl',
        f'{EXPORT_RDF_PATH}/legal/is/legal-is.ttl',
        f'{EXPORT_RDF_PATH}/legal/it/legal-it.ttl',
        f'{EXPORT_RDF_PATH}/legal/li/legal-li.ttl',
        f'{EXPORT_RDF_PATH}/legal/lt/legal-lt.ttl',
        f'{EXPORT_RDF_PATH}/legal/lu/legal-lu.ttl',
        f'{EXPORT_RDF_PATH}/legal/lv/legal-lv.ttl',
        f'{EXPORT_RDF_PATH}/legal/mt/legal-mt.ttl',
        f'{EXPORT_RDF_PATH}/legal/nl/legal-nl.ttl',
        f'{EXPORT_RDF_PATH}/legal/no/legal-no.ttl',
        f'{EXPORT_RDF_PATH}/legal/pl/legal-pl.ttl',
        f'{EXPORT_RDF_PATH}/legal/pt/legal-pt.ttl',
        f'{EXPORT_RDF_PATH}/legal/ro/legal-ro.ttl',
        f'{EXPORT_RDF_PATH}/legal/se/legal-se.ttl',
        f'{EXPORT_RDF_PATH}/legal/si/legal-si.ttl',
        f'{EXPORT_RDF_PATH}/legal/sk/legal-sk.ttl',
        f'{EXPORT_RDF_PATH}/legal/us/legal-us.ttl',

        ),
    'output': f'{EXPORT_RDF_PATH}/legal/legal',
},)

# === SPARQL Query Hooks ===
RDF_EXPORT_HOOK = {
    'pd': [ 
        {
            "title": "Derive concepts as instances of Special Category PD", 
            "query": f"""
            INSERT {{
                <{NAMESPACES['pd']['specialcategory-classes']}> a skos:ConceptScheme .
                ?s a dpv:SpecialCategoryPersonalData .
                ?s skos:inScheme <{NAMESPACES['pd']['specialcategory-classes']}> }}
            WHERE {{ ?s skos:broader+ dpv:SpecialCategoryPersonalData }}
            """,
        },
    ],
}
# add query for associating authority with laws in all jurisdictions
query = {
            "title": "add Authority to Law",
            "query": f"""
            INSERT {{
                ?law dpv:hasAuthority ?auth .
            }}
            WHERE {{
                {{ ?auth skos:broader eu-gdpr:DataProtectionAuthority }}
                UNION
                {{ ?auth skos:broader dpv:DataProtectionAuthority }}
                UNION
                {{ ?auth skos:broader dpv:Authority }}
                ?auth dpv:hasApplicableLaw ?law .
            }}
            """
        }
for loc in (
        'at','be','bg','cy','cz','de','dk','ee','es','eu',
        'fi','fr','gb','gr','hr','hu','ie','in','is','it',
        'li','lt','lu','lv','mt','nl','no','pl','pt','ro',
        'se','si','sk','us',):
    if f'legal-{loc}' not in RDF_EXPORT_HOOK:
        RDF_EXPORT_HOOK[f'legal-{loc}'] = []
    RDF_EXPORT_HOOK[f'legal-{loc}'].append(query)

# === guides ===
GUIDES = {
    'Primer': {
        'template': 'template_primer.jinja2',
        'output': '../primer/index.html',
    },
    'Consent-27560': {
        'template': 'template_guides_consent_27560.jinja2',
        'output': '../guides/consent-27560.html',
    },
    'Notice-29184': {
        'template': 'template_guides_privacy_notice_29184.jinja2',
        'output': '../guides/notice-29184.html',
    },
    'GDPR-ROPA': {
        'template': 'template_guides_gdpr_ropa.jinja2',
        'output': '../guides/gdpr-ropa.html',
    },
    'GDPR-DPIA': {
        'template': 'template_guides_gdpr_dpia.jinja2',
        'output': '../guides/gdpr-dpia.html',
    },
    'GDPR-Data-Breach': {
        'template': 'template_guides_gdpr_data_breach.jinja2',
        'output': '../guides/gdpr-data-breach.html',
    },
    'DPV-ODRL': {
        'template': 'template_guides_dpv_odrl.jinja2',
        'output': '../guides/dpv-odrl.html',
    },
    'DPV-OWL': {
        'template': 'template_guides_owl2.jinja2',
        'output': '../guides/dpv-owl.html',
    },
    'DPV-SKOS': {
        'template': 'template_guides_dpv_skos.jinja2',
        'output': '../guides/dpv-skos.html',
    },
    'DPV-MISC': {
        'template': 'template_guides_dpv_miscformats.jinja2',
        'output': '../guides/dpv-miscformats.html',
    },
    'Rights': {
        'template': 'template_guides_rights.jinja2',
        'output': '../guides/rights.html',
    },
}

# === examples ===
EXAMPLES = {}

# == functions ==

# === prefix-iri ===
def prefix_from_iri(iri):
    for prefix, ns in NAMESPACES.items():
        if iri.startswith(ns):
            term = iri.replace(ns, '')
            return f'{prefix}:{term}'
    return None

# === contributors ==
import json
with open('../contributors.json', 'r') as fd:
    contributors = json.load(fd)


def generate_author_affiliation(author):
    '''takes author name, returns affiliation'''
    author = str(author)
    if author in contributors:
        return contributors[author]
    return ''


def generate_authors_affiliations(authors):
    '''takes author name, returns affiliation'''
    authors = [contributors[author] for author in contributors]
    return authors