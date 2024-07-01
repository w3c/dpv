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
# MODE="http://localhost:8000"
MODE="https://dev.dpvcg.org/2.0"
MODE="localhost:8000/2.0"

FILES=(
    # core specs
    "$MODE/dpv/index.html"
    # extensions
    "$MODE/pd/index.html"
    "$MODE/tech/index.html"
    "$MODE/risk/index.html"
    "$MODE/ai/index.html"
    "$MODE/justifications/index.html"
    "$MODE/loc/index.html"
    # legal
    "$MODE/legal/index.html"
    "$MODE/legal/eu/index.html"
    "$MODE/legal/eu/gdpr/index.html"
    "$MODE/legal/eu/dga/index.html"
    "$MODE/legal/eu/aiact/index.html"
    "$MODE/legal/eu/nis2/index.html"
    "$MODE/legal/eu/rights/index.html"
    "$MODE/legal/de/index.html"
    "$MODE/legal/gb/index.html"
    "$MODE/legal/ie/index.html"
    "$MODE/legal/in/index.html"
    "$MODE/legal/us/index.html"
    # misc
    "$MODE/../primer/index.html"
    "$MODE/../use-cases/index.html"
    "$MODE/examples/index.html"
    "$MODE/../guides/index.html"
    "$MODE/../guides/dpv-owl.html"
    "$MODE/../guides/consent-27560.html"
    "$MODE/../guides/gdpr-data-breach.html"
    "$MODE/../guides/gdpr-dpia.html"
    "$MODE/../guides/gdpr-ropa.html"
    "$MODE/../guides/notice-29184.html"
    "$MODE/../guides/rights.html"
    "$MODE/../guides/dpv-misc.html"
    "$MODE/../guides/dpv-odrl.html"
    "$MODE/../guides/dpv-skos.html"
    )

DPV_MODULES=(
    "$MODE/dpv/modules/context.html"
    "$MODE/dpv/modules/entities.html"
    "$MODE/dpv/modules/legal_basis.html"
    "$MODE/dpv/modules/personal_data.html"
    "$MODE/dpv/modules/processing.html"
    "$MODE/dpv/modules/purposes.html"
    "$MODE/dpv/modules/rights.html"
    "$MODE/dpv/modules/risk.html"
    "$MODE/dpv/modules/rules.html"
    "$MODE/dpv/modules/TOM.html"
    )

for i in "$@"; do
    case $i in
        -m)
            for i in "${!DPV_MODULES[@]}"
            do
                $COMMAND ${DPV_MODULES[i]}
            done
            exit 1
            ;;
    esac
done

for i in "${!FILES[@]}"
do
    xdg-open ${FILES[i]}
done