#!/usr/bin/env python3

# SPDX-FileContributor: Arthit Suriyawongkul
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: W3C-20150513

"""
Find terms without an example
"""

import argparse
import os
import re
from collections import Counter
from typing import Iterator

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

DEFAULT_VOCAB_DIR = "../2.2"
DEFAULT_EXAMPLES_DIR = "../examples"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Find terms without an example")
    parser.add_argument(
        "--vocab-dir",
        default=DEFAULT_VOCAB_DIR,
        help="Directory containing vocabulary TTL files",
    )
    parser.add_argument(
        "--examples-dir",
        default=DEFAULT_EXAMPLES_DIR,
        help="Directory containing example TTL files",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    return parser.parse_args()


def get_ttl_files(root: str) -> Iterator[str]:
    """Yield all TTL files in the given directory and its subdirectories"""
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


def collect_used_terms(files: list[str]) -> set[str]:
    """
    Collect terms used in TTL files

    Since TTLs in examples directory does not have namespaces defined,
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
) -> bool:
    """Check if a term is used or any of its parents is used."""
    if term in used_terms:
        return True

    for parent in parents.get(term, set()):
        if parent in used_terms:
            return True

    return False


def count_per_namespace(terms: set[str]) -> Counter[str]:
    """Count terms per namespace"""
    ns_counter: Counter[str] = Counter()
    for item in terms:
        if ":" in item:
            ns = item.split(":")[0]
            ns_counter[ns] += 1
    return ns_counter


def count_parents(terms: set[str], parents: dict[str, set[str]]) -> Counter[str]:
    """Count parents of terms"""
    counter: Counter[str] = Counter()
    for term in terms:
        for parent in parents.get(term, []):
            counter[parent] += 1
    return counter


def print_terms_without_examples(
    terms: set[str], parents: dict[str, set[str]], label: str = "Terms"
) -> None:
    """Print terms without examples with their parent info."""
    print(f"\n==== {label} without examples ====\n")
    for term in sorted(terms):
        parent = parents.get(term)
        if parent:
            print(f"{term:<40} ⊂ {', '.join(parent)}")
        else:
            print(term)


def print_summary(
    classes: set[str],
    properties: set[str],
    used_classes: set[str],
    used_properties: set[str],
    print_complete_ns: bool = False,
) -> None:
    """Print per-namespace summary of classes and properties with examples.

    If print_complete_ns is False,
    do not print namespaces where all classes and properties have examples.
    """
    classes_ns_count = count_per_namespace(classes)
    properties_ns_count = count_per_namespace(properties)
    used_classes_ns_count = count_per_namespace(used_classes)
    used_properties_ns_count = count_per_namespace(used_properties)

    print()
    print("Namespace                  Class w/ Examples Prop. w/ Examples")
    print("-------------------------- ----------------- -----------------")
    for ns in sorted(set(classes_ns_count) | set(properties_ns_count)):
        if ns in SKIP_PREFIXES:
            continue
        c_used = used_classes_ns_count.get(ns, 0)
        c_total = classes_ns_count.get(ns, 0)
        p_used = used_properties_ns_count.get(ns, 0)
        p_total = properties_ns_count.get(ns, 0)
        if not print_complete_ns and c_used == c_total and p_used == p_total:
            continue
        print(f"{ns:<26} {c_used:>7} / {c_total:<7} {p_used:>7} / {p_total:<7}")


def main() -> None:
    """Main function"""
    args = parse_args()
    vocab_dir = args.vocab_dir
    examples_dir = args.examples_dir
    verbose = args.verbose

    vocab_files = list(get_ttl_files(vocab_dir))
    ex_files = list(get_ttl_files(examples_dir))
    if verbose:
        print(f"Vocabulary directory: {vocab_dir}")
        print(f"Example directory: {examples_dir}")
        print(f"Vocabulary TTL files found: {len(vocab_files)}")
        print(f"Example TTL files found: {len(ex_files)}")

    classes, properties, parents = collect_terms(vocab_files)
    if verbose:
        print(f"Classes defined: {len(classes)}")
        print(f"Properties defined: {len(properties)}")

    used = collect_used_terms(ex_files)
    used_classes = {c for c in classes if is_used_or_parent_used(c, used, parents)}
    used_properties = {
        p for p in properties if is_used_or_parent_used(p, used, parents)
    }
    unused_classes = classes - used_classes
    unused_properties = properties - used_properties
    if verbose:
        print(f"Classes with examples: {len(used_classes)} / {len(classes)}")
        print(f"Properties with examples: {len(used_properties)} / {len(properties)}")
        print_terms_without_examples(unused_classes, parents, "Classes")
        print_terms_without_examples(unused_properties, parents, "Properties")

    print_summary(
        classes,
        properties,
        used_classes,
        used_properties,
        print_complete_ns=verbose,
    )

    unused_classes_no_loc = {c for c in unused_classes if not c.startswith("loc:")}
    top_classes_parents = count_parents(unused_classes_no_loc, parents).most_common(10)
    top_properties_parents = count_parents(unused_properties, parents).most_common(10)

    print("\nTop parents among classes without examples (excluding 'loc:'):")
    for parent, count in top_classes_parents:
        print(f"{count:>7}  {parent}")
    print("\nTop parents among properties without examples:")
    for parent, count in top_properties_parents:
        print(f"{count:>7}  {parent}")

if __name__ == "__main__":
    main()
