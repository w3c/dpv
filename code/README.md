# Documentation generator for DPV vocabularies

The documentation generator is responsible for producing the HTML and RDF-based outputs. It downloads a bunch of spreadsheets containing the data for DPV and other vocabularies (such as DPV-GDPR), converts it to RDF serialisations, and generates HTML documentation using the W3C ReSpec template.

The Data Privacy Vocabulary (DPV) is available at https://w3id.org/dpv and its repository is at https://github.com/w3c/dpv. 

## Quick Summary

There are 3 scripts to executre for each of the three tasks.

If you have updated concepts or want to regenerate the spreadsheets from which all RDF and HTML is produced - use `./100_download_CSV.py` (by default it will download and extract all spreadsheets). You can use `--ds <name>` to only download and extract specific spreadsheets. See the _Downloading CSV data_ section below for more information on this.

If you want to generate the RDF files - `./200_serialise_RDF.py` which will will create RDF serialisations for all DPV modules and extensions.

If you want to generate the HTML files - `./300_generate_HTML.py` will generate HTML documentation for all DPV modules and extensions. To only generate the HTML for guides, use `./300_generate_HTML.py --guides`.

To generate the zip files for publishing DPV releases on GitHub, use `./900_generate_releases.sh`, which will produce zip files in `releases` folder.

To change metadata and config for the above processes, see `vocab_management.py`

## Requirements

- Internet connectivity - for downloading the spreadsheets from Google Sheets hosting the DPV terms and metadata with `100` script.
- Python 3.11+ (preferably as close to the latest version as possible) - for executing scripts
- Python modules to be installed using `pip` - see `requirements.txt`

The below are optional additional requirements for publishing DPV in alternate serialisations:

- Ontology Converter v2.0 from https://github.com/sszuev/ont-converter (grab the latest release from https://github.com/sszuev/ont-converter/releases) - required to convert RDF to Manchester Syntax with `201` script.

The below are optional additional requirements for validations using SHACL:

- Java runtime 18+ (preferably as close to the latest version as possible) - for executing SHACL validations (this is optional)
- TopBraid SHACL validation binary from https://github.com/TopQuadrant/shacl (grab the latest release from https://repo1.maven.org/maven2/org/topbraid/shacl/)

## How everything works

### Downloading CSV data

`./100_download_CSV.py` will download the CSV data from a Google Sheets document and store it in the `vocab_csv` path specified. The outcome will be a CSV file for each sheet. To only download and generate the CSVs for specific modules/extensions, use `--ds <name>` where `name` is the key in `DPV_FILES` present in the script. E.g. to download spreadsheets containing purposes, use `--ds purpose_processing`. Running the script without any parameters will download and extract all spreadsheets.

This uses the Google Sheet export link to download the sheet data in CSV form. Needs specifying the document ID in `DPV_DOCUMENT_ID` variable and listing the sheet name(s) in `DPV_SHEETS`. The default save path for CSV is `vocab_csv`. This results in downloading the Google Sheet as a Excel spreadsheet and then locally exporting each tab as a CSV file.

### Converting to RDF

This uses `rdflib` to generate the RDF data from CSV. Namespaces are manually represented in the top of the document and are automatically handled in text as URI references. Serialisations to be produced are registered in `RDF_SERIALIZATIONS` variable - see `vocab_management.py` file for config variables regarding import, export, namespaces, metadata, etc.

The way the RDF generation works is as follows:

. In `vocab_management.py`, the CSV file path is associated with a _schema_ in the `CSVFILES` variable. For example, _classes_, _properties_, and _taxonomy_ are schemas commonly used for most CSVs. 
. The schema is a reference to a dict in `vocab_schemas.py` where each CSV column is mapped to a function in `vocab_funcs.py`. 
. The generator in `300` script takes each row, and calls the appropriate function by passing the specific cell and the entire row as values (along with others stuff like currently used namespace). 
. The function returns a list of triples which are added to the current graph being generated.
. In addition to the above, the generator `300` script also deals with modules and extensions by using the metadata/config variables in `vocab_management.py`.
. The generator `300` script outputs the RDF files using RDFS+SKOS serialisation, then converts them to OWL using SPARQL CONSTRUCT queries. In addition, it can also add in custom OWL-only triples at this stage.

### Generating HTML documentation

The `./300_generate_HTML.py` script is used to produce the HTML documentation for all DPV modules and extensions. This uses `jinja2` to render the HTML file from a template. The RDF data is loaded for each vocabulary and its modules for all RDF filepaths as defined in `vocab_management.py`. The data is stored in-memory as a giant dictionary so that lookups can be performed across extensions (e.g. to get the label of a parent concept from another vocabulary). See `vocab_management.py` file for export paths and the configuration of each template assigned to a vocabulary or module.

This script also produces the guides HTML files. By default, it will do this automatically after producing all the RDF documentation. To only produce the guides, use the `--guides` flag.

### Testing using SHACL

In between steps 2 (generate RDF) and 3 (generate HTML), there can be a series of tests done to ensure the RDF is generated correctly. For this, some basic SHACL constraints are defined in `shacl_shapes`.

The folder `shacl_shapes` holds the constraints in `shapes.ttl` to verify the vocabulary terms contain some basic annotations. The script `verify.py` executes the SHACL validator (currently hardcoded to use the [TopBraid SHACL](https://github.com/TopQuadrant/shacl) binary as `shaclvalidate.sh`), retrieves the results, runs a SPARQL query on them to get the failing nodes and messages.

The script uses `DATA_PATHS` to declare what data files should be validated. Currently, it will only validate `Turtle (.ttl)` files for simplicity as all files are duplicate serialisations of each other. The variable `SHAPES` declares the list of shape files to use. For each folder in `DATA_PATHS`, the script will execute the SHACL binary to check constraints defined in each of the `SHAPES` files.

To execute the tests, and to use the TopBraid SHACL binary, download the latest release from [maven](https://repo1.maven.org/maven2/org/topbraid/shacl/), extract it somewhere and note the path of the folder. Export `SHACLROOT` in the shell the script is going to run in (or e.g. save it in the bash profile) to the path of the folder. To be more precise, `$SHACLROOT/shaclvalidate.sh` should result in the binary being executed. 

The output of the script lists the data and shapes files being used in the validation process, the number of errors found, and a list of data nodes and the corresponding failure message.

### Spellcheck

The spell check is run for HTML documents by using [aspell](http://aspell.net/)
or a similar tool, with the dictionary containing words used in documents
provided as `./dictionary-aspell-en.pws`. If using `aspell`, the command is:

```bash
aspell -d en_GB --extra-dicts=./dictionary-aspell-en.pws -c <file>
```

If not using `aspell`, the file above is a simple text file with one word
per limit - which can be added or linked to whatever spell check is being
used.

For spell check in RDF / source, currently this is best done in the source
tool e.g. Google Sheets has a spell check option which should be used to
check for english valid terms. Running `aspell` on a CSV can be cumbersome
and difficult to complete as there are a large number of files to process.
Another reason to prefer the source tool is that if the CSV are modified,
the changes will still need to be synced back to the GSheets.

## FAQ

1. Fixing an error in the vocabulary terms i.e. term label, property, annotation --> Make the changes in the Google Sheet, and run the `100` script to download CSV, then `200` to produce RDF, then `300` to produce HTML.
2. Fixing an error in serialisation e.g. rdf:Property is defined as rdfs:Propety --> Make the changes in the `200` script for generating RDF, and `300` script to generate HTML
3. Changing content in HTML documentation e.g. change motivation paragraph --> Make the changes in the relevant `template` and `300` script to generate HTML
