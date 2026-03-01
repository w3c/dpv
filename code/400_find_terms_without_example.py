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
    "ex",  # Example namespaces
    "exA",
    "exB",
    "exC",
    "exD",
    "exE",
    "exF",
    "exG",
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

DEFAULT_VOCAB_DIR = "../2.3"
DEFAULT_EXAMPLES_DIR = "../examples"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Find terms without an example")
    parser.add_argument(
        "-d",
        "--vocab-dir",
        default=DEFAULT_VOCAB_DIR,
        help="Directory containing vocabulary TTL files",
    )
    parser.add_argument(
        "-e",
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
    parser.add_argument(
        "-x",
        "--list-undefined-html-terms",
        action="store_true",
        help="Print terms used in HTMLs but not defined in vocabulary files",
    )
    return parser.parse_args()


def get_ttl_files(root: str) -> Iterator[str]:
    """Yield .ttl files, excluding files ending with -owl.ttl"""
    base = Path(root)
    if not base.exists():
        return
    for p in base.rglob("*.ttl"):
        name = p.name.lower()
        if not name.endswith("-owl.ttl"):
            yield str(p)


def get_html_files(root: str) -> Iterator[str]:
    """Yield .html files, excluding files ending with -en.html"""
    base = Path(root)
    if not base.exists():
        return
    for p in base.rglob("*.html"):
        name = p.name.lower()
        if not name.endswith("-en.html"):
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
    pattern = re.compile(r"(?<![\"\'\:])\b([a-zA-Z0-9_\-]+):([a-zA-Z0-9_\-]+)\b(?![\"\'\:])")  # prefix:term, do not match if surrounded by quotes or colons 
    for f in files:
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                for match in pattern.finditer(line):
                    term = match.group(0)  # full term (prefix:term)
                    prefix = match.group(1)
                    if prefix not in SKIP_PREFIXES:
                        used[term].add(f)
    return used


def collect_terms_in_htmls(files: list[str]) -> dict[str, dict[str, set[int]]]:
    """Collect terms mentioned in description section of HTML files"""
    # { term: { filepath: set of line numbers } } }
    used: dict[str, dict[str, set[int]]] = defaultdict(lambda: defaultdict(set))

    # respecConfig.shortName
    global_prefix_pat = re.compile(
        r"respecConfig\s*=\s*{[\s\S]*?shortName\s*[:=]\s*['\"]([^'\"]+)['\"]",
        re.IGNORECASE,
    )
    # [=term=]
    term_bracket_pat = re.compile(r"\[=\s*?([a-zA-Z0-9_\-]+?)\s*?=\]")
    # <code>term</code> -- too many false positives but can be useful if you have time to comb through
    # term_code_pat = re.compile(r"<code>\s*?([a-zA-Z0-9_\-]+?)\s*?</code>")
    # <code>prefix:term</code>
    term_code_prefix_pat = re.compile(
        r"<code>\s*?([a-zA-Z0-9_\-]+?:[a-zA-Z0-9_\-]+?)\s*?</code>"
    )
    # `prefix:term`
    term_backtick_prefix_pat = re.compile(r"`([a-zA-Z0-9_\-]+?:[a-zA-Z0-9_\-]+?)`")

    for f in files:
        try:
            with open(f, encoding="utf-8", errors="ignore") as fh:
                html = fh.read()
        except OSError:
            continue

        match = global_prefix_pat.search(html)
        prefix = match.group(1).lower() if match else ""

        for n, line in enumerate(html.splitlines(), start=1):
            for m in term_bracket_pat.finditer(line):
                term = m.group(1)
                term = f"{prefix}:{term}" if prefix else term
                used[term][f].add(n)

            # for m in term_code_pat.finditer(line):
            #     term = m.group(1)
            #     term = f"{prefix}:{term}" if prefix else term
            #     used[term][f+"**"].add(n)

            for m in term_code_prefix_pat.finditer(line):
                term = m.group(1)  # full term (prefix:term)
                used[term][f].add(n)

            for m in term_backtick_prefix_pat.finditer(line):
                term = m.group(1)  # full term (prefix:term)
                used[term][f].add(n)

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
    print(f"\n{label} without examples ({len(terms)})")
    print("-------------------------------")

    if not terms:
        print("Not found.")
        return

    for term in sorted(terms):
        parent = parents.get(term)
        if parent:
            print(f"{term:<40} ⊂ {', '.join(parent)}")
        else:
            print(term)


def print_undefined_example_terms(
    used: dict[str, set[str]],
    classes: set[str],
    properties: set[str],
    base_dir: str,
) -> None:
    """
    Print terms that appear in example files but are not defined in the vocabulary files.
    """
    defined = classes | properties
    undefined = sorted(
        term
        for term in used.keys()
        if ":" in term
        and term.split(":", 1)[0] not in SKIP_PREFIXES
        and term not in defined
    )

    print(
        f"\nTerms used in examples but NOT defined in vocabulary files ({len(undefined)})"
    )
    print("----------------------------------------------------------")

    if not undefined:
        print("Not found.")
        return

    for term in undefined:
        files = used.get(term, ())
        found_in = [
            (os.path.relpath(f, start=base_dir) if base_dir else f)
            for f in sorted(files)
        ]
        print(f"{term:<40} in: {', '.join(found_in)}")


def print_undefined_html_terms(
    used: dict[str, dict[str, set[int]]],
    classes: set[str],
    properties: set[str],
    base_dir: str,
) -> None:
    """Print terms referenced in HTML but not defined in vocabulary files.

    html_used: term -> { filepath -> set(line_numbers) }
    """
    undefined = {
        term: filename_linenum
        for term, filename_linenum in used.items()
        if term not in classes
        and term not in properties
        and term.split(":", 1)[0] not in SKIP_PREFIXES
    }

    print(
        f"\nTerms referenced in HTML but NOT defined in vocabulary files ({len(undefined)})"
    )
    print("------------------------------------------------------------")
    if not undefined:
        print("Not found.")
        return

    for term, filename_linenum in sorted(undefined.items()):
        found_in: list[str] = []
        for path in sorted(filename_linenum):
            rel = os.path.relpath(path, start=base_dir)
            lines = sorted(filename_linenum[path])
            found_in.append(f"{rel}:{','.join(map(str, lines))}")
        print(f"{term:<40} in: {', '.join(found_in)}")


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


def print_top_unused_parents(
    unused: set[str],
    parents: dict[str, set[str]],
    exclude_prefixes: set[str],
    top_n: int = 10,
    label: str = "Terms",
) -> None:
    """
    Print top parent terms among unused terms

    exclude_prefixes: prefixes to filter out
    top_n: number of top parents to show
    """
    filtered_terms = {
        c
        for c in unused
        if not any(c.startswith(f"{prefix}:") for prefix in exclude_prefixes)
    }
    top_parents = count_parents(filtered_terms, parents).most_common(top_n)

    print(f"\nTop parents among {label} without examples")
    if exclude_prefixes:
        print(f"(excluding child with prefixes: {', '.join(sorted(exclude_prefixes))})")
    print("-------------------------------------------------------------")
    for parent, count in top_parents:
        print(f"{count:>7}  {parent}")


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
        print_top_unused_parents(
            unused_classes,
            parents,
            exclude_prefixes={"loc"},  # There are many unused loc: terms
            top_n=10,
            label="classes",
        )
        print_top_unused_parents(
            unused_properties,
            parents,
            exclude_prefixes=set(),
            top_n=10,
            label="properties",
        )

    if args.list_undefined_terms or args.verbose:
        print_undefined_example_terms(used, classes, properties, examples_dir)

    if args.list_undefined_html_terms or args.verbose:
        html_files = list(get_html_files(vocab_dir))
        html_used = collect_terms_in_htmls(html_files)
        print_undefined_html_terms(html_used, classes, properties, vocab_dir)


if __name__ == "__main__":
    main()
