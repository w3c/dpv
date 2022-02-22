#!/usr/bin/env python3

import csv
from collections import namedtuple
import os

CSV_FILEPATH = './vocab_csv'

(_, _, CSVS) = next(os.walk(CSV_FILEPATH))
CSVS.sort()


for module in CSVS:
    output = []
    with open(f'{CSV_FILEPATH}/{module}', 'r') as fd:
        csvreader = csv.reader(fd)
        schema_labels = [col.replace('-','_') for col in next(csvreader) if col]
        SCHEMA = namedtuple('SCHEMA', schema_labels)
        for row in csvreader:
            row = row[:len(schema_labels)]
            item = SCHEMA(*row)
            if item.Status not in ("proposed", "changed", "modified"): continue
            if item.Status == "proposed":
                output.append(item.Term)
            else:
                output.append(f'{item.Term} (changed)')
            if 'properties' in module:
                if item.ParentProperty:
                    output.append(f'\tparent: {item.ParentProperty}')
            else:
                if item.ParentTerm:
                    output.append(f'\tparent: {item.ParentTerm}')
            if item.Contributors:
                output.append(f'\tcontributor: {item.Contributors}')
    if output:
        print(f'\n--- {module[:-4]} ---\n')
        for line in output: 
            print(line)
