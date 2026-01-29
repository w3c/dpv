#!/usr/bin/env bash

# Check if argument is provided
if [ -z "$1" ]; then
  echo "Usage: '$0 <YY-MM-DD>' to generate minutes from 'meeting-20<year>-<month>-<date>.irc'"
  exit 1
fi

time="$1"
file="meeting-20${time}"

# check if file exists
if [ ! -f ./data/${file}.irc ]; then
    echo "file ${file}.irc not found"
    exit -1
fi

# Replace with the desired command
perl scribe.perl -implicitContinuations -final -emphasis ./data/${file}.irc > ../../meetings/${file}.html
echo "Generated ../../meetings/${file}.html"
