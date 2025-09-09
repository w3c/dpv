import os
import shutil

from vocab_management import DPV_VERSION

if not os.path.exists('../releases'):
    os.makedirs('../releases')

shutil.make_archive(
    f'../releases/dpv-v{DPV_VERSION}',
    'zip',
    f'../{DPV_VERSION}')

print(f'generated ../releases/dpv-v{DPV_VERSION}.zip')