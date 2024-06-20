#!/usr/bin/env bash
#author: Harshvardhan J. Pandit

# Generate DPV Releases
# Creates Zips or 'packages' for creating a new release
# Zips are stored in `repo-base/releases` which is gitignored

# Creates the following zips:
# dpv.zip - DPV + Extensions as RDFS+SKOS vocabulary

# zip
# -db display bytes
# -dc display counts
# -dg display global dots
# -r input files recursively
# -O output file
# unzip -l file to view list of files

VERSION="v2.0"
# TODO: create 2 zips - for v1 and v2
# TODO: add README to each v1 and v2 explaining the folder structure and the files contained in it

cd ..
mkdir -p releases

# 1. dpv.zip - DPV + Extensions as SKOS vocabulary
zip -q releases/dpv.zip -r $VERSION/dpv $VERSION/ai $VERSION/justifications $VERSION/legal $VERSION/loc $VERSION/pd $VERSION/risk $VERSION/tech
echo "generated releases/dpv.zip"
