#!/usr/bin/env bash
#author: Harshvardhan J. Pandit

#execute DPV RDF generation scripts

CHECK_ERROR() {
	retval=$?
	if [ $retval -ne 0 ]; then
	    echo "Error"
	    echo $retval
		exit 1;
	fi
}

# Step2: generate RDF
./002_parse_csv_to_rdf.py
CHECK_ERROR
./002_parse_csv_to_rdf_skos.py
CHECK_ERROR
./002_parse_csv_to_rdf_owl.py
CHECK_ERROR
