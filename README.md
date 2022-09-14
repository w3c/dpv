# DPVCG
Data Privacy Vocabularies and Controls Community Group (DPVCG) repository

[Community Group](https://www.w3.org/community/dpvcg/) | [(W3C) wiki](https://www.w3.org/community/dpvcg/wiki/Main_Page)

> **Call for Comments/Feedbacks for DPV v1.0 release**
>Please provide your comments by **15-OCT-2022** via [GitHub](https://github.com/w3c/dpv/issues/50) or public-dpvcg@w3.org (mailing list).

The mission of the W3C Data Privacy Vocabularies and Controls CG (DPVCG) is to develop a taxonomy of privacy and data protection related terms, which include in particular terms from the new European General Data Protection Regulation (GDPR), such as a taxonomy of personal data as well as a classification of purposes (i.e., purposes for data collection), and events of disclosures, consent, and processing such personal data.

> Newcomers to the DPV are recommended to start with the [Primer](https://w3id.org/dpv/primer) to familiarise themselves with the concepts, semantics, and usefulness of the DPV.

License: All work produced by DPVCG and provided through this repo or elsewhere is provided by contributors under the [W3C Document License](https://www.w3.org/Consortium/Legal/2015/doc-license). A copy of the license is provided in the [LICENSE.md](./LICENSE.md) file.

## Releases

> [latest release](https://github.com/w3c/dpv/releases/latest)

Releases are provided through the GitHub feature at [https://github.com/w3c/dpv/releases](https://github.com/w3c/dpv/releases). These contained zipped collections of DPV specifications, modules, extensions, and accompanying documents, categorised by serialisation. Currently, the following types of releases are provided:

- dpv (`dpv.zip`) : The core and canocical DPV specification serialised as a SKOS collection of terms
- dpv-skos (`dpv-skos.zip`) : DPV serialised using RDFS and SKOS semantics
- dpv-owl (`dpv-owl.zip`) : DPV serialised using OWL2 semantics
- dpv (`dpv.xlsx`) : DPV's terms provided in a spreadsheet

## DPV Family of Documents

**Core documents:**

* [Primer for Data Privacy Vocabulary](https://www.w3id.org/dpv/primer): introductory document to DPV concepts
    
> **Note:** Newcomers to the DPV are **strongly recommended to first read through the Primer** to familiarise themselves with the semantics and concepts of DPV.
    
*   [Data Privacy Vocabulary (DPV) Specification](https://www.w3id.org/dpv): (this document) formal and normative description of DPV and its concepts.

**Serialisations of DPV:**

-   [Data Privacy Vocabulary serialised using SKOS+RDFS (DPV-SKOS)](https://www.w3id.org/dpv/dpv-skos): serialisation of DPV with SKOS and RDFS semantics
-   [Data Privacy Vocabulary serialised using OWL2 (DPV-OWL)](https://www.w3id.org/dpv/dpv-owl): serialisation of DPV using OWL2 semantics

**Extensions to Concepts:**
-   [GDPR Extension for Data Privacy Vocabulary (DPV-GDPR)](https://www.w3id.org/dpv/dpv-gdpr): extends DPV concepts for GDPR
-   [Personal Data Categories Extension for Data Privacy Vocabulary (DPV-PD)](https://www.w3id.org/dpv/dpv-pd)
-   [Legal Extension providing Jurisdictions, Laws, and Authorities for Data Privacy Vocabulary (DPV-LEGAL)](https://www.w3id.org/dpv/dpv-legal)
-   [Risk Extension providing concepts related to risk assessment and management (RISK)](https://www.w3id.org/dpv/risk)
-   [Rights Extension providing concepts related to rights (RIGHTS)](https://www.w3id.org/dpv/rights)

**Guides and Tutorials**
-   [Guidelines for Adoption and Use of DPV](https://w3id.org/dpv/guides): [Using DPV in OWL2](https://w3id.org/dpv/guides/dpv-owl)

**Other Resources:**
-   [NACE Taxonomy serialised in RDFS](https://www.w3id.org/dpv/dpv-nace)

**Related Links**
*   For a general overview of the Data Protection Vocabularies and Controls Community Group \[[DPVCG](#bib-dpvcg "W3C Data Privacy Vocabularies and Controls Community Group (DPVCG)")\], its history, deliverables, and activities - refer to [DPVCG Website](https://www.w3.org/community/dpvcg/).
*   **Cite as:** The peer-reviewed article “[Creating A Vocabulary for Data Privacy](https://link.springer.com/chapter/10.1007%2F978-3-030-33246-4_44)” presents a historical overview of the DPVCG, and describes the methodology and structure of the DPV along with describing its creation. An open-access version can be accessed [here](http://hdl.handle.net/2262/91581), [here](http://doras.dcu.ie/23801/), and [here](https://aic.ai.wu.ac.at/~polleres/publications/pand-etal-2019ODBASE.pdf).

## Data Privacy Vocabulary (DPV)

The Data Privacy Vocabulary provides terms (classes and properties) to annotate and categorize instances of legally compliant personal data handling according to the EU General Data Protection Regulation. This scope could be extended by later versions to other data and privacy protection regulations. 

The vocabulary provides terms to describe:

* purposes of processing
* personal data categories involved
* processing operations
* technical and organisational measures or restrictions applied
* legal basis used to justify processing
* information about legal basis for processing
* rights as applicable
* risks as applicable

The namespace for DPV terms is `http://www.w3id.org/dpv#` with suggested prefix `dpv`. The IRI for DPV is currently redirected to serve the files hosted in this repository from GitHub pages i.e. `https://w3c.github.io/dpv/dpv/` (thanks to @bert-github for setting this up). Content-negotiation should therefore be supported for all files/serialisations of the DPV and its modules.

### DPV and Modules

The term 'DPV' represents the entire vocabulary - with its concepts and terms as defined in the specification. Serialisations for this in `rdf+xml`, `json-ld`, and `turtle` are provided. The 'modules' in DPV are separate files for each of the hierarchies and concept taxonomies - for example 'purposes'. These are defined in the `rdf` folder with serialisations for each module. The `core` or `base` vocabulary or ontology is defined containing the top-level classes and data model (i.e. `PersonalDataHandling`).

## Contribution / Participation

The DPVCG is the primary forum for contributions and participations regarding the DPV. As such, all decisions and resolutions will be conducted through the group's meetings and call. Membership in DPVCG is not necessary to contribute to DPV, but is recommended for participating in the group's decision making process. Contributions and questions can be sent to the group's [public mailing list](https://lists.w3.org/Archives/Public/public-dpvcg/) or expressed as [GitHub issues](https://github.com/dpvcg/dpv/issues). 

## Suggesting new terms

To suggest a new term, we request following information:

* _term_ 
* _description of the term_
* whether it should be a _class_ or _a property_
* relation to existing term(s) in DPV e.g. through sub-classes
* source (where applicable)
* justification or relevance of why this term should be added (where not obvious)

### Raising issues

Before submitting an issue, please see the whether the issue has been addressed on [GitHub](https://github.com/w3c/dpv/issues). If not, please raise the issue via the group's [public mailing list](https://lists.w3.org/Archives/Public/public-dpvcg/) or expressed as [GitHub issues](https://github.com/w3c/dpv/issues). 

Fixes, corrections to the terms are considered as issues and can be submitted similarly. For minor changes, we may prefer to incorporate them directly rather than through pull requests and patches. For larger issues, please check with the group before submitting a pull-request to ensure its appropriate and efficient incorporation.

## Development Guide

> please refrain from making changes by-hand or manually

The development and maintainence of DPV takes place primarily through a shared spreadsheet. The terms and their annotated metadata are declared in the spreadsheet, and used as input to generate the RDF files and HTML documentation through the [documentation-generator](https://github.com/w3c/dpv/tree/master/documentation-generator) tooling. The `documentation` tool is a collection of Python scripts to assist in the automation of downloading the spreadsheet as CSV files, generating RDF files, validating them for correctness, and producing the HTML documentation.

Therefore, whenever adding a new term or changing existing ones, the following steps are recommended to update the DPV vocabulary and documentation:

1. Make changes appropriately in the shared spreadsheet. The links to this are available to the DPVCG members. For others, please see the CSV files in `documentation_generator/vocab_csv`. Ideally, create an GitHub issue for discussions and follow ups.
2. Use the [documentation-generator](https://github.com/w3c/dpv/tree/master/documentation-generator) tooling to download the spreadsheet, generate RDF, test it, generate HTML output. 
3. Manually inspect whether the changes have been made. Tools, scripts, and software in general can propogate errors silently. 
4. The variables and parameters in  [documentation-generator](https://github.com/w3c/dpv/tree/master/documentation-generator) tooling can be used to define the path where files are exported to can be set to the `dpv` repository to make changes in this directory. For e.g. `EXPORT_DPV_HTML_PATH = ~/code/dpvcg/dpv` will generate the HTML documentation in the `dpv` directory. 
5. Submit a pull-request for merging with the repository.

## Getting help and assistance

If you're unsure about something, or would like clarifications, or suggestions - please drop us a line or open an issue. We would be happy to help.