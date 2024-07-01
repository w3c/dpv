# DPVCG
Data Privacy Vocabularies and Controls Community Group (DPVCG) repository containing
specifications for Data Privacy Vocabulary (DPV) and its extensions, primer, and guides,
and group meeting minutes.

links: [Community Group](https://www.w3.org/community/dpvcg/) | [GitHub wiki](https://github.com/w3c/dpv/wiki/)

> **Announcement: DPV 2.0 Beta Release**
>
> ![Static Badge](https://img.shields.io/badge/DPV-version%202.0-green?labelColor=black) release is complete and is now being provided in _beta_ mode for feedback. The **period for feedback is until 31 July**. The completed 2.0 release will be published after this on 01 August - unless major issues are identified. See the [v2 changelog](https://w3id.org/dpv/2.0/changelog). The scope of DPV has been expanded to include non-personal data and AI technologies - though the focus of the group remains on privacy and data protection. The structure of the repo has also been changed to incorporate multiple jurisdictions and regulations, and their names have been changed e.g. `dpv-gdpr` is `legal/eu/gdpr`. The draft article [Data Privacy Vocabulary (DPV) -- Version 2](https://arxiv.org/abs/2404.13426) by Pandit et al. (2024) describes DPV v2 in terms of its contents, methodology, current adoptions and uses, and future potential. It also describes the relevance and role of DPV in acting as a common vocabulary to support various regulatory (e.g. EU's DGA and AI Act) and community initiatives (e.g. Solid) emerging across the globe. A [Search Index](https://w3id.org/dpv/2.0/search) of all concepts from DPV and extensions is available.

> ![Static Badge](https://img.shields.io/badge/DPV-version%201.0-red?labelColor=black) is available under a new versioned IRI for continued use - though the DPVCG recommends using the latest version of DPV. Versioned IRIs have been created to refer to specific versions, with https://w3id.org/dpv/1.0 for v1 and https://w3id.org/dpv/2.0 for v2. The versionless IRI https://w3id.org/dpv will always point to the latest version. See the [v2 changelog](https://w3id.org/dpv/2.0/changelog) for more details. 

The mission of the W3C Data Privacy Vocabularies and Controls CG (DPVCG) is to develop a taxonomy of privacy and data protection related terms, which include in particular terms from the new European General Data Protection Regulation (GDPR), such as a taxonomy of personal data as well as a classification of purposes (i.e., purposes for data collection), and events of disclosures, consent, and processing such personal data.

License: All work produced by DPVCG and provided through this repo or elsewhere is provided by contributors under the [W3C Document License](https://www.w3.org/copyright/software-license-2023/). A copy of the license is provided in the [LICENSE.md](./LICENSE.md) file.

[Guidelines for suggesting new concepts, identifying bugs and issues, and sending patches or PRs](https://github.com/w3c/dpv/wiki/contributing)

## Specifications
Newcomers to the DPV are recommended to start with the [Primer](https://w3id.org/dpv/primer) to familiarise themselves with the concepts, semantics, and usefulness of the DPV. A [Concise Primer](https://w3id.org/dpv/primer) is also available for a quick (2-pager) introduction to DPV.
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

The namespace for DPV terms is `http://w3id.org/dpv#` with suggested prefix `dpv`, and serialisations are provided in RDF/XML, Turtle, JSON-LD, and N3 formats. The default serialisations are defined using RDFS/SKOS semantics, with an [alternate serialisation](https://w3id.org/dpv/dpv-owl) defined using OWL2 semantics.

### Extensions
These extensions provide additional concepts that extend the concepts and scope of the main DPV specification:
- [Personal Data (PD)](https://w3id.org/dpv/pd) provides a taxonomy of personal data categories
- [Location (LOC)](https://w3id.org/dpv/loc) provides a taxonomy of location concepts based on ISO 3166 (countries, regions)
- [Technology (TECH)](https://w3id.org/dpv/tech) provides a taxonomy of technology concepts
- [AI](https://w3id.org/dpv/ai) provides a taxonomy of AI concepts extending the TECH extension
- [Justifications](https://w3id.org/dpv/justifications) provides concepts for representing justifications i.e. why something must be done or could not be done
- [Risk](https://w3id.org/dpv/risk) provides concepts for risk assessment and management

### Extensions for Jurisdictions and Regulations
The legal extensions provide concepts associated with specific jurisdictions and the laws, authorities, and treaties within them. The [Legal](https://w3id.org/dpv/legal) page provides an overview of these. The jurisdictions are represented by using their ISO 3166-2 codes.

- [European Union (EU)](https://w3id.org/dpv/legal/eu)
    - [GDPR](https://w3id.org/dpv/legal/eu/gdpr)
    - [DGA](https://w3id.org/dpv/legal/eu/dga)
    - [AI Act](https://w3id.org/dpv/legal/eu/aiact)
    - [Charter of Fundamental Rights](https://w3id.org/dpv/legal/eu/rights)
- [Germany (DE)](https://w3id.org/dpv/legal/de)
- [Ireland (IE)](https://w3id.org/dpv/legal/ie)
- [India (IN)](https://w3id.org/dpv/legal/in)
- [United Kingdom (GB)](https://w3id.org/dpv/legal/gb)
- [United States of America (USA)](https://w3id.org/dpv/legal/usa)

### Other Resources
The [NACE Taxonomy serialised in RDFS](https://w3id.org/dpv/dpv-nace) provides a serialisation of the NACE v2 taxonomy in RDFS for use with DPV terms. Since then, NACE v2.1 has been published by the EU Commission. The DPVCG has decided to retire/not provide an alternative serialisation of NACE as it provided no significant benefit and the best practice for using NACE is to always utilise the official authoritative version.

## Guides
- The [Primer](https://w3id.org/dpv/primer) is an introductory document for newcomers to understand the DPV and its concepts. A [2 Page Short Primer](https://w3id.org/dpv/primer/short) provides a succint introduction to the DPV. 
- The [Use-Cases and Requirements](https://w3id.org/dpv/use-cases/) document lists the use-cases and requirements that led to the development of DPV. 
- The [Examples](https://w3id.org/dpv/examples/) page provides an index of examples describing the use of DPV concepts.
- The [Guides](https://w3id.org/dpv/guides) page lists guides for use of DPV in specific domains and applications
    - [Using DPV in OWL2](https://w3id.org/dpv/guides/dpv-owl) 
    - [Implementing ISO/IEC 27560:2023 Consent Records and Receipts](https://w3id.org/dpv/guides/consent-27560)
    - [Implementing ISO/IEC 29184:2020 Privacy Notices and Consent](https://w3id.org/dpv/guides/notice-29184) - Work in Progress, we welcome participation for this
    - [Data Breach Management for GDPR](https://w3id.org/dpv/guides/gdpr-data-breach) - Work in Progress, we welcome participation for this
    - [Data Protection Impact Assessment (DPIA) for GDPR](https://w3id.org/dpv/guides/gdpr-dpia) - Work in Progress, we welcome participation for this
    - [Records of Processing Activities (ROPA) for GDPR](https://w3id.org/dpv/guides/gdpr-ropa) - Work in Progress, we welcome participation for this

## Acknowledgements and Citation

* For use of DPV from v2 onwards, **Cite as:** [Data Privacy Vocabulary (DPV) -- Version 2](https://arxiv.org/abs/2404.13426) by Harshvardhan J. Pandit, Beatriz Esteves, Georg P. Krog, Paul Ryan, Delaram Golpayegani, Julian Flake https://arxiv.org/abs/2404.13426 (2024)
*  For use of DPV up to v1 and v1.1, **Cite as:** The peer-reviewed article “[Creating A Vocabulary for Data Privacy](https://link.springer.com/chapter/10.1007%2F978-3-030-33246-4_44)” presents a historical overview of the DPVCG, and describes the methodology and structure of the DPV along with describing its creation. An open-access version can be accessed [here](http://hdl.handle.net/2262/91581), [here](http://doras.dcu.ie/23801/), and [here](https://aic.ai.wu.ac.at/~polleres/publications/pand-etal-2019ODBASE.pdf).

## Releases

> [go to latest release](https://github.com/w3c/dpv/releases/latest)

Releases are provided through the GitHub feature at [https://github.com/w3c/dpv/releases](https://github.com/w3c/dpv/releases) and contain zipped collections of DPV specifications, modules, extensions, and accompanying documents. 

### Final Reports

The following are final reports i.e. formally published by the W3C:
#### v2
- these reports will be published and available after the release of v2
- [Search Index](https://w3id.org/dpv/2.0/search) of all concepts from DPV and extensions
#### v1
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

## Participating and Getting assistance

If you're unsure about something, or would like clarifications, or suggestions - please communicate with us or open an issue. We would be happy to help. You can view the [current open issues](https://github.com/w3c/dpv/issues) and the [public mailing list](https://lists.w3.org/Archives/Public/public-dpvcg/).

Membership to the group is open to all interested individuals and organisations. To join the group, you need a valid W3C account – which is free to get and can be [requested here](https://www.w3.org/accounts/request). The group meets usually through online meeting calls - see [meetings calendar](https://www.w3.org/groups/cg/dpvcg/calendar) and [minutes](https://w3id.org/dpv/meetings/).

## Funding Acknowledgements

The DPVCG was established as part of the [SPECIAL H2020 Project](https://specialprivacy.ercim.eu/), which received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 731601 from 2017 to 2019.

Harshvardhan J. Pandit was funded to work as the chair of DPVCG from 2020 to 2022 by the [Irish Research Council\'s](https://research.ie/) Government of Ireland Postdoctoral Fellowship Grant#GOIPD/2020/790, and through the [ADAPT SFI Centre](https://www.adaptcentre.ie/) for Digital Media Technology is funded by Science Foundation Ireland through the SFI Research Centres Programme and is co-funded under the European Regional Development Fund (ERDF) through Grant#13/RC/2106 (2018 to 2020) and Grant#13/RC/2106_P2 (2021 onwards).

Further funding acknowledgements for individual members are provided within relevant specifications.
