# Style Guide

## Terms

1.  Term
    1.  Should be a continuos string of alphanumeric characters without spaces or special characters.
    2.  Is intended to be both machine and human readable.
    3.  Should be in English (UK) unless representing a specific concept where no alternative is possible or suitable.
    4.  For classes, should be in *PascalCase* (leading capital-case).
    5.  For properties, should be in *camel_Case* (leading small-case with underscore separation), with a suitable prefix expressing application or association, e.g. hasX or isY or forZ
    6.  Use of 'and', 'or', or similar terms in labels is omitted from corresponding Term, e.g. 'X and Y' label has term as 'XY'
    7.  Status should be one of: accepted, modified, proposed, deprecated

2.  Label
    1.  Should be a set of strings separated by spaces or special characters as appropriate.
    2.  Is intended to be human readable.
    3.  May be in different languages, with corresponding annotation describing the language it is in. By default, labels are in English (UK).
    4.  At least one label must be provided.

3.  Description
    1.  Intended to be human readable.
    2.  Should start with a capital letter.
    3.  Must not end in punctuation (e.g. full-stop).
    4.  May be in different languages, with annotations describing the language it is in. By default, *description* is in English (UK).
    5.  May include illustrative example of concept (e.g.concept season has example summer).
    6.  At least one description must be provided.

4.  Comments
    1.  Comments should be used for providing additional information, such as clarificatinos, examples, or guidance.
    2.  Comments should not repeat the same information as the description.

5.  Status
    1.  Each Term MUST have a Status
    2.  Statuses valid for inclusion in outputs are: accepted, modified, changed
    3.  Statuses not included in outputs but used for documenting are: proposed, deprecated, sunset
