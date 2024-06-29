# DPV Version 1.0

> The namespace and IRI of files in this version have been changed to reflect the versioned provision e.g. https://w3id.org/dpv/1.0 instead of https://w3id.org/dpv which now points at the latest version. The IRIs in 1.0 will continue to function regardless of changes in folder structure and IRIs in 2.0.

The mission of the W3C Data Privacy Vocabularies and Controls CG (DPVCG) is to develop a taxonomy of privacy and data protection related terms, which include in particular terms from the new European General Data Protection Regulation (GDPR), such as a taxonomy of personal data as well as a classification of purposes (i.e., purposes for data collection), and events of disclosures, consent, and processing such personal data.

> Newcomers to the DPV are recommended to start with the [Primer](https://w3id.org/dpv/primer) to familiarise themselves with the concepts, semantics, and usefulness of the DPV.

License: All work produced by DPVCG and provided through this repo or elsewhere is provided by contributors under the [W3C Document License](https://www.w3.org/copyright/software-license-2023/). A copy of the license is provided in the [LICENSE.md](./LICENSE.md) file.

## Specifications
### Data Privacy Vocabulary (DPV)
The [Data Privacy Vocabulary (DPV)](https://w3id.org/dpv) provides an ontology (classes and properties) and taxonomies of concepts to represent information regarding how personal data is processed in the form of an ontology or a knowledge graph. For example, it provides taxonomies associated with:

* purposes of processing
* personal data categories involved
* processing operations
* technical and organisational measures or restrictions applied
* legal basis used to justify processing
* information about legal basis for processing
* rights as applicable
* risks as applicable

The namespace for DPV terms is `http://w3id.org/dpv#` with suggested prefix `dpv`, and serialisations are provided in RDF/XML, Turtle, JSON-LD, and N3 formats. The default serialisations are defined using a custom SKOS extension, with `dpv-skos` providing concepts in RDFS/SKOS semantics, and `dpv-owl` providing concepts in OWL2 semantics.

### Extensions
These extensions provide additional concepts that extend the concepts and scope of the main DPV specification:
- [Personal Data (PD)](https://w3id.org/dpv/dpv-pd) provides a taxonomy of personal data categories
- [Legal](https://w3id.org/dpv/dpv-legal) provides a taxonomy of location concepts based on ISO 3166 (countries, regions) and their laws and authorities
- [Technology (TECH)](https://w3id.org/dpv/dpv-tech) provides a taxonomy of technology concepts
- [Risk](https://w3id.org/dpv/risk) provides concepts for risk assessment and management
- [EU GDPR](https://w3id.org/dpv/dpv-gdpr)
- [EU Charter of Fundamental Rights](https://w3id.org/dpv/rights/eu)

## Acknowledgements and Citation

*  For use of DPV up to v1 and v1.1, **Cite as:** The peer-reviewed article “[Creating A Vocabulary for Data Privacy](https://link.springer.com/chapter/10.1007%2F978-3-030-33246-4_44)” presents a historical overview of the DPVCG, and describes the methodology and structure of the DPV along with describing its creation. An open-access version can be accessed [here](http://hdl.handle.net/2262/91581), [here](http://doras.dcu.ie/23801/), and [here](https://aic.ai.wu.ac.at/~polleres/publications/pand-etal-2019ODBASE.pdf).

### Final Reports

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