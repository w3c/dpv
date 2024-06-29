# Diagrams

> The diagrams in this folder are linked in published documents. **DO NOT REMOVE OR MODIFY THEM**. For newer diagrams linked to versioned documented, e.g. a purpose diagram in DPV 2.0, put them in the `2.0/diagrams` folder. If this diagram is used in another document, e.g. the Primer, use the diagram from the versioned folder. If there are diagrams that are present in unversioned documents, e.g. Primer or guides, put them in a subfolder called `docs` i.e. in `/diagrams/docs`.

> Always **include sources** for diagrams so they can be modified when needed. Always use **open source and non-proprietary** formats so that anyone can modify diagrams without purchasing specific tools/software.


## Naming

Please use descriptive names based on the contents of the diagram. If preserving
a prior diagram is necessary, use numbered suffixes, e.g. _diagram-2.png_. Please
ensure the diagram and the source file have the same name.

## Tools and Formats

Any tool or format that is open and can be used by anyone who wants to edit
the diagram is OK. So far, we have used:

- https://plantuml.com/ - text to diagram tool, which can be installed locally, or used online at https://www.plantuml.com/plantuml/ or https://www.planttext.com/
- https://graphviz.org/ - text to diagram tool using DOT language, which you
can install locally or use online, e.g. https://dreampuf.github.io/GraphvizOnline/.
If using this tool, please ensure the outputs are in PNG format, aren't messy
to look at, and the text is discernible. Please provide the source code for the
diagram in a plain text file with the format `.dot`.
- https://app.diagrams.net/ (used to be draw.io) - saves the file in an XML format,
where the conventional extension is `.drawio` (preferred) or `.xml`. If using
this tool, please export images using the PNG format with transparent background
and a border width of 5 (see options when exporting). Please provide the source
file with the preferred extension.
- https://www.yworks.com/products/yed (yED) is another tool that provides a 
relatively more polished experience. Files are saved using `graphml` extension
which is a form of `XML`. If using this tool, please export images using the PNG
format and provide the source code using the `.graphml` extension.

## Adding/Editing Diagrams

- Based on the extension (`.dot,.drawio,.graphml`) you can use the appropriate
tool OR you can re-create the diagram in an alternate tool (see above section).
- Provide both image (PNG) and source files.

## Linking to Diagrams

Use relative links, i.e. prefer `../diagrams` instead of `/diagrams` to have
consistency in the online and local(host) versions as we use w3id.org which 
replaces the root as `w3id.org/dpv` - note the prefix.

## Contributions

Add yourself here if you have contributed to diagrams.

- Harshvardhan J. Pandit
- Georg P Krog
- Delaram Golpayegani
- Julian Flake