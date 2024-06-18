#!/usr/bin/env bash
#author: Harshvardhan J. Pandit

# Generate DPV Releases
# Creates Zips or 'packages' for creating a new release
# Zips are stored in `repo-base/releases` which is gitignored

# Creates the following zips:
# 1. dpv.zip - DPV + Extensions as SKOS vocabulary
# 2. dpv-skos.zip - DPV + Extensions as RDFS+SKOS ontology
# 3. dpv-owl.zip - DPV + Extensions as OWL ontology
# 4. dpv-csv.zip - DPV + Extensions as CSV files
# 5. dpv-json.zip - DPV + Extensions as JSON files
# 6. dpv-nace.zip - DPV NACE vocabulary
# 7. dpv-examples.zip - Collected examples of using DPV
# 8. dpv-guides.zip - Collected guides and tutorials on using DPV

# zip
# -db display bytes
# -dc display counts
# -dg display global dots
# -r input files recursively
# -O output file

cd ..
mkdir -p releases

# 1. dpv.zip - DPV + Extensions as SKOS vocabulary
zip -q releases/dpv.zip -r dpv dpv-gdpr dpv-pd dpv-legal dpv-tech risk rights
echo "generated releases/dpv.zip"

# 2. dpv-skos.zip - DPV + Extensions as RDFS+SKOS ontology
zip -q releases/dpv-skos.zip -r dpv-skos
echo "generated releases/dpv-skos.zip"

# 3. dpv-owl.zip - DPV + Extensions as OWL ontology
zip -q releases/dpv-owl.zip -r dpv-owl
echo "generated releases/dpv-owl.zip"

# 4. dpv-csv.zip - DPV + Extensions as CSV files
zip -q releases/dpv-xlsx.zip documentation-generator/vocab_csv/*.xlsx
echo "generated releases/dpv-xlsx.zip"

# 5. dpv-json.zip - DPV + Extensions as JSON files
# TODO

# 6. dpv-nace.zip - DPV NACE vocabulary
zip -q releases/dpv-nace.zip -r dpv-nace
echo "generated releases/dpv-nace.zip"

# 7. dpv-examples.zip - Collected examples of using DPV
# EMPTY FOLDERS
# zip -q releases/dpv-examples.zip -r dpv-examples
# echo "generated releases/dpv-examples.zip"

# 8. dpv-guides.zip - Collected guides and tutorials on using DPV
# EMPTY FOLDERS
# zip -q releases/dpv-guides.zip -r dpv-guides
# echo "generated releases/dpv-guides.zip"