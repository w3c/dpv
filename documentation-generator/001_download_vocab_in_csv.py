#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''Downloads the DPV spreadsheets in CSV form'''

# Google Export link
GOOGLE_EXPORT_LINK = (
    'https://docs.google.com/spreadsheets/d/'
    '%s/gviz/tq?tqx=out:csv&sheet=%s')
# Google Excel Export link
GOOGLE_EXCEL_EXPORT_LINK = (
    'https://docs.google.com/spreadsheets/d/'
    '%s/export?exportFormat=xlsx&format=xlsx&title=%s')

# The document *must* be publicly viewable (minimum permissions)
# The document ID is found within the URL
DPV_DOCUMENT_ID = '11bjy424zwC_j4bj9pnhmmI8o7RgrJfX4NgsZ31iR3Wo'
# The sheet names are assumed to be valid IRIs
# If they are not, escape them for IRI/HTML representation
DPV_SHEETS = (
    # Namespaces
    'Namespaces',
    'Namespaces_Other',
    # DPV
    'BaseOntology',
    'BaseOntology_properties',
    'PersonalData',
    'PersonalData_properties',
    'Purpose',
    'Purpose_properties',
    'Context',
    'Context_properties',
    'Status',
    'Status_properties',
    'Risk',
    'Risk_properties',
    'Processing',
    'Processing_properties',
    'ProcessingContext',
    'ProcessingContext_properties',
    'ProcessingScale',
    'ProcessingScale_properties',
    'TechnicalOrganisationalMeasure',
    'TechnicalOrganisationalMeasure_properties',
    'TechnicalMeasure',
    'OrganisationalMeasure',
    'Entities',
    'Entities_properties',
    'Entities_Authority',
    'Entities_Authority_properties',
    'Entities_LegalRole',
    'Entities_LegalRole_properties',
    'Entities_Organisation',
    'Entities_DataSubject',
    'Entities_DataSubject_properties',
    'Jurisdiction',
    'Jurisdiction_properties',
    'LegalBasis',
    'LegalBasis_properties',
    'ConsentTypes',
    'ConsentStatus',
    'Consent_properties',
    # ----- EXTENSIONS -----
    'dpv-pd',
    # DPV-GDPR
    'GDPR_LegalBasis',
    'GDPR_LegalBasis_SpecialCategory',
    'GDPR_LegalBasis_DataTransfer',
    'GDPR_LegalRights',
    'GDPR_DataTransfers',
    'GDPR_DPIA',
    # DPV-Legal
    'legal_properties',
    'legal_Locations',
    'legal_Laws',
    'legal_Authorities',
    'legal_EU_EEA',
    'legal_EU_Adequacy',
    # DPV-Technology
    'dpv-tech',
    'dpv-tech_properties',
    'tech_algorithms',
    # Risk
    'RiskConsequences',
    'RiskLevels',
    'RiskMatrix',
    'RiskControls',
    'RiskAssessmentTechniques',
    'RiskManagement',
    'RiskMethodology',
    # Rights
    'EUFundamentalRights',
    # EXTRA - unused currently
    'Standards_ISO',
    )

from urllib import request


def download_document(
        document_id, document_name, export_link,
        save_path='./vocab_csv', ext='csv'):
    '''Download the sheet and save to specified path in specified format'''
    url = export_link % (document_id, document_name)
    print(f'Downloading {document_name}.{ext} ...', end='')
    try:
        request.urlretrieve(url, f'{save_path}/{document_name}.{ext}')
        print(f'DONE.')
    except Exception as E:
        print(f'ERROR :: {E}')


if __name__ == '__main__':
    for sheet in DPV_SHEETS:
        download_document(
            document_id=DPV_DOCUMENT_ID, 
            document_name=sheet,
            export_link=GOOGLE_EXPORT_LINK)
    # Spreadsheet as Excel
    download_document(
        document_id=DPV_DOCUMENT_ID,
        document_name='dpv_terms_discussion',
        export_link=GOOGLE_EXCEL_EXPORT_LINK,
        ext='xlsx')
