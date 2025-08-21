#!/usr/bin/env python3

# SPDX-FileContributor: Arthit Suriyawongkul
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: W3C-20150513

"""
Find defined terms without an example and terms used in examples but not defined.
"""

import argparse
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
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
    "odrl",
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
    parser.add_argument("-v", "--verbose", action="store_true", help="Print everything")
    parser.add_argument(
        "-l",
        "--list-unused-terms",
        action="store_true",
        help="Print terms without examples",
    )
    parser.add_argument(
        "-t",
        "--top-unused-parents",
        action="store_true",
        help="Print top parents of terms without examples",
    )
    parser.add_argument(
        "-c",
        "--count-used-terms",
        action="store_true",
        help="Print term counts and example counts per namespace",
    )
    parser.add_argument(
        "-u",
        "--list-undefined-terms",
        action="store_true",
        help="Print terms used in examples but not defined in vocabulary files",
    )
    return parser.parse_args()


def get_ttl_files(root: str) -> Iterator[str]:
    """Yield .ttl files, excluding files ending with '-owl.ttl'"""
    base = Path(root)
    if not base.exists():
        return
    for p in base.rglob("*.ttl"):
        name = p.name.lower()
        if not name.endswith("-owl.ttl"):
            yield str(p)


def collect_terms_in_vocabs(
    files: list[str],
) -> tuple[set[str], set[str], dict[str, set[str]], Counter[str], Counter[str]]:
    """Collect terms defined in vocabulary files"""
    classes: set[str] = set()
    properties: set[str] = set()
    parents: dict[str, set[str]] = {}
    classes_ns_count: Counter[str] = Counter()
    properties_ns_count: Counter[str] = Counter()

    for f in files:
        g = Graph()
        g.parse(f, format="turtle")
        for s in g.subjects(RDF.type, RDFS.Class):
            name = g.qname(str(s))
            ns, sep, _ = name.partition(":")
            if ns in SKIP_PREFIXES:
                continue
            if name not in classes:
                classes.add(name)
                if sep:
                    classes_ns_count[ns] += 1
            for o in g.objects(s, RDFS.subClassOf):
                parents.setdefault(name, set()).add(g.qname(str(o)))
            for o in g.objects(s, SKOS.broader):
                parents.setdefault(name, set()).add(g.qname(str(o)))
        for s in g.subjects(RDF.type, RDF.Property):
            name = g.qname(str(s))
            ns, sep, _ = name.partition(":")
            if ns in SKIP_PREFIXES:
                continue
            if name not in properties:
                properties.add(name)
                if sep:
                    properties_ns_count[ns] += 1
            for o in g.objects(s, RDFS.subPropertyOf):
                parents.setdefault(name, set()).add(g.qname(str(o)))
            for o in g.objects(s, SKOS.broader):
                parents.setdefault(name, set()).add(g.qname(str(o)))

    return classes, properties, parents, classes_ns_count, properties_ns_count


def collect_terms_in_examples(files: list[str]) -> dict[str, set[str]]:
    """
    Collect terms used in example files

    Since TTLs in examples directory does not have namespaces defined,
    we cannot use RDFLib to parse them.
    Instead, we use regex to find terms.
    """
    used: dict[str, set[str]] = defaultdict(set)
    pattern = re.compile(r"\b([a-zA-Z0-9_-]+):([a-zA-Z0-9_-]+)\b")
    # Match terms (prefix:term) not surrounded by quotes (since it can be literal)
    # pattern = re.compile(r'(?<!["\'])\b([a-zA-Z0-9_-]+:[a-zA-Z0-9_-]+)\b(?!["\'])')
    for f in files:
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                for match in pattern.finditer(line):
                    term = match.group(0)
                    prefix = match.group(1)
                    if prefix not in SKIP_PREFIXES:
                        used[term].add(f)
    return used


def is_used_or_parent_used(
    term: str, used_keys: set[str], parents: dict[str, set[str]]
) -> bool:
    """Check if a term is used or any of its parents is used."""
    if term in used_keys:
        return True
    return bool(parents.get(term, set()) & used_keys)


def count_parents(terms: set[str], parents: dict[str, set[str]]) -> Counter[str]:
    """Count parents of terms"""
    counter: Counter[str] = Counter()
    for term in terms:
        for parent in parents.get(term, set()):
            counter[parent] += 1
    return counter


