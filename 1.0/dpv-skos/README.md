# RDFS+SKOS Serialisation of Data Privacy Vocabulary (DPVS)

[https://w3id.org/dpv/dpv-skos](https://w3id.org/dpv/dpv-skos)

>  cite as: Pandit H.J. et al. (2019) Creating a Vocabulary for Data Privacy. In:  Panetto H., Debruyne C., Hepp M., Lewis D., Ardagna C., Meersman R.  (eds) On the Move to Meaningful Internet Systems: OTM 2019 Conferences.  OTM 2019. Lecture Notes in Computer Science, vol 11877. Springer, Cham.  https://doi.org/10.1007/978-3-030-33246-4_44

This is a serialisation of the DPV using RDFS and SKOS semantics. RDFS is used to declare classes and properties, and SKOS is used to declare 'hierarchies' between instances of these classes so as to permit their usage in an ad-hoc fashion.

The namespace for DPVS terms is `http://w3id.org/dpv/dpv-skos#` with suggested prefix `dpvs`. 

Extensions of DPVS are also provided using the same semantics in sub-folders with the following suggested previxes and namespaces:

- DPV-GDPR: `dpvs-gdpr` for `http://w3id.org/dpv/dpv-skos/dpv-gdpr#`
- DPV-PD: `dpvs-pd` for `http://w3id.org/dpv/dpv-skos/dpv-pd#`
- DPV-LEGAL: `dpvs-legal` for `http://w3id.org/dpv/dpv-skos/dpv-gdpr#`
- DPV-TECH: `dpvs-tech` for `http://w3id.org/dpv/dpv-skos/dpv-tech#`

The Data Privacy Vocabulary is an outcome of the activities of the [Data Privacy Vocabularies and Controls Community Group (DPVCG)](https://www.w3.org/community/dpvcg/) 

