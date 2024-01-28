# Documentation generator for DPV vocabularies

The documentation generator is responsible for producing the HTML and RDF-based outputs. It downloads a bunch of spreadsheets containing the data for DPV and other vocabularies (such as DPV-GDPR), converts it to RDF serialisations, and generates HTML documentation using the W3C ReSpec template.

The Data Privacy Vocabulary (DPV) is available at https://w3id.org/dpv and its repository is at https://github.com/w3c/dpv. 

## Quick Summary

There are 3 scripts to executre for each of the three tasks.

`./001_download_vocab_in_csv.py` will download the CSV data from a Google Sheets document and store it in the `vocab_csv` path specified. The outcome will be a CSV file for each sheet.

`./002_parse_csv_to_rdf.py` will create RDF serialisations for DPV using data from CSV. It will create different serialisation files for each 'module' and also for DPV combined.

In between steps 2 and 3, there can be a series of tests done to ensure the RDF is generated correctly. For this, some basic SHACL constraints are defined in `shacl_shapes`.

`./003_generate_respec_html.py` will generate HTML documentation for DPV and DPV-GDPR from RDF.

The `9**` series offers convenience in running the other scripts in some combination. `902` executes all the RDF generation scripts, `903` executes all the HTML generation scripts, and `999` executes all scripts.

In addition to these, `1**` series offers convenience with tasks. `101` converts the DPV-OWL RDF files into OWL (Manchester Syntax). It will be run automatically through the `902` script so that every update will auto-generate these files.

The `8**` series provides packaging and release management tasks. `801` will generate zips for creating a new release, stored in `repo-base/releases` which is gitignored. 

## Requirements

- Internet connectivity - for downloading the spreadsheets from Google Sheets hosting the DPV terms and metadata with `100` script.
- Python 3.11+ (preferably as close to the latest version as possible) - for executing scripts
- Python modules to be installed using `pip` - see `requirements.txt`
- Java runtime 18+ (preferably as close to the latest version as possible) - for executing SHACL validations
- TopBraid SHACL validation binary from https://github.com/TopQuadrant/shacl (grab the latest release from https://repo1.maven.org/maven2/org/topbraid/shacl/)
- Ontology Converter v2.0 from https://github.com/sszuev/ont-converter (grab the latest release from https://github.com/sszuev/ont-converter/releases) - required to convert RDF to Manchester Syntax with `101` script.

## How everything works

### Downloading CSV data

This uses the Google Sheet export link to download the sheet data in CSV form. Needs specifying the document ID in `DPV_DOCUMENT_ID` variable and listing the sheet name(s) in `DPV_SHEETS`. The default save path for CSV is `vocab_csv`.

### Converting to RDF

This uses `rdflib` to generate the RDF data from CSV. It uses `DPV_CSV_FILES` to retrieve classes and properties from the CSV and render them in RDF serialisations. Namespaces are manually represented in the top of the document and are automatically handled in text as URI references. Serialisations to be produced are registered in `RDF_SERIALIZATIONS` variable.

The variables for CSV inputs and RDF outputs are:

* `IMPORT_CSV_PATH` defines where the CSV files are stored, with default value `./vocab_csv`
* `EXPORT_DPV_PATH` defines where the DPV rdf files are stored, with default value `../dpv`
* `EXPORT_DPV_MODULE_PATH` defines where the DPV module files are stored, with default value `../dpv/modules`
* `EXPORT_DPV_GDPR_PATH`  defines where the DPV-GDPR files are stored, with default value `../dpv-gdpr`

There are three main classes responsible for generation of metadata:

* `add_common_triples_for_all_terms` will add common metadata for each term, such as label, description, author, and so on
* `add_triples_for_classes` will add metadata for classes such as subclass
* `add_triples_for_properties` will add metadata for properties such as domain, range, sub-property

### Generating HTML documentation

This uses `jinja2` to render the HTML file from a template. The data is loaded using a module called `rdform` which is meant to provide ORM features and convenience features over RDF data. 

The variables for RDF inputs and HTML outputs are:

* `IMPORT_DPV_MODULES_PATH` defines where the RDF for DPV modules are loaded from, with default value `../dpv/modules`
* `IMPORT_DPV_GDPR_PATH` defines where the RDF for DPV-GDPR module is loaded from,  with default value `../dpv-gdpr`
* `EXPORT_DPV_HTML_PATH` defines where the output HTML for DPV documentation is stored, with default value `../dpv`, the generated file is `index.html`
* `EXPORT_DPV_GDPR_HTML_PATH` defines where the output HTML for DPV-GDPR documentation is stored, with default value `../dpv-gdpr`, the generated file is `index.html`

The general flow of steps in the script is along the following lines:

1. Load RDF instances from a module file with the `load_data` function. 
2. This creates a RDF graph using `rdflib` and extracts classes and properties from it in separate variables as `{module}_classes` and `{module}_properties`
3. Create HTML using a `jinja2` template, which is located in `jinja2_resources`. The tempalte for dpv is `template_dpv.jinja2`.
4. The template uses a macro to repeat the same table and metadata records for each module and term. The macro is defined in `macro_term_table.jinja2`. The template file itself contains the other information such as headlines and paragraphs.

### Testing using SHACL

The folder `shacl_shapes` holds the constraints in `shapes.ttl` to verify the vocabulary terms contain some basic annotations. The script `verify.py` executes the SHACL validator (currently hardcoded to use the [TopBraid SHACL](https://github.com/TopQuadrant/shacl) binary as `shaclvalidate.sh`), retrieves the results, runs a SPARQL query on them to get the failing nodes and messages.

The script uses `DATA_PATHS` to declare what data files should be validated. Currently, it will only validate `Turtle (.ttl)` files for simplicity as all files are duplicate serialisations of each other. The variable `SHAPES` declares the list of shape files to use. For each folder in `DATA_PATHS`, the script will execute the SHACL binary to check constraints defined in each of the `SHAPES` files.

To execute the tests, and to use the TopBraid SHACL binary, download the latest release from [maven](https://repo1.maven.org/maven2/org/topbraid/shacl/), extract it somewhere and note the path of the folder. Export `SHACLROOT` in the shell the script is going to run in (or e.g. save it in the bash profile) to the path of the folder. To be more precise, `$SHACLROOT/shaclvalidate.sh` should result in the binary being executed. 

The output of the script lists the data and shapes files being used in the validation process, the number of errors found, and a list of data nodes and the corresponding failure message.

## FAQ

1. Fixing an error in the vocabulary terms i.e. term label, property, annotation --> Make the changes in the Google Sheet, and run scripts to download CSV, parse RDF, and generate HTML
2. Fixing an error in serialisation e.g. rdf:Property is defined as rdfs:Propety --> Make the changes in the `002` script for generating RDF, and generate HTML
3. Changing content in HTML documentation e.g. change motivation paragraph --> Make the changes in the relevant `template` and generate HTML