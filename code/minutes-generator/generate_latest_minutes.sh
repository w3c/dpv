#!/usr/bin/env bash

file="data/$(ls -1 data/ | tail -1)"
filename=$(basename -- "$file")
# extension="${filename##*.}"
filename="${filename%.*}"
perl scribe.perl -implicitContinuations -final -emphasis $file > ../../meetings/${filename}.html
