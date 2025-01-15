# Mappings between DPV and other Vocabularies

These folders contain mappings (or will contain mappings) between DPV concepts
and other vocabularies. For the moment, the following vocabularies have 
been identified for mappings (see https://github.com/w3c/dpv/issues/31):

- foaf - annotations for agents / entities
- vCard - annotations for agents / entities
- DCMI Metadata Terms - relations for commonly utilised information e.g. timestamps, publication provenance, identifiers
- ODRL - legal/deontic terms e.g. parties (entities in DPV) and rules regarding permissions - aligned with DPV's taxonomy e.g. personal data, purpose, legal basis
- SEMIC - EU SEMIC vocabularies such as DCAT-AP, Core, ADMS used for open data
- PROV - activities, aretefacts, agents/entities, and expressing plans/provenance
- gist - upper ontology for business processes and concepts

The mappings process is a simple process that will utilise SKOS to express
whether the two concepts are exact, or have a broader/narrower relationship,
or are related with each other. The goal of this exercise is to establish
the overlap/alignment of DPV with existing (best practice and standardised)
vocabularies, and therefore we are starting with a simple form of mapping as
opposed to a rigorous exhaustive expression of exactly how two concepts can
be made equivalent (e.g. using OWL2 axioms).

Each folder will have a RDF file containing the mapping, and a corresponding
HTML documentation page showing the mapping and providing commentary on it.
Mappings are not intended to act as guides for the use of DPV or other 
vocabularies alongside DPV - for these, the guides folder should be looked at.
