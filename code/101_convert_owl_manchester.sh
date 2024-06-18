#!/usr/bin/env bash
#author: Harshvardhan J. Pandit

# Convert DPV files from RDF / Turtle format to OWL / Machester formats

echo "Converting DPV files from .rdf to .owl with ManchesterSyntax"

# REQUIREMENTS: Ont-Converter
# Get it from here https://github.com/sszuev/ont-converter/releases
# Put the jar as "ont-converter.jar" in this same folder

# convert .rdf files to .owl files in manchester syntax
convert_owl() {
    filepath="${1%.*}"
    filepath_owl="${filepath}.owl"
    echo -n "converting $filepath ..."
    java -jar ont-converter.jar -f -i "$1" -if RDF_XML -o "$filepath_owl" -of ManchesterSyntax
    echo "DONE"
}
export -f convert_owl

# Find all .rdf files in parent directory,
#   then convert them to .owl using the ont-converter.
# The assumption here is that .rdf files are only present in places
#   where DPV outputs exist, and won't be for example in the
#   documentation generator metadata folders (they are .ttl)

find ../dpv-owl -type f -name "*.rdf" -exec bash -c 'convert_owl "$0"' {} \;
# java -jar $ONT_CONVERTER