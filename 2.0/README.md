# DPV Version 2.0

> The scope of DPV has been expanded to include non-personal data and AI technologies - though the focus of the group remains on privacy and data protection. The structure of the repo has also been changed to incorporate multiple jurisdictions and regulations, and their names have been changed e.g. `dpv-gdpr` is `legal/eu/gdpr`. The namespace and IRI have been chnaged to reflect versions e.g. https://w3id.org/dpv/2.0 with the versionless IRI e.g. https://w3id.org/dpv always pointing to the latest version. Read more in [v2 changelog](https://w3id.org/dpv/2.0/changelog). 

> The draft article [Data Privacy Vocabulary (DPV) -- Version 2](https://arxiv.org/abs/2404.13426) by Pandit et al. (2024) describes DPV v2 in terms of its contents, methodology, current adoptions and uses, and future potential. It also describes the relevance and role of DPV in acting as a common vocabulary to support various regulatory (e.g. EU's DGA and AI Act) and community initiatives (e.g. Solid) emerging across the globe

The mission of the W3C Data Privacy Vocabularies and Controls CG (DPVCG) is to develop a taxonomy of privacy and data protection related terms, which include in particular terms from the new European General Data Protection Regulation (GDPR), such as a taxonomy of personal data as well as a classification of purposes (i.e., purposes for data collection), and events of disclosures, consent, and processing such personal data.

> Newcomers to the DPV are recommended to start with the [Primer](https://w3id.org/dpv/primer) to familiarise themselves with the concepts, semantics, and usefulness of the DPV.

License: All work produced by DPVCG and provided through this repo or elsewhere is provided by contributors under the [W3C Document License](https://www.w3.org/copyright/software-license-2023/). A copy of the license is provided in the [LICENSE.md](./LICENSE.md) file.

[Guidelines for contributing new concepts, identified bugs and issues, and suggestions](https://github.com/w3c/dpv/wiki/contributing)

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

## Acknowledgements and Citation

For use of DPV from v2 onwards, **Cite as:** [Data Privacy Vocabulary (DPV) -- Version 2](https://arxiv.org/abs/2404.13426) by Harshvardhan J. Pandit, Beatriz Esteves, Georg P. Krog, Paul Ryan, Delaram Golpayegani, Julian Flake https://arxiv.org/abs/2404.13426 (2024)

### Final Reports

The following are final reports i.e. formally published by the W3C: TBA

## Folder Structure

- `dpv` contains the DPV specification
- `pd` contains the personal data extension
- `tech` contains the technical concepts extension
- `risk` contains the risk assessment and management extension
- `loc` contains the location extension
- `justifications` contains the justifications extension
- `legal` contains legal extensions with further subfolders
    - the `legal` folder itself contains an aggregated collection of laws, authorities, and other relevant concepts from existing extensions
    - folders with names based on ISO 3166-2 are provided which represent a specific jurisdiction - currently these are: `ie` - Ireland, `in` - India, `de` - Germany, `eu` - European Union, `gb` - United Kingdom (UK), `us` - United States of America
    - within these folders, the respective laws of that jurisdiction are defined as subfolders, e.g. `eu` has `gdpr`, `dga`, `nis2`, and `aiact`
- `search.html` contains an index of all concepts within DPV and extensions, and provides a visual way to navigate them and search/filter them based on string-matching