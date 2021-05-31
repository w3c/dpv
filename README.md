# GDPR terms for Data Privacy Vocabulary (DPV-GDPR)

<https://w3.org/ns/dpv-gdpr>

>  cite as: Pandit H.J. et al. (2019) Creating a Vocabulary for Data Privacy. In:  Panetto H., Debruyne C., Hepp M., Lewis D., Ardagna C., Meersman R.  (eds) On the Move to Meaningful Internet Systems: OTM 2019 Conferences.  OTM 2019. Lecture Notes in Computer Science, vol 11877. Springer, Cham.  <https://doi.org/10.1007/978-3-030-33246-4_44>

## Abstract / Summary

The Data Privacy Vocabulary provides terms (classes and properties) to annotate and categorize instances of legally compliant personal data handling according to the EU General Data Protection Regulation. This extension provides terms, such as legal basis, defined within the GDPR for use with DPV. 

The namespace for DPV-GDPR terms is `http://www.w3.org/ns/dpv-gdpr#`

The suggested prefix for the DPV-GDPR namespace is `dpv-gdpr`

The Data Privacy Vocabulary and DPV-GDPR are outcomes of the activities of the [Data Privacy Vocabularies and Controls Community Group (DPVCG)](https://www.w3.org/community/dpvcg/) 

## Contribution / Participation

The DPVCG is the primary forum for contributions and participations regarding the DPV and DPV-GDPR. As such, all decisions and resolutions will be conducted through the group's meetings and call. Membership in DPVCG is not necessary to contribute to DPV or DPV-GDPR, but is recommended for participating in the group's decision making process. Contributions and questions can be sent to the group's [public mailing list](https://lists.w3.org/Archives/Public/public-dpvcg/) or expressed as [GitHub issues](https://github.com/dpvcg/dpv-gdpr/issues). 

### Suggesting new terms

To suggest a new term, we request following information:

- *term* 
- *description of the term*
- whether it should be a *class* or *a property*
- relation to existing term(s) in DPV e.g. through sub-classes
- justification or relevance of why this term should be added (where not obvious)

### Raising issues

Before submitting an issue, please see the whether the issue has been addressed on [GitHub](https://github.com/dpvcg/dpv-gdpr/issues) or [W3C trackers](https://www.w3.org/community/dpvcg/track/). If not, please raise the issue via the group's [public mailing list](https://lists.w3.org/Archives/Public/public-dpvcg/) or expressed as [GitHub issues](https://github.com/dpvcg/dpv-gdpr/issues). 

Fixes, corrections to the terms are considered as issues and can be submitted similarly. For minor changes, we may prefer to incorporate them directly rather than through pull requests and patches. For larger issues, please check with the group before submitting a pull-request to ensure its appropriate and efficient incorporation.

## Development Guide

> please refrain from making changes by-hand or manually

The development and maintainence of DPV and DPV-GDPR takes place primarily through a shared spreadsheet. The terms and their annotated metadata are declared in the spreadsheet, and used as input to generate the RDF files and HTML documentation through the [dpv-documentation](https://github.com/coolharsh55/dpv-documentation) tooling. The `dpv-documentation` repository is a collection of Python scripts to assist in the automation of downloading the spreadsheet as CSV files, generating RDF files, validating them for correctness, and producing the HTML documentation.

Therefore, whenever adding a new term or changing existing ones, the following steps are recommended to update the DPV-GDPR vocabulary and documentation:

1. Make changes appropriately in the shared spreadsheet. The links to this are available to the DPVCG members.
2. Use the [dpv-documentation](https://github.com/coolharsh55/dpv-documentation) tooling to download the spreadsheet, generate RDF, test it, generate HTML output. 
3. Manually inspect whether the changes have been made. Tools, scripts, and software in general can propogate errors silently. 
4. The variables and parameters in  [dpv-documentation](https://github.com/coolharsh55/dpv-documentation) tooling can be used to define the path where files are exported to can be set to the `dpv` repository to make changes in this directory. For e.g. `EXPORT_DPV_GDPR_HTML_PATH = ~/code/dpvcg/dpv-gdpr` will generate the HTML documentation in the `dpv-gdpr` directory. 
5. Submit a pull-request for merging with the repository.

## Getting help and assistance

If you're unsure about something, or would like clarifications, or suggestions - please drop us a line or open an issue. We would be happy to help.