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
    # DPV
    'BaseOntology',
    'BaseOntology_properties',
    'PersonalDataCategory',
    'Purpose',
    'Purpose_properties',
    'Processing',
    'Processing_properties',
    'TechnicalOrganisationalMeasure',
    'TechnicalOrganisationalMeasure_properties',
    'Entities',
    'Entities_properties',
    'Consent',
    'Consent_properties',
    # DPV-GDPR
    'GDPR_LegalBasis',
    'GDPR_LegalRights',
    )

from urllib import request


def download_csv(document_id, sheet_name, save_path='./vocab_csv'):
    '''Download the sheet and save to given path'''
    url = GOOGLE_EXPORT_LINK % (document_id, sheet_name)
    print(f'Downloading {sheet_name}...', end='')
    request.urlretrieve(url, f'{save_path}/{sheet_name}.csv')
    print('DONE')


if __name__ == '__main__':
    for sheet in DPV_SHEETS:
        download_csv(DPV_DOCUMENT_ID, sheet)
