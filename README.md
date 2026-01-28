# DPVCG

Data Privacy Vocabularies and Controls Community Group (DPVCG) repository containing
specifications for Data Privacy Vocabulary (DPV) and its extensions, primer, and guides,
and group meeting minutes.

links: [Community Group](https://www.w3.org/community/dpvcg/) | [GitHub wiki](https://github.com/w3c/dpv/wiki/)

The mission of the W3C Data Privacy Vocabularies and Controls CG (DPVCG) is to develop a taxonomy of privacy and data protection related terms, which include in particular terms from the European General Data Protection Regulation (GDPR), such as a taxonomy of personal data as well as a classification of purposes (i.e., purposes for data collection), and events of disclosures, consent, and processing such personal data.

License: All work produced by DPVCG and provided through this repo or elsewhere is provided by contributors under the [W3C Document License](https://www.w3.org/copyright/software-license-2023/) unless otherwise noted. A copy of the license is provided in the [LICENSE.md](./LICENSE.md) file.

[Guidelines for suggesting new concepts, identifying bugs and issues, and sending patches or PRs](https://github.com/w3c/dpv/wiki/Contribution-Guide)

## Specifications

Newcomers to the DPV are recommended to start with the [Primer](https://w3id.org/dpv/primer) to familiarise themselves with the concepts, semantics, and usefulness of the DPV. A [Concise Primer](https://w3id.org/dpv/primer/concise) is also available for a quick (2-pager) introduction to DPV.

### Data Privacy Vocabulary (DPV)

The [Data Privacy Vocabulary (DPV)](https://w3id.org/dpv) provides an ontology (classes and properties) along with taxonomies that represent real-world uses of these concepts for representing information regarding how (personal) data and technologies (including AI). For example, it provides concepts and taxonomies to represent:

- purposes of processing data or using technologies
- personal data categories
- processing operations on data
- technical and organisational measures for safeguarding data and processes
- legal basis used to indicate why it is legally permitted
- rights involved and how to exercise them
- risks applicable and what would be its consequences and impacts

> The versionless base IRI, e.g. `https://w3id.org/dpv`, always points to the latest release which is a versioned IRI, e.g. `https://w3id.org/dpv/2.2` for v2.2.

The namespace for DPV terms is `http://w3id.org/dpv#` with suggested prefix `dpv`, and serialisations are provided in RDF/XML, Turtle, JSON-LD, and N3 formats. The default serialisations are defined using RDFS/SKOS semantics, with an [alternate serialisation](https://w3id.org/dpv/dpv-owl) defined using OWL2 semantics.

### Extensions

These extensions provide additional concepts that extend the concepts and scope of the main DPV specification:

- [Personal Data (PD)](https://w3id.org/dpv/pd) provides a taxonomy of personal data categories;
- [Location (LOC)](https://w3id.org/dpv/loc) provides a taxonomy of location concepts based on ISO 3166 (countries, regions);
- [Technology (TECH)](https://w3id.org/dpv/tech) provides a taxonomy of technology concepts;
- [AI](https://w3id.org/dpv/ai) provides a taxonomy of AI concepts extending the TECH extension;
- [Justifications](https://w3id.org/dpv/justifications) provides concepts for representing justifications i.e. why something must be done or could not be done;
- [Risk](https://w3id.org/dpv/risk) provides concepts for risk assessment and management;

In v2.1, the Sector and Standard group of extensions was added to the DPV specifications. [Sector](https://w3id.org/dpv/sector) provides sector-specific concepts which extend concepts in other DPV extensions. Currently, the following sectors are represented:

- [SECTOR-EDUCATION](https://w3id.org/dpv/sector/education) for Education Sector
- [SECTOR-FINANCE](https://w3id.org/dpv/sector/finance) for Finance Sector
- [SECTOR-HEALTH](https://w3id.org/dpv/sector/health) for Health Sector
- [SECTOR-INFRA](https://w3id.org/dpv/sector/infra) for (Critical) Infrastructure Sector
- [SECTOR-LAW](https://w3id.org/dpv/sector/law) for Law Enforcement & Justice Sector
- [SECTOR-PUBLICSERVICES](https://w3id.org/dpv/sector/publicservices) for Public Services Sector

The Standards extensions are aimed to provide additional concepts for implementing specific standards using DPV. Currently it contains [IEEE-P7012](https://w3id.org/dpv/standards/p7012) based on [IEEE P7012 Draft Standard for Machine Readable Personal Privacy Terms](https://standards.ieee.org/ieee/7012/7192/).

### Extensions for Jurisdictions and Regulations

The LEGAL extensions provide concepts associated with specific jurisdictions and the laws, authorities, and treaties within them. The [Legal](https://w3id.org/dpv/legal) page provides an overview of these. The jurisdictions are represented by using their ISO 3166-2 codes.

- [European Union (EU)](https://w3id.org/dpv/legal/eu) with the following laws provided as modular extensions within the EU namespace:
    - [General Data Protection Regulation (EU-GDPR)](https://w3id.org/dpv/legal/eu/gdpr)
    - [Data Governance Act (EU-DSA)](https://w3id.org/dpv/legal/eu/dga)
    - [Artificial Intelligence Act (EU-AIAct)](https://w3id.org/dpv/legal/eu/aiact)
    - [Network and Information Systems Directive (EU-NIS2)](https://w3id.org/dpv/legal/eu/nis2)
    - [European Health Data Spaces (EU-EHDS)](https://w3id.org/dpv/legal/eu/ehds)
    - [Charter of Fundamental Rights (EU-RIGHTS)](https://w3id.org/dpv/legal/eu/rights)
- [LEGAL-AT](https://w3id.org/dpv/legal/at) for Austria
- [LEGAL-BE](https://w3id.org/dpv/legal/be) for Belgium
- [LEGAL-BG](https://w3id.org/dpv/legal/bg) for Bulgaria
- [LEGAL-CY](https://w3id.org/dpv/legal/cy) for Cyprus
- [LEGAL-CZ](https://w3id.org/dpv/legal/cz) for the Czech Republic
- [LEGAL-DE](https://w3id.org/dpv/legal/de) for Germany
- [LEGAL-DK](https://w3id.org/dpv/legal/dk) for Denmark
- [LEGAL-EE](https://w3id.org/dpv/legal/ee) for Estonia
- [LEGAL-ES](https://w3id.org/dpv/legal/es) for Spain
- [LEGAL-FI](https://w3id.org/dpv/legal/fi) for Finland
- [LEGAL-FR](https://w3id.org/dpv/legal/fr) for France
- [LEGAL-GB](https://w3id.org/dpv/legal/gb) for Great Britain and Northern Ireland
- [LEGAL-GR](https://w3id.org/dpv/legal/gr) for Greece
- [LEGAL-HK](https://w3id.org/dpv/legal/hk) for Hong Kong
- [LEGAL-HR](https://w3id.org/dpv/legal/hr) for Croatia
- [LEGAL-HU](https://w3id.org/dpv/legal/hu) for Hungary
- [LEGAL-IE](https://w3id.org/dpv/legal/ie) for Ireland
- [LEGAL-IN](https://w3id.org/dpv/legal/in) for India
- [LEGAL-IS](https://w3id.org/dpv/legal/is) for Iceland
- [LEGAL-IT](https://w3id.org/dpv/legal/it) for Italy
- [LEGAL-JP](https://w3id.org/dpv/legal/jp) for Japan
- [LEGAL-KR](https://w3id.org/dpv/legal/kr) for Republic of Korea
- [LEGAL-LI](https://w3id.org/dpv/legal/li) for Liechtenstein
- [LEGAL-LT](https://w3id.org/dpv/legal/lt) for Lithuania
- [LEGAL-LU](https://w3id.org/dpv/legal/lu) for Luxembourg
- [LEGAL-LV](https://w3id.org/dpv/legal/lv) for Latvia
- [LEGAL-MO](https://w3id.org/dpv/legal/mo) for Macao
- [LEGAL-MT](https://w3id.org/dpv/legal/mt) for Malta
- [LEGAL-MY](https://w3id.org/dpv/legal/my) for Malaysia
- [LEGAL-NL](https://w3id.org/dpv/legal/nl) for the Netherlands
- [LEGAL-NO](https://w3id.org/dpv/legal/no) for Norway
- [LEGAL-PH](https://w3id.org/dpv/legal/ph) for the Philippines
- [LEGAL-PL](https://w3id.org/dpv/legal/pl) for Poland
- [LEGAL-PT](https://w3id.org/dpv/legal/pt) for Portugal
- [LEGAL-RO](https://w3id.org/dpv/legal/ro) for Romania
- [LEGAL-SE](https://w3id.org/dpv/legal/se) for Sweden
- [LEGAL-SG](https://w3id.org/dpv/legal/sg) for Singapore
- [LEGAL-SI](https://w3id.org/dpv/legal/si) for Slovenia
- [LEGAL-SK](https://w3id.org/dpv/legal/sk) for Slovakia
- [LEGAL-TH](https://w3id.org/dpv/legal/th) for Thailand
- [LEGAL-TW](https://w3id.org/dpv/legal/tw) for Taiwan
- [LEGAL-US](https://w3id.org/dpv/legal/us) for the United States of America

### Other Resources

The NACE Taxonomy serialised in RDFS (previously available at <https://w3id.org/dpv/dpv-nace>) provided a serialisation of the NACE v2 taxonomy in RDFS for use with DPV terms. Since then, [NACE v2.1](https://ec.europa.eu/eurostat/web/nace) has been published by the EU Commission. The DPVCG has decided to retire/not provide an alternative serialisation of NACE as it provided no significant benefit and the best practice for using NACE is to always utilise the official authoritative version.

## Guides

- The [Primer](https://w3id.org/dpv/primer) is an introductory document for newcomers to understand the DPV and its concepts. A [2-Page Concise Primer](https://w3id.org/dpv/primer/concise) provides a succinct introduction to the DPV.
- The [Use-Cases and Requirements](https://w3id.org/dpv/use-cases/) document lists the use-cases and requirements that led to the development of DPV.
- The [Examples](https://w3id.org/dpv/examples/) page provides an index of examples describing the use of DPV concepts.
- The [Guides](https://w3id.org/dpv/guides) page lists guides for use of DPV in specific domains and applications
    - [Using DPV in OWL2](https://w3id.org/dpv/guides/dpv-owl)
    - [Implementing ISO/IEC 27560:2023 Consent Records and Receipts](https://w3id.org/dpv/guides/consent-27560)

In addition to the above, we welcome participation in the following guides being developed:

- [Using DPV with RDFS and SKOS](https://w3id.org/dpv/guides/dpv-skos)
- [Using DPV with JSON and CSV for non-semantic web systems](https://w3id.org/dpv/guides/dpv-misc)
- [Using DPV with ODRL](https://w3id.org/dpv/guides/dpv-odrl)
- [Implementing ISO/IEC 29184:2020 Privacy Notices and Consent](https://w3id.org/dpv/guides/notice-29184)
- [Data Breach Management for GDPR](https://w3id.org/dpv/guides/gdpr-data-breach)
- [Data Protection Impact Assessment (DPIA) for GDPR](https://w3id.org/dpv/guides/gdpr-dpia)
- [Records of Processing Activities (ROPA) for GDPR](https://w3id.org/dpv/guides/gdpr-ropa)
- [Rights Management and Exercise](https://w3id.org/dpv/guides/rights)

## Acknowledgements and Citation

- For use of DPV from v2 onwards, **Cite as:** [Data Privacy Vocabulary (DPV) -- Version 2](https://doi.org/10.1007/978-3-031-77847-6_10) by Harshvardhan J. Pandit, Beatriz Esteves, Georg P. Krog, Paul Ryan, Delaram Golpayegani, Julian Flake; 23rd International Semantic Web Conference (ISWC 2024) https://doi.org/10.1007/978-3-031-77847-6_10
- For use of DPV up to v1 and v1.1, **Cite as:** The peer-reviewed article “[Creating A Vocabulary for Data Privacy](https://link.springer.com/chapter/10.1007%2F978-3-030-33246-4_44)” presents a historical overview of the DPVCG, and describes the methodology and structure of the DPV along with describing its creation. An open-access version can be accessed [here](http://hdl.handle.net/2262/91581), [here](http://doras.dcu.ie/23801/), and [here](https://aic.ai.wu.ac.at/~polleres/publications/pand-etal-2019ODBASE.pdf).
- In addition to the above, each specifications or document may have additional references for peer-reviewed articles associated with it - these are provided at the top of each document.

## Releases

> [go to latest release](https://github.com/w3c/dpv/releases/latest)

Releases are provided through the GitHub feature at [https://github.com/w3c/dpv/releases](https://github.com/w3c/dpv/releases) and contain zipped collections of DPV specifications, modules, extensions, and accompanying documents.

### Final Reports

A full list of reports (i.e. formally published by the W3C) produced by the CG is available in [CG-REPORTS](./CG-REPORTS.md). Note that works considered to be in a 'draft' state are not formally published in this manner. Below are reports corresponding to the latest release v2.2.

- Primer [w3c/cg-reports link to be added]()
- DPV [w3c/cg-reports link to be added]()
- Personal Data (PD) extension [w3c/cg-reports link to be added]()
- Technology (TECH) extension [w3c/cg-reports link to be added]()
- Risk (RISK) extension [w3c/cg-reports link to be added]()
- Locations (LOC) extension [w3c/cg-reports link to be added]()
- AI Technology (AI) extension [w3c/cg-reports link to be added]()
- Justifications extension [w3c/cg-reports link to be added]()
- Legal extensions [w3c/cg-reports link to be added]()
    - Austria (LEGAL-AT) [w3c/cg-reports link to be added]()
    - Belgium (LEGAL-BE) [w3c/cg-reports link to be added]()
    - Bulgaria (LEGAL-BG) [w3c/cg-reports link to be added]()
    - Cyprus (LEGAL-CY) [w3c/cg-reports link to be added]()
    - Czech Republic (LEGAL-CZ) [w3c/cg-reports link to be added]()
    - Germany (LEGAL-DE) [w3c/cg-reports link to be added]()
    - Denmark (LEGAL-DK) [w3c/cg-reports link to be added]()
    - Estonia (LEGAL-EE) [w3c/cg-reports link to be added]()
    - Spain (LEGAL-ES) [w3c/cg-reports link to be added]()
    - European Union (EU) [w3c/cg-reports link to be added]()
    - Finland (LEGAL-FI) [w3c/cg-reports link to be added]()
    - France (LEGAL-FR) [w3c/cg-reports link to be added]()
    - Great Britain and Northern Ireland (LEGAL-GB) [w3c/cg-reports link to be added]()
    - Greece (LEGAL-GR) [w3c/cg-reports link to be added]()
    - Hong Kong (LEGAL-HK) [w3c/cg-reports link to be added]()
    - Croatia (LEGAL-HR) [w3c/cg-reports link to be added]()
    - Hungary (LEGAL-HU) [w3c/cg-reports link to be added]()
    - Ireland (LEGAL-IE) [w3c/cg-reports link to be added]()
    - India (LEGAL-IN) [w3c/cg-reports link to be added]()
    - Iceland (LEGAL-IS) [w3c/cg-reports link to be added]()
    - Italy (LEGAL-IT) [w3c/cg-reports link to be added]()
    - Japan (LEGAL-JP) [w3c/cg-reports link to be added]()
    - Republic of Korea (LEGAL-KR) [w3c/cg-reports link to be added]()
    - Liechtenstein (LEGAL-LI) [w3c/cg-reports link to be added]()
    - Lithuania (LEGAL-LT) [w3c/cg-reports link to be added]()
    - Luxembourg (LEGAL-LU) [w3c/cg-reports link to be added]()
    - Latvia (LEGAL-LV) [w3c/cg-reports link to be added]()
    - Macao (LEGAL-MO) [w3c/cg-reports link to be added]()
    - Malta (LEGAL-MT) [w3c/cg-reports link to be added]()
    - Malaysia (LEGAL-MY) [w3c/cg-reports link to be added]()
    - Netherlands (LEGAL-NL) [w3c/cg-reports link to be added]()
    - Norway (LEGAL-NO) [w3c/cg-reports link to be added]()
    - the Philippines (LEGAL-PH) [w3c/cg-reports link to be added]()
    - Poland (LEGAL-PL) [w3c/cg-reports link to be added]()
    - Portugal (LEGAL-PT) [w3c/cg-reports link to be added]()
    - Romania (LEGAL-RO) [w3c/cg-reports link to be added]()
    - Sweden (LEGAL-SE) [w3c/cg-reports link to be added]()
    - Singapore (LEGAL-SG) [w3c/cg-reports link to be added]()
    - Slovenia (LEGAL-SI) [w3c/cg-reports link to be added]()
    - Slovakia (LEGAL-SK) [w3c/cg-reports link to be added]()
    - Thailand (LEGAL-TH) [w3c/cg-reports link to be added]()
    - Taiwan (LEGAL-TW) [w3c/cg-reports link to be added]()
    - United States of America (LEGAL-US) [w3c/cg-reports link to be added]()
- Legal extensions modelling laws
    - EU General Data Protection Regulation (EU-GDPR) [w3c/cg-reports link to be added]()
    - EU Data Governance Act (EU-DSA) [w3c/cg-reports link to be added]()
    - EU Artificial Intelligence Act (EU-AIAct) [w3c/cg-reports link to be added]()
    - EU Network and Information Systems Directive (EU-NIS2) [w3c/cg-reports link to be added]()
    - EU Health Data Spaces (EU-EHDS) [w3c/cg-reports link to be added]()
    - EU Charter of Fundamental Rights (EU-RIGHTS) [w3c/cg-reports link to be added]()

## Participating and Getting assistance

If you're unsure about something, or would like clarifications, or suggestions - please communicate with us or open an issue. We would be happy to help. You can view the [current open issues](https://github.com/w3c/dpv/issues) and the [public mailing list](https://lists.w3.org/Archives/Public/public-dpvcg/).

Membership to the group is open to all interested individuals and organisations. To join the group, you need a valid W3C account – which is free to get and can be [requested here](https://www.w3.org/accounts/request). The group usually meets through online meeting calls - see [meetings calendar](https://www.w3.org/groups/cg/dpvcg/calendar) and [minutes](https://w3id.org/dpv/meetings/).

## Funding Acknowledgements

The DPVCG was established as part of the [SPECIAL H2020 Project](https://specialprivacy.ercim.eu/), which received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 731601 from 2017 to 2019.

Harshvardhan J. Pandit was funded to maintain these specifications and to chair the DPVCG from 2020 to 2022 by the [Irish Research Council\'s](https://research.ie/) Government of Ireland Postdoctoral Fellowship Grant#GOIPD/2020/790, and through the [ADAPT SFI Centre](https://www.adaptcentre.ie/) for Digital Media Technology which is funded by Science Foundation Ireland through the SFI Research Centres Programme and is co-funded under the European Regional Development Fund (ERDF) through Grant#13/RC/2106 (2018 to 2020) and Grant#13/RC/2106_P2 (2021 onwards), and through the AI Accountability Lab (AIAL) which is supported by grants from following groups: the AI Collaborative, an Initiative of the Omidyar Group; Luminate; the Bestseller Foundation; and the John D. and Catherine T. MacArthur Foundation (from 2025 onwards).

Further funding acknowledgements for individual members are provided within relevant specifications.
