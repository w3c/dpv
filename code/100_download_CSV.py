#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

# This script will Download Spreadsheets and Extract CSVs.
# The spreadsheets are currently stored in a [shared google drive
# folder](https://drive.google.com/drive/folders/1oDJBjxukEZantJL82gg4zbiRugRqyePT)
# from which the spreadsheet file IDs are used to download the
# entire document as Excel (.xlsx) and then individual CSVs are
# extracted from it using an external tool [xlsx2csv
# ](https://github.com/dilshod/xlsx2csv).

import logging
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

# == Export ==

# This is the Google Excel Export link which requires the
# document ID to download the document as XLSX
GOOGLE_EXCEL_EXPORT_LINK = (
    'https://docs.google.com/spreadsheets/d/'
    '%s/export?exportFormat=xlsx&format=xlsx&title=%s')
# Documents are to be stored in this folder
DOCS_FOLDER = './vocab_csv'

# == DPV Files == 
DPV_FILES = {
    # The files to download are indicated in the following structure:
    # Each group/dictionary represents the
    # 'document level' grouping - this is the collection
    # of 'sheets' in a single document
    # The documents in Google Drive are organised per 
    # topic already, so this mapping reflects that.
    'namespaces': { 
    # The name is the document name the downloaded file is saved as
        'name': 'namespaces', 
    # The ID of the document through which it is downloaded
    # (obtained by copying the info in
    # link where https://docs.google.com/spreadsheets/d/`<DOC_ID>`)
        'doc_id': '1x5Wfl-2Xp22R89lhNwNpYP0xN0zfQLFlNe3On6pwNM4',
        # Only the list of 'sheets' will be downloaded
        'sheets': ( 
            # > Note: the 'name' of the 'sheet' MUST be exact
            'Namespaces', 
            'Namespaces_Other', 
            ),
    },
    'process': { 
        'name': 'process', 
        'doc_id': '17wwwFpE11KzWAkmWkrJDqUMZq2AhStcAqBjcWE2wMEM',
        'sheets': ( 
            'Process', 
            'Process_properties',
            ),
    },
    # Sheets for Data concepts in main DPV and Personal Data extension
    'pd': { 
        'name': 'pd',
        'doc_id': '1SI6gZh9-dq1rf_etfrlYHj0QZwq9Vd25f_OHPX5hbSQ',
        'sheets': (
            'PersonalData', 
            'PersonalData_properties', 
            'pd-core',
            'pd-extended',
            ),
    },
    # Sheets for Purpose, Processing, and Processing Context/Scale
    'purpose_processing': {
        'name': 'purpose_processing',
        'doc_id': '1ePg6BU2Zp9fiSDuEnKuVi6dIRrFLEVdatbVxjHRk-8s',
        'sheets': (
           'Purpose', 
           'Purpose_properties', 
           'Processing', 
           'Processing_properties', 
           'ProcessingContext', 
           'ProcessingContext_properties', 
           'ProcessingScale', 
           'ProcessingScale_properties',
           'Purpose_Education',
           'Purpose_Infrastructure',
           'Purpose_PublicServices',
           'Purpose_Justice',
           'Purpose_Healthcare',
           'Purpose_Finance',
           ),
    },
    # Sheets for Context and Statuses
    'context_status': {
        'name': 'context_status',
        'doc_id':  '1VPQW1DanprQhMwnhSqyKSGbEXdTmLHdc6UjpWJhyLMA', 
        'sheets': (
            'Context', 
            'Context_properties', 
            'Status', 
            'Status_properties',
            ),
    },
    # Sheets for Tech/Org Measures
    'toms': {
        'name': 'toms',
        'doc_id':  '16d0_k6ueoXxXRTgecih9Ny7NpeXYF8icm4QX99cPYJA', 
        'sheets': (
            'TOM', 
            'TOM_properties', 
            'TechnicalMeasure', 
            'OrganisationalMeasure',
            'LegalMeasure',
            'PhysicalMeasure',
            'Notice',
            'Notice_properties',
            ),
    },
    # Sheets for Entities
    'entities': {
        'name': 'entities',
        'doc_id':  '1g6zLqVt5FlNlgsXq_NW2W9INv3KdGEFjJCyOd03UmOg', 
        'sheets': (
            'Entities', 
            'Entities_properties', 
            'Entities_Authority', 
            'Entities_Authority_properties', 
            'Entities_LegalRole', 
            'Entities_LegalRole_properties', 
            'Entities_Organisation', 
            'Entities_DataSubject', 
            'Entities_DataSubject_properties',
            ),
    },
    # Sheets for Locations and Jurisdiction
    'location_jurisdiction': {
        'name': 'location_jurisdiction',
        'doc_id': '19exhY34jq6VDApRp2abHD-br6rpm6Q7BOP7H_pm5sKM',
        'sheets': (
            'Jurisdiction', 
            'Jurisdiction_properties', 
            'location',
            'location_properties',
            'location_memberships',
            ),
    },
    # Sheets for Legal Basis and Consent
    'legal_basis': {
        'name': 'legal_basis',
        'doc_id':  '13Ub4LXHruocffYnd7JKCMvzi1MYv3Gy61d3UmQBhARc', 
        'sheets': (
            'LegalBasis', 
            'LegalBasis_properties', 
            'ConsentTypes', 
            'ConsentStatus', 
            'Consent_properties',
            'ConsentControls',
            'ContractTypes',
            'ContractStatus',
            'ContractClause',
            'ContractControl',
            'Contract_properties',
            'LegalBasisStatus',
            ),
    },
    # Sheets for Tech extension
    'tech': {
        'name': 'tech',
        'doc_id': '1GVmF4c7b-9xMSs0TyT45kXoCLLUVs8bbW34tfcozbuA',
        'sheets': (
            'tech-core',
            'tech-core-properties',
            'tech-io',
            'tech-provision',
            'tech-actors',
            'tech-actors-properties',
            'tech-comms',
            'tech-docs',
            'tech-status',
            'tech-status-properties',
            'tech-tools',
            'tech-tools-properties',
            ),
    },
    'ai': {
        'name': 'ai',
        'doc_id': '1H3nSZ6Z4GL5ZdaVKrH2_oZPc8sRvNg-MiiosZE-qAOo',
        'sheets': (
            'ai-core',
            'ai-properties',
            'ai-systems',
            'ai-data',
            'ai-data-properties',
            'ai-techniques',
            'ai-capabilities',
            'ai-measures',
            'ai-lifecycle',
            'ai-risks',
            ),
    },
    # Sheets for Risk extension
    'risk': {
        'name': 'risk',
        'doc_id': '1y8r3Vk-_Gi1MqbyAM6Ot4DoNDJpa2ZVhCyCyFQkGBy0',
        'sheets': (
            'dpv-Risk', 
            'dpv-Risk_properties', 
            'RiskManagement', 
            'RiskManagement_properties', 
            'RiskLevels', 
            'RiskMatrix', 
            'RiskControls',
            'RiskControls_properties', 
            'RiskSource',
            'Incident',
            'Incident_properties',
            'IncidentStatus',
            'RiskEvents',
            ),
    },
    # Sheets for Rights extension
    'rights': {
        'name': 'rights',
        'doc_id': '1XW-L6rGWbgGGp62q8eA22SWvh4wUWK5BpC0zfD6wAxM',
        'sheets': (
            'Rights', 
            'Rights_properties', 
            'EUFundamentalRights',
            'EUFundamentalRights_Impacts',
            ),
    },
    # Sheets for Rules extension
    'rules': {
        'name': 'rules',
        'doc_id':  '1SDmlzSo1Ax_35v754Jzx4oFGKvGo5nyNtEAL0vSBbM0', 
        'sheets': (
            'Rules', 
            'Rules_properties',
            ),
    },
    # Sheets for Standards extension
    'standards': {
        'name': 'standards',
        'doc_id': '1z-qaB2m6lD1ROmPVf9yhfG05D68Z7H4glYLERj6ZCRk',
        'sheets': (
            'Standards_ISO',
            ),
    },
    # Sheets for Justifications extension
    'justifications': {
        'name': 'justifications',
        'doc_id': '1fZu0J-Z18NZDNZusmmYPGoek5Q0zjKioIrdzqlBO00E',
        'sheets': (
            'Justifications_NotRequired',
            'Justifications_NonFulfilment',
            'Justifications_Delay',
            'Justifications_Exercise',
            ),
    },
    # Sheets for Legal extension
    'laws-authorities': {
        'name': 'laws-authorities',
        'doc_id': '1pqGE67I5kyoGrkhMItJbi18VLguVqE1jVecnfki1ujY',
        'sheets': (
            'legal-at',
            'legal-be',
            'legal-bg',
            'legal-cy',
            'legal-cz',
            'legal-de',
            'legal-dk',
            'legal-ee',
            'legal-es',
            'legal-eu',
            'legal-fi',
            'legal-fr',
            'legal-gb',
            'legal-gr',
            'legal-hk',
            'legal-hr',
            'legal-hu',
            'legal-ie',
            'legal-in',
            'legal-is',
            'legal-it',
            'legal-jp',
            'legal-kr',
            'legal-li',
            'legal-lt',
            'legal-lu',
            'legal-lv',
            'legal-mo',
            'legal-mt',
            'legal-my',
            'legal-nl',
            'legal-no',
            'legal-ph',
            'legal-pl',
            'legal-pt',
            'legal-ro',
            'legal-se',
            'legal-sg',
            'legal-si',
            'legal-sk',
            'legal-th',
            'legal-tw',
            'legal-us',
            )
    },
    # Sheets for EU-GDPR extension
    'eu-gdpr': {
        'name': 'eu-gdpr',
        'doc_id': '1lDJZpl0UND8Bm_4iWKVQtgmMUz0YwP2R63CgP7Gro-U',
        'sheets': (
            'GDPR_MiscConcepts',
            'GDPR_LegalBasis', 
            'GDPR_LegalBasis_SpecialCategory', 
            'GDPR_LegalBasis_DataTransfer', 
            'GDPR_LegalRights', 
            'GDPR_LegalRights_Impacts', 
            'GDPR_LegalBasis_Rights_Mapping', 
            'GDPR_LegalRights_Justifications',
            'GDPR_DataTransfers', 
            'GDPR_DPIA',
            'GDPR_DPIA_properties',
            'GDPR_DataBreach',
            'GDPR_compliance',
            'GDPR_entities',
            'GDPR_entities_properties',
            'GDPR_principles',
            # 'GDPR_Justificiations',
            ),
    },
    # Sheets for EU-DGA extension
    'eu-dga': {
        'name': 'eu-dga',
        'doc_id':  '1wKsf0Vqr0Gg1C91MqshtI5tjGXmQvXu4p4xF0yK0KaA',
        'sheets': (
            'DGA_LegalBasis',
            'DGA_LegalRights',
            'DGA_LegalRights_Impacts',
            'DGA_Services',
            'DGA_Registers',
            'DGA_TOMs',
            'DGA_entities',
            'DGA_properties',
            'DGA_compliance',
            ),
    },
    'eu-aiact': {
        'name': 'eu-aiact',
        'doc_id': '17WAXH7Bkzu2m2eeOSTyhJBeHp9nst988KYCSRES8xCE',
        'sheets': (
            'aiact-system',
            'aiact-capability',
            'aiact-risk',
            'aiact-data',
            'aiact-roles',
            'aiact-docs',
            'aiact-status',
            'aiact-status-properties',
            'aiact-misc',
            'aiact-assessment',
            'aiact-compliance',
            'aiact-sector',
            ),
    },
    'eu-nis2': {
        'name': 'eu-nis2',
        'doc_id': '1uh14-RUYQuKiouu2Cahi-voaKBCw5D4lPE4w5NaqDPc',
        'sheets': (
            'NIS2_Notice',
            'NIS2_compliance',
            ),
    },
    'eu-ehds': {
        'name': 'eu-ehds',
        'doc_id': '1pEyUXsCsMKMjVFODOpYRmL_q_Z6_1evCz6GXF8UV5ZY',
        'sheets': (
            'EHDS_Data',
            'EHDS_Purpose',
            'EHDS_Entities',
            'EHDS_Process',
            ),
    },
    # Standards - P7012
    'p7012': {
        'name': 'p7012',
        'doc_id': '1mhnDukj_OHNJJPoG8Yu4FsbPdyeb9FFl_2xXnYemOGU',
        'sheets': (
            'p7012_entities',
            'p7012_entities_properties',
            'p7012_process',
            'p7012_process_properties',
            'p7012_agreement',
            'p7012_status',
            'p7012_data',
            'p7012_purpose',
            'p7012_privacy_term',
            'p7012_privacy_term_properties',
            ),
    },
    # Sheets for Use-Cases, Requirements, and Examples
    'ucr': {
        'name': 'ucr',
        'doc_id': '1__STWvOEZRc1u2J-8teOYjLpnTPlZ80_ebTytrUlWgQ',
        'sheets': (
            'UseCase',
            'Requirement',
            'Example',
            ),
    },
    # Sheets for Translations
    'translations': {
        'name': 'translations',
        'doc_id': '1HqIWw8VdWatYnbRwKoW3gAdXWmVTnSAJ9d9x8FSDsWM',
        'sheets': (
            'DE_prod',
            'DE_verify',
            'DE_glossary',
            # TODO: Add sheets for FR, IT, etc. languages
            )
    },
    # Mappings
    'mappings': {
        'name': 'mappings',
        'doc_id': '1g6t_axf8VPW0I_iqOrRe6iaUCvrtIDPphbSgwB6couE',
        'sheets': (
            'Mapping_ODRL',
        )
    },
}

