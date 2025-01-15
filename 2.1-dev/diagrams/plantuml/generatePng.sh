#!/usr/bin/env bash

# you need wget and java on your $PATH

PLANTUML_JAR_PATH=/tmp/plantuml.jar
PLANTUML_URL="https://github.com/plantuml/plantuml/releases/download/v1.2024.5/plantuml-1.2024.5.jar"

EXCLUDES=("dpv.plantuml" "style.plantuml")

if [ ! -f $PLANTUML_JAR_PATH ]; then
    echo "Downloading plantuml.jar to $PLANTUML_JAR_PATH"
    wget $PLANTUML_URL -O $PLANTUML_JAR_PATH
fi

for i in `ls -1 *.plantuml`
do
    if [[ ${EXCLUDES[@]} =~ $i ]]
    then
	echo "skip $i"
    else
	echo "render $i"
	java -jar $PLANTUML_JAR_PATH -headless -tsvg -o .. "$i"
    fi
done
