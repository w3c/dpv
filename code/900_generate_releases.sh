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

VERSION="2.0"

cd ../$VERSION

# Create ReSpec exported outputs for representing published documents
# assuming respec is installed ; if not:
# npm install --global respec
# find $VERSION -type f -name *.html -exec respec --src {} --out {} \;

# Create zip of release 
mkdir -p ../releases
zip -q ../releases/dpv-$VERSION.zip -r *

cd ../code

echo "generated releases/dpv-$VERSION.zip"
# END
