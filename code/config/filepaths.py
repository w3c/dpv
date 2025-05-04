from version import DPV_VERSION

#= Documentation Generator =#

GOOGLE_EXCEL_EXPORT_LINK = (
    'https://docs.google.com/spreadsheets/d/'
    '%s/export?exportFormat=xlsx&format=xlsx&title=%s')

# folder where downloaded CSVs are stored
FILEPATH_CSV = 'vocab_csv'
# folder where Jinja2 templates are stored
TEMPLATE_PATH = './jinja2_resources'

#= Outputs =#

#  folder where exported files are stored
OUTPUT_PATH = f'../{DPV_VERSION}'
GUIDES_PATH = f"../guides"
MAPPINGS_PATH = f"../mappings"
EXAMPLES_PATH = f"../examples"
