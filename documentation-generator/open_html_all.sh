#!/usr/bin/env bash
#author: Harshvardhan J. Pandit

# This script will open all DPV HTML documents in the browser
# for a visual inspection of contents.
# The script assumes there's a server running on localhost:8000
# from the root directory
# The easiest way to do this is using python3 -m http.server

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
	COMMAND=xdg-open
elif [[ "$OSTYPE" == "darwin"* ]]; then
	COMMAND=open
fi

FILES=(
	# core specs
	"http://localhost:8000/dpv"
	"http://localhost:8000/dpv-gdpr"
	"http://localhost:8000/dpv-pd"
	"http://localhost:8000/dpv-legal"
	"http://localhost:8000/dpv-tech"
	"http://localhost:8000/risk"
	"http://localhost:8000/rights"
	"http://localhost:8000/rights/eu"
	# dpv-skos
	"http://localhost:8000/dpv-skos/"
	"http://localhost:8000/dpv-skos/dpv-gdpr"
	"http://localhost:8000/dpv-skos/dpv-pd"
	"http://localhost:8000/dpv-skos/dpv-legal"
	"http://localhost:8000/dpv-skos/dpv-tech"
	"http://localhost:8000/dpv-skos/risk"
	"http://localhost:8000/dpv-skos/rights"
	"http://localhost:8000/dpv-skos/rights/eu"
	# dpv-owl
	"http://localhost:8000/dpv-owl"
	"http://localhost:8000/dpv-owl/dpv-gdpr"
	"http://localhost:8000/dpv-owl/dpv-pd"
	"http://localhost:8000/dpv-owl/dpv-legal"
	"http://localhost:8000/dpv-owl/dpv-tech"
	"http://localhost:8000/dpv-owl/risk"
	"http://localhost:8000/dpv-owl/rights"
	"http://localhost:8000/dpv-owl/rights/eu"
	# misc
	"http://localhost:8000/primer"
	"http://localhost:8000/use-cases"
	"http://localhost:8000/examples"
	"http://localhost:8000/guides"
	"http://localhost:8000/guides/dpv-owl.html"
	)

for i in "${!FILES[@]}"
do
	$COMMAND ${FILES[i]}
done