# == Downloading files ==
from urllib import request


def download_document(
    document_id:str, document_name:str, export_link:str, ext:str='xlsx') -> None:
    '''Download the document and save to specified path in specified format'''
    # - `document_id`: ID of document to be downloaded
    # - `document_name`: name to save the document with
    # - `export_link`: string template to call to download the document 
    #   (this will be the google export link)
    # - `ext`: extension to save the document as (XLSX default)
    url = export_link % (document_id, document_name)
    try:
        request.urlretrieve(url, f'{DOCS_FOLDER}/{document_name}.{ext}')
        INFO(f'Downloaded {document_name}.{ext}')
    except Exception as E:
        logging.error(f'ERROR :: {E}')


def _download_spreadsheets(document_id, document_name, export_link):
    # This is just a wrapper function that calls `download_document`
    # with the Google excel export link
    download_document(
        document_id=document_id,
        document_name=document_name,
        export_link=GOOGLE_EXCEL_EXPORT_LINK,
        ext='xlsx')


def _extract_CSVs(document_name, sheets):
    # Extracts sheets from XLSX file and saves them as individual CSVs
    # > Note: XLSX2CSV is an **external** tool called as a subprocess
    INFO(document_name)
    import subprocess
    for sheet_name in sheets:
        with open(f'{DOCS_FOLDER}/{sheet_name}.csv', 'w') as outfile:
            subprocess.run(["xlsx2csv", f"{DOCS_FOLDER}/{document_name}.xlsx", "-i", "-n", f"{sheet_name}"], stdout=outfile)
        INFO(f'Wrote {sheet_name}.csv from {document_name}.xlsx')


