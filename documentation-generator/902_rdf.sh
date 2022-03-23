#!/usr/bin/env bash
#author: Harshvardhan J. Pandit

#execute DPV RDF generation scripts

# Step2: generate RDF
./002_parse_csv_to_rdf.py
./002_parse_csv_to_rdf_skos.py
./002_parse_csv_to_rdf_owl.py

