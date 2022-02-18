#!/usr/bin/env bash
#author: Harshvardhan J. Pandit

#execute all DPV generation scripts

# Step1: download files
# ./001_download_vocab_in_csv.py

# Step2: generate RDF
./002_parse_csv_to_rdf.py
./002_parse_csv_to_rdf_skos.py
./002_parse_csv_to_rdf_owl.py

# Step3: generate HTML
./003_generate_respec_html.py
./003_generate_respec_html_skos.py
./003_generate_respec_html_owl.py

