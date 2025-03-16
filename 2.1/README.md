# DPV 2.1

> ![Static Badge](https://img.shields.io/badge/DPV-version%202.1-green?labelColor=black) DPV 2.1 is the continued expansion of DPV 2.0's broadened scope regarding data and (AI) technologies and includes new draft extensions for jurisdictions, laws, and sectors. The article [Data Privacy Vocabulary (DPV) -- Version 2](https://arxiv.org/abs/2404.13426) describes the structure of DPV v2.0+ specifications in terms of its contents, methodology, current adoptions and uses, and future potential. It also describes the relevance and role of DPV in acting as a common vocabulary to support various regulatory (e.g. EU's DGA and AI Act) and community initiatives (e.g. Solid) emerging across the globe. A [Search Index](https://w3id.org/dpv/2.1/search) of all concepts from DPV and extensions is available. See the [v2.1 changelog](https://w3id.org/dpv/2.1/changelog.html) for more details. 

License: All work produced by DPVCG and provided through this repo or elsewhere is provided by contributors under the [W3C Software and Document License](https://www.w3.org/copyright/software-license-2023/) unless otherwise noted. A copy of the license is provided in the [LICENSE.md](./LICENSE.md) file.

## Specifications
Newcomers to the DPV are recommended to start with the [Primer](https://w3id.org/dpv/primer) to familiarise themselves with the concepts, semantics, and usefulness of the DPV. A [Concise Primer](https://w3id.org/dpv/primer) is also available for a quick (2-pager) introduction to DPV.

### Data Privacy Vocabulary (DPV)
The [Data Privacy Vocabulary (DPV)](https://w3id.org/dpv) provides an ontology (classes and properties) along with taxonomies that represent real-world uses of these  concepts for representing information regarding how (personal) data and technologies (including AI). For example, it provides concepts and taxonomies to represent:

* purposes of processing data or using technologies
* personal data categories
* processing operations on data
* technical and organisational measures for safeguarding data and processes
* legal basis used to indicate why it is legally permitted
* rights involved and how to exercise them
* risks applicable and what would be its consequences and impacts 

> The versionless base IRI https://w3id.org/dpvalways points to the latest release. The versioned base IRI for v2.1 is https://w3id.org/dpv/2.1. 

The namespace for DPV terms is `http://w3id.org/dpv#` with suggested prefix `dpv`, and serialisations are provided in RDF/XML, Turtle, JSON-LD, and N3 formats. The default serialisations are defined using RDFS/SKOS semantics, with an alternate serialisations defined using OWL2 semantics provided in a separate namespace and file.

### Extensions
These extensions provide additional concepts that extend the concepts and scope of the main DPV specification:
- [Personal Data (PD)](https://w3id.org/dpv/pd) provides a taxonomy of personal data categories;
- [Location (LOC)](https://w3id.org/dpv/loc) provides a taxonomy of location concepts based on ISO 3166 (countries, regions);
- [Technology (TECH)](https://w3id.org/dpv/tech) provides a taxonomy of technology concepts;
- [AI](https://w3id.org/dpv/ai) provides a taxonomy of AI concepts extending the TECH extension;
- [Justifications](https://w3id.org/dpv/justifications) provides concepts for representing justifications i.e. why something must be done or could not be done;
- [Risk](https://w3id.org/dpv/risk) provides concepts for risk assessment and management;

In v2.1, the Sector and Standard group of extensions was added to the DPV specifications. [Sector](https://w3id.org/dpv/sector) provides sector-specific concepts which extend concepts in other DPV extensions. Currently, the following sectors are represented:
-[SECTOR-EDUCATION](https://w3id.org/dpv/sector/education) for Education Sector
-[SECTOR-FINANCE](https://w3id.org/dpv/sector/finance) for Finance Sector
-[SECTOR-HEALTH](https://w3id.org/dpv/sector/health) for Health Sector
-[SECTOR-INFRA](https://w3id.org/dpv/sector/infra) for (Critical) Infrastructure Sector
-[SECTOR-LAW](https://w3id.org/dpv/sector/law) for Law Enforcement & Justice Sector
-[SECTOR-PUBLICSERVICES](https://w3id.org/dpv/sector/publicservices) for Public Services Sector

The Standards extensions are aimed to provide additional concepts for implementing specific standards using DPV. Currently it contains [IEEE-P7012](https://w3id.org/dpv/standards/p7012) based on [IEEE P7012 Draft Standard for Machine Readable Personal Privacy Terms](https://standards.ieee.org/ieee/7012/7192/).

### Extensions for Jurisdictions and Regulations
The LEGAL extensions provide concepts associated with specific jurisdictions and the laws, authorities, and treaties within them. The [Legal](https://w3id.org/dpv/legal) page provides an overview of these. The jurisdictions are represented by using their ISO 3166-2 codes.

- [European Union (EU)](https://w3id.org/dpv/legal/eu) with the following laws provided as modular extensions within the EU namespace:
    - [General Data Protection Regulation (GDPR)](https://w3id.org/dpv/legal/eu/gdpr)
    - [Data Governance Act (DSA)](https://w3id.org/dpv/legal/eu/dga)
    - [Artificial Intelligence Act (AI Act)](https://w3id.org/dpv/legal/eu/aiact)
    - [Network and Information Systems Directive (NIS2)](https://w3id.org/dpv/legal/eu/nis2)
    - [Draft European Health Data Space (EHDS)](https://w3id.org/dpv/legal/eu/ehds)
    - [Charter of Fundamental Rights](https://w3id.org/dpv/legal/eu/rights)
- [LEGAL-AT](https://w3id.org/dpv/legal/at) for Austria 
- [LEGAL-BE](https://w3id.org/dpv/legal/be) for Belgium 
- [LEGAL-BG](https://w3id.org/dpv/legal/bg) for Bulgaria 
- [LEGAL-CY](https://w3id.org/dpv/legal/cy) for Cyprus 
- [LEGAL-CZ](https://w3id.org/dpv/legal/cz) for Czech Republic 
- [LEGAL-DE](https://w3id.org/dpv/legal/de) for Germany 
- [LEGAL-DK](https://w3id.org/dpv/legal/dk) for Denmark 
- [LEGAL-EE](https://w3id.org/dpv/legal/ee) for Estonia 
- [LEGAL-ES](https://w3id.org/dpv/legal/es) for Spain 
- [LEGAL-FI](https://w3id.org/dpv/legal/fi) for Finland 
- [LEGAL-FR](https://w3id.org/dpv/legal/fr) for France 
- [LEGAL-GB](https://w3id.org/dpv/legal/gb) for United Kingdom of Great Britain and Northern Ireland
- [LEGAL-GR](https://w3id.org/dpv/legal/gr) for Greece 
- [LEGAL-HR](https://w3id.org/dpv/legal/hr) for Croatia 
- [LEGAL-HU](https://w3id.org/dpv/legal/hu) for Hungary 
- [LEGAL-IE](https://w3id.org/dpv/legal/ie) for Ireland 
- [LEGAL-IS](https://w3id.org/dpv/legal/is) for Iceland 
- [LEGAL-IN](https://w3id.org/dpv/legal/in) for India
- [LEGAL-IT](https://w3id.org/dpv/legal/it) for Italy 
- [LEGAL-LI](https://w3id.org/dpv/legal/li) for Liechtenstein 
- [LEGAL-LT](https://w3id.org/dpv/legal/lt) for Lithuania 
- [LEGAL-LU](https://w3id.org/dpv/legal/lu) for Luxembourg 
- [LEGAL-LV](https://w3id.org/dpv/legal/lv) for Latvia 
- [LEGAL-MT](https://w3id.org/dpv/legal/mt) for Malta 
- [LEGAL-NL](https://w3id.org/dpv/legal/nl) for Netherlands 
- [LEGAL-NO](https://w3id.org/dpv/legal/no) for Norway 
- [LEGAL-PL](https://w3id.org/dpv/legal/pl) for Poland 
- [LEGAL-PT](https://w3id.org/dpv/legal/pt) for Portugal 
- [LEGAL-RO](https://w3id.org/dpv/legal/ro) for Romania 
- [LEGAL-SE](https://w3id.org/dpv/legal/se) for Sweden 
- [LEGAL-SI](https://w3id.org/dpv/legal/si) for Slovenia 
- [LEGAL-SK](https://w3id.org/dpv/legal/sk) for Slovakia 
- [LEGAL-US](https://w3id.org/dpv/legal/usa) for United States of America (USA)

## Guides
- The [Primer](https://w3id.org/dpv/primer) is an introductory document for newcomers to understand the DPV and its concepts. A [2 Page Short Primer](https://w3id.org/dpv/primer/short) provides a succint introduction to the DPV. 
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

* For use of DPV from v2 onwards, **Cite as:** [Data Privacy Vocabulary (DPV) -- Version 2](https://arxiv.org/abs/2404.13426) by Harshvardhan J. Pandit, Beatriz Esteves, Georg P. Krog, Paul Ryan, Delaram Golpayegani, Julian Flake; 23rd International Semantic Web Conference (ISWC 2024) https://doi.org/10.1007/978-3-031-77847-6_10
* For use of DPV up to v1 and v1.1, **Cite as:** The peer-reviewed article “[Creating A Vocabulary for Data Privacy](https://link.springer.com/chapter/10.1007%2F978-3-030-33246-4_44)” presents a historical overview of the DPVCG, and describes the methodology and structure of the DPV along with describing its creation. An open-access version can be accessed [here](http://hdl.handle.net/2262/91581), [here](http://doras.dcu.ie/23801/), and [here](https://aic.ai.wu.ac.at/~polleres/publications/pand-etal-2019ODBASE.pdf).
* In addition to the above, each specifications or document may have additional references for peer-reviewed articles associated with it - these are provided at the top of each document.

## Releases

The following are final reports produced by the DPVCG i.e. formally published by the W3C:

- Primer [w3c/cg-reports link to be added]()
- DPV [w3c/cg-reports link to be added]()
- Personal Data (PD) extension [w3c/cg-reports link to be added]()
- Technology (TECH) extension [w3c/cg-reports link to be added]()
- Risk (RISK) extension [w3c/cg-reports link to be added]()
- Locations (LOC) extension [w3c/cg-reports link to be added]()
- AI Technology (AI) extension [w3c/cg-reports link to be added]()
- Justifications extension [w3c/cg-reports link to be added]()
- Legal extensions [w3c/cg-reports link to be added]()
    - Austria (AT)  [w3c/cg-reports link to be added]()
    - Belgium (BE)  [w3c/cg-reports link to be added]()
    - Bulgaria (BG)  [w3c/cg-reports link to be added]()
    - Cyprus (CY)  [w3c/cg-reports link to be added]()
    - Czech Republic (CZ)  [w3c/cg-reports link to be added]()
    - Germany (DE)  [w3c/cg-reports link to be added]()
    - Denmark (DK)  [w3c/cg-reports link to be added]()
    - Estonia (EE)  [w3c/cg-reports link to be added]()
    - Spain (ES)  [w3c/cg-reports link to be added]()
    - European Union (EU) [w3c/cg-reports link to be added]()
    - Finland (FI)  [w3c/cg-reports link to be added]()
    - France (FR)  [w3c/cg-reports link to be added]()
    - United Kingdom of Great Britain and Northern Ireland (GB)  [w3c/cg-reports link to be added]()
    - Greece (GR)  [w3c/cg-reports link to be added]()
    - Croatia (HR)  [w3c/cg-reports link to be added]()
    - Hungary (HU)  [w3c/cg-reports link to be added]()
    - Ireland (IE)  [w3c/cg-reports link to be added]()
    - Iceland (IS)  [w3c/cg-reports link to be added]()
    - India (IN)  [w3c/cg-reports link to be added]()
    - Italy (IT)  [w3c/cg-reports link to be added]()
    - Liechtenstein (LI)  [w3c/cg-reports link to be added]()
    - Lithuania (LT)  [w3c/cg-reports link to be added]()
    - Luxembourg (LU)  [w3c/cg-reports link to be added]()
    - Latvia (LV)  [w3c/cg-reports link to be added]()
    - Malta (MT)  [w3c/cg-reports link to be added]()
    - Netherlands (NL)  [w3c/cg-reports link to be added]()
    - Norway (NO)  [w3c/cg-reports link to be added]()
    - Poland (PL)  [w3c/cg-reports link to be added]()
    - Portugal (PT)  [w3c/cg-reports link to be added]()
    - Romania (RO)  [w3c/cg-reports link to be added]()
    - Sweden (SE)  [w3c/cg-reports link to be added]()
    - Slovenia (SI)  [w3c/cg-reports link to be added]()
    - Slovakia (SK)  [w3c/cg-reports link to be added]()
    - United States of America (US)  [w3c/cg-reports link to be added]()
    - United Kingdom of Great Britain and Northern Ireland (GB) [w3c/cg-reports link to be added]()
- Legal extensions modelling laws
    - EU General Data Protection Regulation (GDPR) [w3c/cg-reports link to be added]()
    - EU Data Governance Act (DSA) [w3c/cg-reports link to be added]()
    - EU Artificial Intelligence Act (AI Act) [w3c/cg-reports link to be added]()
    - EU Network and Information Systems Directive (NIS2) [w3c/cg-reports link to be added]()
    - EU Charter of Fundamental Rights [w3c/cg-reports link to be added]()
    
## Funding Acknowledgements

The DPVCG was established as part of the [SPECIAL H2020 Project](https://specialprivacy.ercim.eu/), which received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 731601 from 2017 to 2019.

Harshvardhan J. Pandit was funded to work as the chair of DPVCG from 2020 to 2022 by the [Irish Research Council\'s](https://research.ie/) Government of Ireland Postdoctoral Fellowship Grant#GOIPD/2020/790, and through the [ADAPT SFI Centre](https://www.adaptcentre.ie/) for Digital Media Technology is funded by Science Foundation Ireland through the SFI Research Centres Programme and is co-funded under the European Regional Development Fund (ERDF) through Grant#13/RC/2106 (2018 to 2020) and Grant#13/RC/2106_P2 (2021 onwards).

Further funding acknowledgements for individual author are provided within relevant specifications.
