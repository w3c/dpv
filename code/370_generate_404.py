#!/usr/bin/env python3

# SPDX-FileContributor: Arthit Suriyawongkul
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: W3C-20150513

import os
import re

# For example, 1.0, 2.0, 2.3-dev, etc.
VERSION_PATTERN = re.compile(r"^\d+\.\d+(\-dev)?$")

ROOT_DIR = ".."
EXCLUDE_DIRS = ["diagrams", "img", "modules"]
NO_LINK_DIRS = ["standards"]

OUTPUT_FILE = "404.html"

BASE_URL_PROD = "https://w3c.github.io/dpv"
BASE_URL_DEV = "https://dev.dpvcg.org"


def ascii_tree(base_path, dpv_version, prefix="", rel_path=""):
    """Recursively build an ASCII tree for folders under base_path"""
    entries = [
        e for e in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, e))
    ]
    entries.sort()
    lines = []
    for i, entry in enumerate(entries):
        if entry in EXCLUDE_DIRS:
            continue
        connector = "└── " if i == len(entries) - 1 else "├── "
        dir_rel_path = f"{rel_path}/{entry}" if rel_path else entry
        if "dev" in dpv_version:
            url = f"{BASE_URL_DEV}/{dpv_version}/{dir_rel_path}/"
        else:
            url = f"{BASE_URL_PROD}/{dpv_version}/{dir_rel_path}/"
        if entry in NO_LINK_DIRS:
            link = f"{entry}"
        else:
            link = f'<a href="{url}">{entry}</a>'

        lines.append(f"    {prefix}{connector}{link}<br>")
        sub_path = os.path.join(base_path, entry)
        sub_entries = [
            e
            for e in os.listdir(sub_path)
            if e not in EXCLUDE_DIRS and os.path.isdir(os.path.join(sub_path, e))
        ]
        if sub_entries:
            indent = "    " if i == len(entries) - 1 else "│   "
            lines.extend(
                ascii_tree(sub_path, dpv_version, prefix + indent, dir_rel_path)
            )
    return lines


version_dirs = [
    name
    for name in os.listdir(ROOT_DIR)
    if os.path.isdir(os.path.join(ROOT_DIR, name)) and VERSION_PATTERN.match(name)
]


def version_sort_key(s):
    parts = s.split("-")  # "-dev" suffix
    nums = [int(x) for x in parts[0].split(".")]
    suffix = tuple(ord(c) for c in parts[1]) if len(parts) > 1 else (0,)
    return nums + list(suffix)


version_dirs.sort(key=version_sort_key, reverse=True)

html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>DPV - 404 error</title>
    <style type="text/css">
        body {
            max-width: 800px;
            margin: auto;
            /*font-family: monospace;*/
        }
        .url {
            color: blue;
        }
    </style>
</head>
<body>
    <h1>404 Error</h1>
    <p><strong>DPVCG Resource Not Found</strong>
    <p>Common causes of this error:</p>
    <ol>
        <li>Typo in the URL - <span id="span-check-url"></span>.</li>
        <li>Used an older unversioned URL - <span id="span-check-version"></span>.</li>
        <li>The page existed before, but doesn't exist now OR it has been moved to a new location under a different name. You can view the available resources below.</li>
    </ol>
    <div id="wb404"/>
    <script src="https://archive.org/web/wb404.js"></script>
"""

for version in version_dirs:
    html_content += f"\n    <h3>DPV v{version}</h3>\n"
    html_content += "    <p>\n"
    tree = ascii_tree(os.path.join(ROOT_DIR, version), version)
    html_content += "\n".join(tree)
    html_content += "\n    </p>\n"

html_content += """
    <script type="text/javascript">
        const url = window.location.href;
        const span_typo = document.getElementById('span-check-url');
        const span_unversioned = document.getElementById('span-check-version');
        const re_check_version = /\d+/;
        class PAGE_STATUS {
            static _PROD = 0;
            static _DEV = 1;
            static _LOCAL = 2;
            static _OTHER = 3;

            static get PROD() { return this._PROD; }
            static get DEV() { return this._DEV; }
            static get LOCAL() { return this._LOCAL; }
            static get OTHER() { return this._OTHER; }
        };
        var MODE = PAGE_STATUS.OTHER;
        if (url.startsWith("https://w3c.github.io/dpv/")) {
            MODE = PAGE_STATUS.PROD;
            var purl = url.replace("https://w3c.github.io/dpv/", "https://w3id.org/dpv/")
            span_typo.innerHTML = "check <span class='url'>"+url+"</span> is correct, or its purl form <a href='"+purl+"'>"+purl+"<a/>";
            if (re_check_version.exec(url.replace("https://w3c.github.io/dpv/", "")) == null) {
                span_unversioned.innerHTML = "you can check whether this versioned form is the url you are looking for: <a href='https://w3c.github.io/dpv/2.1/" + url.replace("https://w3c.github.io/dpv/", "") + "'>https://w3c.github.io/dpv/2.1/" + url.replace("https://w3c.github.io/dpv/", "") + "</a>";
            } else {
                span_unversioned.innerHTML = "but this doesn't appear to be the case";
            }
        } else if (url.startsWith("https://dev.dpvcg.org/")) { 
            MODE = PAGE_STATUS.DEV;
            span_typo.innerHTML = "check <span class='url'>"+url+"</span> is correct";
            if (re_check_version.exec(url.replace("https://dev.dpvcg/org/", "")) == null) {
                span_unversioned.innerHTML = "this appears to be an unversioned url, you can check whether this versioned form is the url you are looking for: <a href='https://dev.dpvcg/org/2.1/" + url.replace("https://dev.dpvcg/org/", "") + "'>https://dev.dpvcg/org/2.1/" + url.replace("https://dev.dpvcg/org/", "") + "</a>";
            } else {
                span_unversioned.innerHTML = "... but this doesn't appear to be the case";
            }
        } else if (url.includes("localhost:")) { 
            MODE = PAGE_STATUS.LOCAL;
            span_typo.innerHTML = "check <span class='url'>"+url+"</span> is correct";
            span_unversioned.innerHTML = "but this doesn't appear to be the case";
        }

        // Typo in the URL
            // .replace("https://w3c.github.io/dpv/", "https://w3id.org/dpv");

        // const span_currenturl = document.getElementById('current-url');
        // span_currenturl.innerHTML = window.location.href;
    </script>
</body>
</html>
"""

output_path = os.path.join(ROOT_DIR, OUTPUT_FILE)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"{output_path} generated from these DPV version directories:")
for folder in version_dirs:
    print(f"- {folder}")
