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
    'owl': 'xml', 
    'ttl': 'turtle', 
    'n3': 'n3',
    'jsonld': 'json-ld'
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
			# DEBUG(f'{prefix} namespace with IRI {iri}')

from rdflib import Graph
NS = Graph()
NS.ns = { k:v for k,v in NAMESPACES.items() }

# === Import/Export for RDF and HTML ===

# Root folder to import RDF files from
IMPORT_PATH = '..'
# Root folder to export HTML filese to
EXPORT_PATH = '..'
# Root folder where Jinja2 templates are stored
TEMPLATE_PATH = './jinja2_resources'

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
        'consent': {
            'properties': f'{IMPORT_CSV_PATH}/Consent_properties.csv',
        },
        'consent_types': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ConsentTypes.csv',
        },
        'consent_status': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ConsentStatus.csv',
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
            'taxonomy': f'{IMPORT_CSV_PATH}/Risk.csv',
            'properties': f'{IMPORT_CSV_PATH}/Risk_properties.csv',
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
        'data': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-data.csv',
        },
        'ops': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-ops.csv',
        },
        'security': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-security.csv',
        },
        'surveillance': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-surveillance.csv',
        },
        'provision': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-provision.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-provision-properties.csv',
        },
        'actors': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-actors.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-actors-properties.csv',
        },
        'comms': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-comms.csv',
        },
        'provision': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-provision.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-provision-properties.csv',
        },
        'tools': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-tools.csv',
        }, 
    },
    'risk': {
        'risk_consequences': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskConsequences.csv',
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
        'risk_assessment': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskAssessment.csv',
        },
        'risk_methodology': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskMethodology.csv',
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
    'legal-eu': {
        'eu': {
            'laws': f'{IMPORT_CSV_PATH}/legal-eu.csv',
        },
    },
    'legal-de': {
        'de': {
            'laws': f'{IMPORT_CSV_PATH}/legal-de.csv',
        },
    },
    'legal-gb': {
        'gb': {
            'laws': f'{IMPORT_CSV_PATH}/legal-gb.csv',
        },
    },
    'legal-ie': {
        'ie': {
            'laws': f'{IMPORT_CSV_PATH}/legal-ie.csv',
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
        'data_transfers': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_DataTransfers.csv',
        },
        'dpia': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_DPIA.csv',
            'properties': f'{IMPORT_CSV_PATH}/GDPR_DPIA_properties.csv',
        },
        'compliance': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_compliance.csv',
        },
        'legal_basis_rights_mapping': {
            'legal_basis_rights_mapping': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis_Rights_Mapping.csv',
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
    },
    'eu-rights': {
        'fundamental': {
            'taxonomy': f'{IMPORT_CSV_PATH}/EUFundamentalRights.csv',
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
            "dct:title": "DPV Examples",
            "dct:description": "Examples for/using DPVCG vocabularies",
            "dct:created": "2022-08-18",
            "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": "2",
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
            'entities': f'{IMPORT_PATH}/dpv/modules/entities.ttl',
            'entities-authority': f'{IMPORT_PATH}/dpv/modules/entities_authority.ttl',
            'entities-legalrole': f'{IMPORT_PATH}/dpv/modules/entities_legalrole.ttl',
            'entities-organisation': f'{IMPORT_PATH}/dpv/modules/entities_organisation.ttl',
            'entities-datasubject': f'{IMPORT_PATH}/dpv/modules/entities_datasubject.ttl',
            'legal_basis': f'{IMPORT_PATH}/dpv/modules/legal_basis.ttl',
            'legal_basis-consent': f'{IMPORT_PATH}/dpv/modules/consent.ttl',
            'legal_basis-consent-types': f'{IMPORT_PATH}/dpv/modules/consent_types.ttl',
            'legal_basis-consent-status': f'{IMPORT_PATH}/dpv/modules/consent_status.ttl',
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
            "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": "2",
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
            "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit, Axel Polleres",
            "schema:version": "2",
        },
    },
    'tech': {
        'vocab': f'{IMPORT_PATH}/tech/tech.ttl',
        'template': 'template_tech.jinja2',
        'export': f'{EXPORT_PATH}/tech',
        'modules': {
            'core': f'{IMPORT_PATH}/tech/modules/core.ttl',
            'data': f'{IMPORT_PATH}/tech/modules/data.ttl',
            'ops': f'{IMPORT_PATH}/tech/modules/ops.ttl',
            'security': f'{IMPORT_PATH}/tech/modules/security.ttl',
            'surveillance': f'{IMPORT_PATH}/tech/modules/surveillance.ttl',
            'provision': f'{IMPORT_PATH}/tech/modules/provision.ttl',
            'actors': f'{IMPORT_PATH}/tech/modules/actors.ttl',
            'comms': f'{IMPORT_PATH}/tech/modules/comms.ttl',
            'provision': f'{IMPORT_PATH}/tech/modules/provision.ttl',
            'tools': f'{IMPORT_PATH}/tech/modules/tools.ttl',
        },
        'metadata': {
            "dct:title": "Technology Concepts",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing information about technologies and its provision",
            "dct:created": "2022-06-15",
            "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit, Georg P Krog, Paul Ryan, Julian Flake",
            "schema:version": "0.8.2",
        },
    },
    'risk': {
        'vocab': f'{IMPORT_PATH}/risk/risk.ttl',
        'template': 'template_risk.jinja2',
        'export': f'{EXPORT_PATH}/risk',
        'modules': {
            'risk_consequences': f'{IMPORT_PATH}/risk/modules/risk_consequences.ttl',
            'risk_levels': f'{IMPORT_PATH}/risk/modules/risk_levels.ttl',
            'risk_matrix': f'{IMPORT_PATH}/risk/modules/risk_matrix.ttl',
            'risk_controls': f'{IMPORT_PATH}/risk/modules/risk_controls.ttl',
            'risk_assessment': f'{IMPORT_PATH}/risk/modules/risk_assessment.ttl',
            'risk_methodology': f'{IMPORT_PATH}/risk/modules/risk_methodology.ttl',
        },
        'metadata': {
            "dct:title": "Risk Concepts",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing information about risk assessment and risk management",
            "dct:created": "2022-08-14",
            "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit, Georg P Krog, Paul Ryan, Beatriz Esteves, Julian Flake",
            "schema:version": "0.8.2",
        },
    },
    'loc': {
        'vocab': f'{IMPORT_PATH}/loc/loc.ttl',
        'template': 'template_locations.jinja2',
        'export': f'{EXPORT_PATH}/loc',
        'modules': {
            'locations': f'{IMPORT_PATH}/loc/modules/locations.ttl',
        },
        'metadata': {
            "dct:title": "Location Concepts",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing (geo-political) locations and memberships",
            "dct:created": "2022-04-02",
            "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": "2",
        },
    },
    # LEGAL VOCABS
    'legal-eu': {
        'vocab': f'{IMPORT_PATH}/legal/eu/legal-eu.ttl',
        'template': 'template_legal_jurisdiction.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu',
        'modules': {
            'legal': f'{IMPORT_PATH}/legal/eu/legal-eu.ttl',
        },
        'metadata': {
            "dct:title": "Legal Concepts for European Union (EU)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for EU as jurisdiction",
            "dct:created": "2024-01-01",
            # "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": "2",
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
            "dct:title": "Legal Concepts for Germany",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Germany as jurisdiction",
            "dct:created": "2024-01-01",
            # "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": "2",
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
            "dct:title": "Legal Concepts for United Kingdom of Great Britain and Northern Ireland",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for United Kingdom of Great Britain and Northern Ireland as jurisdiction",
            "dct:created": "2024-01-01",
            # "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": "2",
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
            "dct:title": "Legal Concepts for Ireland",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for Ireland as jurisdiction",
            "dct:created": "2024-01-01",
            # "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": "2",
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
            "dct:title": "Legal Concepts for United States of America (USA)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing legal information for United States of America (USA) as jurisdiction",
            "dct:created": "2024-01-01",
            # "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": "2",
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
            "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": "2",
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
            'data_transfers': f'{IMPORT_PATH}/legal/eu/gdpr/modules/data_transfers.ttl',
            'dpia': f'{IMPORT_PATH}/legal/eu/gdpr/modules/dpia.ttl',
            'compliance': f'{IMPORT_PATH}/legal/eu/gdpr/modules/compliance.ttl',
            'legal_basis-rights_mapping': f'{IMPORT_PATH}/legal/eu/gdpr/modules/legal_basis_rights_mapping.ttl',
        },
        'metadata': {
            "dct:title": "EU General Data Protection Regulation (GDPR)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing information associated with EU GDPR",
            "dct:created": "2019-06-18",
            "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit, Axel Polleres",
            "schema:version": "2",
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
        },
        'metadata': {
            "dct:title": "EU Data Governance Act (DGA)",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing  information associated with EU DGA",
            "dct:created": "2023-09-20",
            "dct:modified": "2024-01-01",
            "dct:creator": "Beatriz Esteves, Harshvardhan J. Pandit, Georg P Krog",
            "schema:version": "2",
        },
    },
    'eu-rights': {
        'vocab': f'{IMPORT_PATH}/legal/eu/rights/eu-rights.ttl',
        'template': 'template_legal_eu_rights.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu/rights',
        'modules': {},
        'metadata': {
            "dct:title": "EU Fundamental Rights and Freedoms",
            "dct:description": "Extension to the Data Privacy Vocabulary (DPV) providing concepts for representing information associated with EU's Fundamental Rights and Freedoms",
            "dct:created": "2022-08-15",
            "dct:modified": "2024-01-01",
            "dct:creator": "Harshvardhan J. Pandit",
            "schema:version": "2",
        },
    },
}

