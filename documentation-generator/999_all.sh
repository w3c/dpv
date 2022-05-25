#!/usr/bin/env bash
#author: Harshvardhan J. Pandit

#execute all DPV generation scripts

CHECK_ERROR() {
    retval=$?
    if [ $retval -ne 0 ]; then
        echo "Error"
        echo $retval
        exit 1;
    fi
}

# Step1: download files
# ./001_download_vocab_in_csv.py
echo "Step1: download files ...SKIPPED"

# Step2: generate RDF
echo -n "Step2: generate RDF files ..."
./902_rdf.sh > logs/902.txt 2>&1
CHECK_ERROR
echo "DONE"

# Step2.5: validate using SHACL
echo -n "Step2.5: validate using SHACL ..."
./verify_002.py > logs/validation_report.txt 2>&1
CHECK_ERROR
echo "DONE"

# Step3: generate HTML
echo -n "Step3: generate HTML ..."
./903_html.sh > logs/903.txt 2>&1
CHECK_ERROR
echo "DONE"

# Step4: generate changelog
echo -n "Step4: generate changelog ..."
./changelog.py > logs/changelog.txt 2>&1
CHECK_ERROR
echo "DONE"