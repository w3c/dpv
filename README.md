# DPVCG
Data Privacy Vocabularies and Controls Community Group (DPVCG) repository

[Community Group](https://www.w3.org/community/dpvcg/) | [(W3C) wiki](https://www.w3.org/community/dpvcg/wiki/Main_Page)

> [!WARNING]  
> **NOTICE OF PLANNED MAJOR CHANGES**
>
> Major changes as described by: 1) #99 including non-personal data; and 2) #107 repo restructuring -- are planned to be implemented from **30 SEP 2023**. If you wish to raise issues or objections, please do so before then.

The mission of the W3C Data Privacy Vocabularies and Controls CG (DPVCG) is to develop a taxonomy of privacy and data protection related terms, which include in particular terms from the new European General Data Protection Regulation (GDPR), such as a taxonomy of personal data as well as a classification of purposes (i.e., purposes for data collection), and events of disclosures, consent, and processing such personal data.

> Newcomers to the DPV are recommended to start with the [Primer](https://w3id.org/dpv/primer) to familiarise themselves with the concepts, semantics, and usefulness of the DPV.

License: All work produced by DPVCG and provided through this repo or elsewhere is provided by contributors under the [W3C Document License](https://www.w3.org/Consortium/Legal/2015/doc-license). A copy of the license is provided in the [LICENSE.md](./LICENSE.md) file.

Contributing: See [contributing.md](./contributing.md)

## Releases

> [latest release](https://github.com/w3c/dpv/releases/latest)

Releases are provided through the GitHub feature at [https://github.com/w3c/dpv/releases](https://github.com/w3c/dpv/releases). These contained zipped collections of DPV specifications, modules, extensions, and accompanying documents, categorised by serialisation. Currently, the following types of releases are provided:

- dpv (`dpv.zip`) : The core and canocical DPV specification serialised as a SKOS collection of terms
- dpv-skos (`dpv-skos.zip`) : DPV serialised using RDFS and SKOS semantics
- dpv-owl (`dpv-owl.zip`) : DPV serialised using OWL2 semantics
- dpv (`dpv.xlsx`) : DPV's terms provided in a spreadsheet

### Final Reports

The following vocabularies are being published as v1 and final reports of the group:

- Primer [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-primer-20221205)
- DPV [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-20221205)
- DPV-GDPR [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-gdpr-20221205)
- DPV-PD [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-pd-20221205)
- DPV-OWL [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-owl-20221205)
- DPV-OWL-GDPR [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-owl-gdpr-20221205)
- DPV-OWL-PD [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-owl-pd-20221205)
- Guide on using DPV in OWL2 [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-guide-dpv-owl-20221006)
- DPV-SKOS [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-skos-20221205)
- DPV-SKOS-GDPR [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-skos-gdpr-20221205)
- DPV-SKOS-PD [w3c/cg-reports link](https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-skos-pd-20221205)

## DPV Family of Documents

**Core documents:**

* [Primer for Data Privacy Vocabulary](https://www.w3id.org/dpv/primer): introductory document to DPV concepts
    
> **Note:** Newcomers to the DPV are **strongly recommended to first read through the Primer** to familiarise themselves with the semantics and concepts of DPV.
    
*   [Data Privacy Vocabulary (DPV) Specification](https://www.w3id.org/dpv): (this document) formal and normative description of DPV and its concepts.
*   [Use-Cases and Requirements](https://w3id.org/dpv/use-cases/)
*   [Examples](https://w3id.org/dpv/examples/)

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

## Getting help and assistance

If you're unsure about something, or would like clarifications, or suggestions - please communicate with us or open an issue. We would be happy to help.