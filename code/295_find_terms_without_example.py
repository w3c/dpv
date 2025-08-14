#!/usr/bin/env python3

# SPDX-FileContributor: Arthit Suriyawongkul
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: W3C-20150513

"""
Find terms without an example
"""

import os
import re
import sys
from collections import Counter

from rdflib import RDF, RDFS, SKOS, Graph

# Assuming consistent prefixes in vocabulary files
SKIP_PREFIXES = {
    "ex",  # Example namespace
    "_",  # Blank nodes
    "bibo",
    "dcat",
    "dct",
    "foaf",
    "org",
    "owl",
    "profile",
    "rdf",
    "rdfs",
    "role",
    "schema",
    "scoro",
    "skos",
    "sw",
    "time",
    "vann",
    "xsd",
}


vocab_dir = "../2.2"
examples_dir = "../examples"

verbose = "--verbose" in sys.argv or "-v" in sys.argv


def get_ttl_files(root: str):
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".ttl"):
                yield os.path.join(dirpath, f)


def collect_terms(files: list[str]) -> tuple[set[str], set[str], dict[str, set[str]]]:
    """Collect terms defined in vocabulary files"""
    classes: set[str] = set()
    properties: set[str] = set()
    parents: dict[str, set[str]] = {}
    for f in files:
        g = Graph()
        g.parse(f, format="turtle")
        for s in g.subjects(RDF.type, RDFS.Class):
            name = g.qname(s)
            if name.split(":")[0] in SKIP_PREFIXES:
                continue
            classes.add(name)
            for o in g.objects(s, RDFS.subClassOf):
                parents.setdefault(name, set()).add(g.qname(o))
            for o in g.objects(s, SKOS.broader):
                parents.setdefault(name, set()).add(g.qname(o))
        for s in g.subjects(RDF.type, RDF.Property):
            name = g.qname(s)
            if name.split(":")[0] in SKIP_PREFIXES:
                continue
            properties.add(name)
            for o in g.objects(s, RDFS.subPropertyOf):
                parents.setdefault(name, set()).add(g.qname(o))
            for o in g.objects(s, SKOS.broader):
                parents.setdefault(name, set()).add(g.qname(o))

    return classes, properties, parents


def collect_used_terms(files: list[str]):
    """
    Collect terms used in TTL files

    Since TTLs in examples directory is not in full Turtle format,
    we cannot use RDFLib to parse them.
    Instead, we use regex to find terms.
    """
    used: set[str] = set()
    pattern = re.compile(r"\b([a-zA-Z0-9_-]+:[a-zA-Z0-9_-]+)\b")
    for f in files:
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                for match in pattern.findall(line):
                    prefix = match.split(":")[0]
                    if prefix not in SKIP_PREFIXES:
                        used.add(match)
    return used


def is_used_or_parent_used(
    term: str, used_terms: set[str], parents: dict[str, set[str]]
):
    """Check if a term is used or any of its parents is used."""
    if term in used_terms:
        return True

    for parent in parents.get(term, set()):
        if parent in used_terms:
            return True

    return False


def count_per_namespace(terms: set[str]) -> dict[str, int]:
    """Count terms per namespace"""
    ns_counter: dict[str, int] = Counter()
    for item in terms:
        if ":" in item:
            ns = item.split(":")[0]
            ns_counter[ns] += 1
    return ns_counter


def main():
    vocab_files = list(get_ttl_files(vocab_dir))
    ex_files = list(get_ttl_files(examples_dir))
    if verbose:
        print(f"Vocabulary directory: {vocab_dir}")
        print(f"Example directory: {examples_dir}")
        print(f"Vocabulary TTL files found: {len(vocab_files)}")
        print(f"Example TTL files found: {len(ex_files)}")

    classes, properties, parents = collect_terms(vocab_files)
    if verbose:
        print(f"Classes defined in vocabulary files: {len(classes)}")
        print(f"Properties defined in vocabulary files: {len(properties)}")

    used = collect_used_terms(ex_files)
    used_classes = {c for c in classes if is_used_or_parent_used(c, used, parents)}
    used_properties = {
        p for p in properties if is_used_or_parent_used(p, used, parents)
    }
    if verbose:
        print(f"Classes with examples: {len(used_classes)} / {len(classes)}")
        print(f"Properties with examples: {len(used_properties)} / {len(properties)}")

    # Print all terms without examples
    if verbose:
        unused_classes = sorted(classes - set(used_classes))
        unused_properties = sorted(properties - set(used_properties))
        print("\n==== Classes without examples ====\n")
        for c in unused_classes:
            parent = parents.get(c)
            if parent:
                print(f"{c}  (broader/subClassOf {', '.join(parent)})")
            else:
                print(c)
        print("\n==== Properties without examples ====\n")
        for p in unused_properties:
            parent = parents.get(p)
            if parent:
                print(f"{p}  (broader/subPropertyOf {', '.join(parent)})")
            else:
                print(p)

    all_classes_ns = count_per_namespace(classes)
    all_properties_ns = count_per_namespace(properties)
    used_classes_ns = count_per_namespace(used_classes)
    used_properties_ns = count_per_namespace(used_properties)

    print()
    print("Namespace              Class w/ Examples Prop. w/ Examples")
    print("---------------------- ----------------- -----------------")
    for ns in sorted(set(all_classes_ns) | set(all_properties_ns)):
        if ns in SKIP_PREFIXES:
            continue
        c_used = used_classes_ns.get(ns, 0)
        c_total = all_classes_ns.get(ns, 0)
        p_used = used_properties_ns.get(ns, 0)
        p_total = all_properties_ns.get(ns, 0)
        if not verbose and c_used == c_total and p_used == p_total:
            continue
        print(f"{ns:<22} {c_used:>7} / {c_total:<7} {p_used:>7} / {p_total:<7}")


if __name__ == "__main__":
    main()
