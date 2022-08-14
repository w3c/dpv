#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''Downloads the DPV spreadsheets in CSV form'''

# Google Export link
GOOGLE_EXPORT_LINK = (
    'https://docs.google.com/spreadsheets/d/'
    '%s/gviz/tq?tqx=out:csv&sheet=%s')

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
    'Consent',
    'Consent_properties',
    # ----- EXTENSIONS -----
    'dpv-pd',
    # DPV-GDPR
    'GDPR_LegalBasis',
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
    # Risk
    'Consequences',
    'RiskLevels',
    'RiskMatrix',
    'RiskControls',
    'RiskAssessmentTechniques',
    # Rights
    'EUFundamentalRights',
    )

from urllib import request


def download_csv(document_id, sheet_name, save_path='./vocab_csv'):
    '''Download the sheet and save to given path'''
    url = GOOGLE_EXPORT_LINK % (document_id, sheet_name)
    print(f'Downloading {sheet_name}...', end='')
    try:
        request.urlretrieve(url, f'{save_path}/{sheet_name}.csv')
        print('DONE')
    except Exception as E:
        print(f'ERROR :: {E}')


if __name__ == '__main__':
    for sheet in DPV_SHEETS:
        download_csv(DPV_DOCUMENT_ID, sheet)
