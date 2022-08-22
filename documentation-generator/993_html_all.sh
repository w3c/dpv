#!/usr/bin/env bash
#author: Harshvardhan J. Pandit

#execute DPV HTML generation scripts

CHECK_ERROR() {
    retval=$?
    if [ $retval -ne 0 ]; then
        echo "Error"
        echo $retval
        exit 1;
    fi
}

# Step3: generate HTML
./003_generate_respec_html.py
CHECK_ERROR
./003_generate_respec_html_skos.py
CHECK_ERROR
./003_generate_respec_html_owl.py
CHECK_ERROR
./004_generate_guides.py
CHECK_ERROR
./005_generate_examples.py
CHECK_ERROR
./006_generate_primer.py
CHECK_ERROR