# === exports ===
EXPORT_RDF_PATH = '..'
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
    'risk': {
        'main': f'{EXPORT_RDF_PATH}/risk',
        'modules': f'{EXPORT_RDF_PATH}/risk/modules',
    },
    'loc': {
        'main': f'{EXPORT_RDF_PATH}/loc',
        'modules': f'{EXPORT_RDF_PATH}/loc/modules',
    },
    'legal': {  # Consolidated graph of all legal data
        'main': f'{EXPORT_RDF_PATH}/legal',
    },
    'legal-eu': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu',
        'modules': f'{EXPORT_RDF_PATH}/legal/eu/modules',
    },
    'legal-de': {
        'main': f'{EXPORT_RDF_PATH}/legal/de',
        'modules': f'{EXPORT_RDF_PATH}/legal/de/modules',
    },
    'legal-gb': {
        'main': f'{EXPORT_RDF_PATH}/legal/gb',
        'modules': f'{EXPORT_RDF_PATH}/legal/gb/modules',
    },
    'legal-ie': {
        'main': f'{EXPORT_RDF_PATH}/legal/ie',
        'modules': f'{EXPORT_RDF_PATH}/legal/ie/modules',
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
        f'{EXPORT_RDF_PATH}/legal/eu/legal-eu.ttl',
        f'{EXPORT_RDF_PATH}/legal/de/legal-de.ttl',
        f'{EXPORT_RDF_PATH}/legal/ie/legal-ie.ttl',
        f'{EXPORT_RDF_PATH}/legal/gb/legal-gb.ttl',
        f'{EXPORT_RDF_PATH}/legal/us/legal-us.ttl',
        ),
    'output': f'{EXPORT_RDF_PATH}/legal/legal',
},)

# === SPARQL Query Hooks ===
RDF_EXPORT_HOOK = {
    'pd': [ # Create concept scheme for Special Category Personal Data
        # Derive all concepts that are instances of SCPD
        f"""
        INSERT {{
            <{NAMESPACES['pd']['specialcategory-classes']}> a skos:ConceptScheme .
            ?s a dpv:SpecialCategoryPersonalData .
            ?s skos:inScheme <{NAMESPACES['pd']['specialcategory-classes']}> }}
        WHERE {{ ?s skos:broader+ dpv:SpecialCategoryPersonalData }}
        """,
    ],
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