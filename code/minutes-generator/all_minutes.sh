#!/usr/bin/env bash

for file in data/*; do
    filename=$(basename -- "$file")
    # extension="${filename##*.}"
    filename="${filename%.*}"

    perl scribe.perl -implicitContinuations -final -emphasis $file > ../../meetings/${filename}.html
done
