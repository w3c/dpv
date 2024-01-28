#!/usr/bin/env bash
#author: Harshvardhan J. Pandit

# This script will open all DPV HTML documents in the browser
# for a visual inspection of contents.
# It can open the live versions; OR
# The script assumes there's a server running on localhost:8000
# from the root directory (if not, change the localhost)
# The easiest way to do this is using python3 -m http.server

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
	COMMAND=xdg-open
elif [[ "$OSTYPE" == "darwin"* ]]; then
	COMMAND=open
fi

## Choose Mode for live or local version
# MODE="https://w3id.org/dpv"
MODE="http://localhost:8000"

FILES=(
	# core specs
	"$MODE/dpv"
	"$MODE/dpv-gdpr"
	"$MODE/dpv-pd"
	"$MODE/dpv-legal"
	"$MODE/dpv-tech"
	"$MODE/risk"
	"$MODE/rights"
	"$MODE/rights/eu"
	# dpv-skos
	"$MODE/dpv-skos/"
	"$MODE/dpv-skos/dpv-gdpr"
	"$MODE/dpv-skos/dpv-pd"
	"$MODE/dpv-skos/dpv-legal"
	"$MODE/dpv-skos/dpv-tech"
	"$MODE/dpv-skos/risk"
	"$MODE/dpv-skos/rights"
	"$MODE/dpv-skos/rights/eu"
	# dpv-owl
	"$MODE/dpv-owl"
	"$MODE/dpv-owl/dpv-gdpr"
	"$MODE/dpv-owl/dpv-pd"
	"$MODE/dpv-owl/dpv-legal"
	"$MODE/dpv-owl/dpv-tech"
	"$MODE/dpv-owl/risk"
	"$MODE/dpv-owl/rights"
	"$MODE/dpv-owl/rights/eu"
	# misc
	"$MODE/primer"
	"$MODE/use-cases"
	"$MODE/examples"
	"$MODE/guides"
	"$MODE/guides/dpv-owl.html"
	)

for i in "${!FILES[@]}"
do
	$COMMAND ${FILES[i]}
done