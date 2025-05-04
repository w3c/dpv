#= Term Statuses =#

VOCAB_TERM_ACCEPT = (
    'accepted', 
    'changed', 
    'modified', 
    'sunset'
)

VOCAB_TERM_REJECT = (
    'deprecated',
    'removed'
)

VOCAB_TERM_PROPOSED = (
    'proposed',
)

#= Do not do anything with/about these terms =#
IGNORED_TERMS = (
    'rdf:type', 
    'rdfs:Class', 
    'rdf:Property', 
    'skos:Concept'
)