def print_terms_without_examples(
    terms: set[str], parents: dict[str, set[str]], label: str = "Terms"
) -> None:
    """Print terms without examples with their parent info."""
    print(f"\n{label} without examples")
    print("-------------------------------")
    if len(terms) == 0:
        print("Not found.")
        return

    for term in sorted(terms):
        parent = parents.get(term)
        if parent:
            print(f"{term:<40} ⊂ {', '.join(parent)}")
        else:
            print(term)


def print_terms_used_but_undefined(
    used_terms: dict[str, set[str]],
    classes: set[str],
    properties: set[str],
    examples_dir: str,
) -> None:
    """
    Print terms that appear in example files but are not defined in the vocabulary files.
    """
    defined = classes | properties
    undefined = sorted(
        term
        for term in used_terms.keys()
        if ":" in term
        and term.split(":", 1)[0] not in SKIP_PREFIXES
        and term not in defined
    )

    if not undefined:
        print("\nNo undefined terms found in examples (all used terms are defined).")
        return

    print("\nTerms used in examples but NOT defined in vocabulary files")
    print("----------------------------------------------------------")
    for term in undefined:
        files = used_terms.get(term, ())
        rel_files = [
            (os.path.relpath(f, start=examples_dir) if examples_dir else f)
            for f in sorted(files)
        ]
        print(f"{term:<40} in: {", ".join(rel_files)}")


def print_summary_terms_with_examples(
    classes_ns_count: Counter[str],
    properties_ns_count: Counter[str],
    used_classes_ns_count: Counter[str],
    used_properties_ns_count: Counter[str],
    print_complete_ns: bool = False,
) -> None:
    """Print per-namespace summary of classes and properties with examples.

    If print_complete_ns is False,
    do not print namespaces where all classes and properties have examples.
    """
    print()
    print("Namespace                  Class w/ Examples Prop. w/ Examples")
    print("-------------------------- ----------------- -----------------")
    for ns in sorted(classes_ns_count.keys() | properties_ns_count.keys()):
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

    vocab_files = list(get_ttl_files(vocab_dir))
    ex_files = list(get_ttl_files(examples_dir))
    if args.verbose:
        print(f"Vocabulary directory: {vocab_dir}")
        print(f"Example directory: {examples_dir}")
        print(f"Vocabulary TTL files found: {len(vocab_files)}")
        print(f"Example TTL files found: {len(ex_files)}")

    classes, properties, parents, classes_ns_count, properties_ns_count = (
        collect_terms_in_vocabs(vocab_files)
    )

    used = collect_terms_in_examples(ex_files)
    used_keys = set(used)  # cache keys for faster lookup

    used_classes: set[str] = set()
    used_properties: set[str] = set()
    used_classes_ns_count: Counter[str] = Counter()
    used_properties_ns_count: Counter[str] = Counter()

    for c in classes:
        if is_used_or_parent_used(c, used_keys, parents):
            used_classes.add(c)
            ns, sep, _ = c.partition(":")
            if sep:
                used_classes_ns_count[ns] += 1

    for p in properties:
        if is_used_or_parent_used(p, used_keys, parents):
            used_properties.add(p)
            ns, sep, _ = p.partition(":")
            if sep:
                used_properties_ns_count[ns] += 1

    print(f"Classes (inc. parents) with examples: {len(used_classes)} / {len(classes)}")
    print(
        f"Properties (inc. parents) with examples: {len(used_properties)} / {len(properties)}"
    )

    unused_classes = classes - used_classes
    unused_properties = properties - used_properties

    if args.list_unused_terms or args.verbose:
        print_terms_without_examples(unused_classes, parents, "Classes")
        print_terms_without_examples(unused_properties, parents, "Properties")

    print_summary_terms_with_examples(
        classes_ns_count,
        properties_ns_count,
        used_classes_ns_count,
        used_properties_ns_count,
        print_complete_ns=args.verbose,
    )

    if args.top_unused_parents or args.verbose:
        unused_classes_no_loc = {c for c in unused_classes if not c.startswith("loc:")}
        top_classes_parents = count_parents(unused_classes_no_loc, parents).most_common(
            10
        )
        top_properties_parents = count_parents(unused_properties, parents).most_common(
            10
        )
        print("\nTop parents among classes without examples (excluding 'loc:')")
        print("-------------------------------------------------------------")
        for parent, count in top_classes_parents:
            print(f"{count:>7}  {parent}")
        print("\nTop parents among properties without examples")
        print("---------------------------------------------")
        for parent, count in top_properties_parents:
            print(f"{count:>7}  {parent}")

    if args.list_undefined_terms or args.verbose:
        print_terms_used_but_undefined(used, classes, properties, examples_dir)


if __name__ == "__main__":
    main()