def _download_all_spreadsheets():
    # Iterate and download all spreadsheets 
    # as specified in DPV_FILES variable
    for data in DPV_FILES.values():
        doc_id = data['doc_id']
        document_name = data['name']
        _download_spreadsheets(
            doc_id, document_name, GOOGLE_EXCEL_EXPORT_LINK)


def _extract_all_CSVs():
    # Iterate and extract all CSVs 
    # as specified in the DPV_FILES variable
    for data in DPV_FILES.values():
        document_name = data['name']
        sheets = data['sheets']
        _extract_CSVs(document_name, sheets)


# == script ==
if __name__ == '__main__':
    # The script has a default behaviour where it will NOT download
    # any file and will extract ALL CSVs from existing files.
    import argparse
    parser = argparse.ArgumentParser()
    # - `-d` will download and extract ALL files
    parser.add_argument('-d', '--d', action='store_true', help="download data files")
    # - `-x` will extract ALL files
    parser.add_argument('-x', '--x', action='store_true', default=True, help="extract CSVs from all data files")
    # - `-ds <foo>` will download and extract ONLY `foo` files
    parser.add_argument('--ds', nargs='+', default=False, help="download only indicated data files")
    # - `-xs <foo>` will extract ONLY `foo` files
    parser.add_argument('--xs', nargs='+', default=False, help="extract CSVs from indicated data files")
    args = parser.parse_args()

    # If files are to be downloaded, do the following.
    if args.d or args.ds:
        INFO('-'*40)
        INFO('Downloading spreadsheets...')
        INFO('-'*40)
        if not args.ds: # download all files
            _download_all_spreadsheets()
            args.x = True # set extraction param
        else: # download only indicated files
            if not args.ds:
                args.ds = [] # error handling for empty input
            for document_name in args.ds:
                if document_name not in DPV_FILES:
                    raise NameError(f'{document_name} is not a DPV File')
                _download_spreadsheets(
                    DPV_FILES[document_name]['doc_id'],
                    document_name, GOOGLE_EXCEL_EXPORT_LINK)
            args.xs = args.ds # set extraction queue to be same as download
        INFO('-'*40)
    # If files are to be extracted do the following.
    if args.x is True:
        INFO('-'*40)
        INFO('Extracting CSVs...')
        INFO('-'*40)
        if not args.xs: # extract all CSVs
            _extract_all_CSVs()
        else: # extract specified CSVs
            if not args.xs:
                args.xs = [] # error handling for empty input
            for document_name in args.xs:
                if document_name not in DPV_FILES:
                    raise NameError(f'{document_name} is not a DPV File')
                _extract_CSVs(
                    document_name, DPV_FILES[document_name]['sheets'])
        INFO('-'*40)
