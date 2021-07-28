#!/usr/bin/env python3
#author: Harshvardhan J. Pandit
#id: coolharsh55

"""
RDF ORM

Create Python objects (classes with properties) from data in a
RDF graph which has a schema (RDFS and OWL2).

:Mechanism:
For every 'subject' in the graph, retrieve all triples
where it is the subject (i.e. <?s ?p ?o>).
If ?o is a literal then store its value as native python datatype.
Otherwise, ?o is an IRI and it may be present in the graph or 
externally resolvable. If ?o is in the graph, change the value to
a reference to the object corresponding to that IRI.
Otherwise, store the IRI as an external reference.

:Naming:
To enable any arbitrary properties to be accessed dynamically,
the prefixes are used to label the property names.
For example, rdf:type --> rdf_type
Default prefixes known: RDF, RDFS, OWL, XSD, Schema, DCT, Time
Additional prefixes can be added using global method/list.

:Classes and Instances:
If something is a class, then it is subclassed from BaseClass.
If something is an instance, then it is instantiated from its Class.
Punning is a problem, since it is not handled currently.
"""

from rdflib import Graph
from rdflib import Namespace
from rdflib import RDF, RDFS, OWL
from rdflib.term import Literal, URIRef, BNode
from rdflib.collection import Collection
from rdflib.namespace import NamespaceManager

import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug


class RDFS_Resource(object):
    """Base class for everything.
    Since everything is an RDFS_Resource, everything is an instance
    of this class, with other information being properties.

    Generation of object from data will automatically populate it
    with rdf:type if present in the graph.
    Similarly, other properties will be populated as well.
    The name of properties is prefix_label e.g. rdf_type.

    Covenience queries, such as getting all instances of a class,
    are handled through explicitly provided methods in the module
    as opposed to a class method. This is because having a class
    method means keeping a local list and keeping it udpated.
    And then there is the additional constraint of named graphs.
    """

    def __init__(self, *args, **kwargs):
        self.iri = None
        self.metadata = { }

    def __getattr__(self, name):
        if name in self.metadata:
            return self.metadata[name]
        else:
            raise AttributeError

    def __str__(self):
        """String representation of object"""

        if 'schema_name' in self.metadata:
            return self.schema_name
        elif 'dct_title' in self.metadata:
            return self.dct_title
        elif 'rdfs_label' in self.metadata:
            return self.rdfs_label
        elif self.iri is not None:
            return self.iri
        else:
            return 'Blank Node'

    def __repr__(self):
        """representation of object"""

        if 'schema_name' in self.metadata:
            return f'entity: {self.schema_name}'
        elif 'dct_title' in self.metadata:
            return f'entity: {self.dct_title}'
        elif 'rdfs_label' in self.metadata:
            return f'entity: {self.rdfs_label}'
        elif self.iri.startswith('https://schema.org/'):
            return f'schema:{self.iri.rpartition("/")[2]}'
        elif self.iri is not None:
            return f'entity: {self.iri}'
        else:
            return 'Blank Node'

    def __lt__(self, other):
        if type(other) is not RDFS_Resource:
            return self.iri < other
        return self.iri < other.iri

    def __gt__(self, other):
        if type(other) is not RDFS_Resource:
            return self.iri > other
        return self.iri > other.iri        


class DataGraph(object):
    """Graph of instances created from data.
    Provides methods to load triples from a graph, query them
    for criteria such as all classes, instance of specific class.
    Stores a list of instances generated.
    All instances are of rdfs:Resource."""

    def __init__(self, *args, **kwargs):
        # list of rdfs:Resource objects
        self.objects = { }
        self.graph = None

    def _get_iri_from_prefix(self, name):
        prefix, name = name.split('_')
        prefixes = list(self.graph.namespace_manager.namespaces())
        prefixes = [x[1] for x in prefixes if x[0] == prefix]
        if not prefixes:
            return None
        prefix = prefixes[0]
        return str(prefix) + name

    def load(self, graph=None):
        """takes a rdflib graph and creates objects from it"""

        if graph is None:
            if self.graph is None:
                raise Exception('graph is not provided')
            graph = self.graph
        else:
            # replace existing graph
            self.graph = graph
            self.objects = {}

        # instantiate objects from class data
        # DEBUG('loading objects from graph')

        collections = []

        # iterate triples in graph
        for s, p, o in graph:
            iri = str(s)
            # DEBUG(f'{iri}')
            # if the object has been encountered before, retrieve it
            # otherwise create new object for given iri
            if iri.startswith('f'):
                # do not handle collections as subjects
                continue
            if iri in self.objects:
                obj = self.objects[iri]
            else:
                obj = RDFS_Resource()
                obj.iri = iri
                # DEBUG(f'created {obj.iri}')
                self.objects[obj.iri] = obj

            if type(o) == URIRef or type(o) == BNode:
                o_str = str(o)
                if o_str in self.objects:
                    o = self.objects[o_str]
                else:
                    if o_str.startswith('f'):
                        # rdf collection
                        temp_o = list(Collection(graph, o))
                        o = list()
                        # DEBUG(f'collection {temp_o}')
                        for o_s in temp_o:
                            # create objects for each item in collection
                            o_s_str = str(o_s)
                            if o_s_str in self.objects:
                                o_s = self.objects[o_s_str]
                            elif type(o_s) != Literal:
                                o_s = RDFS_Resource()
                                o_s.iri = o_s_str
                                # DEBUG(f'created {o_s.iri}')
                                self.objects[o_s_str] = o_s
                            else:
                                o_s = o_str
                            o.append(o_s)
                    else:
                        o = RDFS_Resource()
                        o.iri = o_str
                        # DEBUG(f'created {o.iri}')
                        self.objects[o_str] = o
                    # self.objects[o_str] = RDFS_Resource()
                    # self.objects[o_str].iri = o_str
            else:
                o = str(o)
             
            p = p.n3(graph.namespace_manager).replace(':', '_').replace('-', '_')
            if p in obj.metadata:
                p_in_m = obj.metadata[p]
                if type(p_in_m) is not list:
                    obj.metadata[p] = [p_in_m]
                obj.metadata[p].append(o)
            else:
                obj.metadata[p] = o
            # DEBUG(f'handled triple: {iri} {p} {o}')
            # DEBUG(f'type of s: {type(iri)}')
            # DEBUG(f'data in p: {obj.metadata[p]}')

        # for iri, obj in self.objects.items():
        #     DEBUG(f'{iri}')
        #     for k, v in obj.metadata.items():
        #         DEBUG(f'\t{k}: {v}')
                
    def classes(self):
        """returns list of classes in current graph"""

        # filter objects for classes
        # return list of classes

    def instances(self):
        """returns list of instances in current graph"""

        # filter objects for instances

    def get_instances_of(self, classname):
        """returns list of instances of given class"""

        if type(classname) is RDFS_Resource:
            # if classname is a RDFS_Resource object, just get its iri
            classname = classname.iri
        elif type(classname) is str:
            # otherwise check if it is a string
            # if yes, then check if it already exists in list of objects
            # if not, it could be prefixed key:value syntax
            # try to derive iri from prefix
            # if all fails, return None
            if classname not in self.objects:
                if '_' not in classname:
                    # prefix_label syntax
                    # DEBUG('classname is not prefixed')
                    return None
                # classname is prefixed
                classname = self._get_iri_from_prefix(classname)
                if classname is None:
                    # DEBUG('iri could not be generated from prefix')
                    return None
        else:
            # DEBUG('classname is neither rdfs object nor string')
            return None
        if classname not in self.objects:
            # DEBUG('classname could not be found in objects')
            return None

        # at this point, classname is definitely in self.objects
        instances = []
        class_obj = self.objects[classname]
        if class_obj is None:
            return None
        # go over each object, check if it has a rdf_type whose value
        # matches the object ; if yes, collect it
        for obj in self.objects.values():
            if not hasattr(obj, 'rdf_type'):
                continue
            parents = obj.rdf_type
            if type(parents) is list:
                if class_obj in parents:
                    instances.append(obj)
            elif type(parents) is RDFS_Resource:
                if parents is class_obj:
                    instances.append(obj)

        return instances

    def get_entity(self, name):
        if name in self.objects:
            return self.objects[name]

        if '_' in name:
            # name is prefixed
            name = self._get_iri_from_prefix(name)
            if name is None:
                return None
            if name in self.objects:
                return self.objects[name]

        return None

    def resolve_entities_to_objects(self, items):
        return_list = []
        for item in items:
            entity = None
            if type(item) is str:
                entity = self.get_entity(item)
            elif type(item) is URIRef or type(item) is BNode:
                entity = self.get_entity(str(item))
            elif type(item) is Literal:
                entity = item.toPython()
            if entity is None:
                entity = item
            return_list.append(entity)
        return return_list

    def subclasses(self, classname):
        """returns subclasses of given term"""

        if type(classname) is RDFS_Resource:
            # if classname is a RDFS_Resource object, just get its iri
            classname = classname.iri
        elif type(classname) is str:
            # otherwise check if it is a string
            # if yes, then check if it already exists in list of objects
            # if not, it could be prefixed key:value syntax
            # try to derive iri from prefix
            # if all fails, return None
            if classname not in self.objects:
                if '_' not in classname:
                    # prefix_label syntax
                    # DEBUG('classname is not prefixed')
                    return None
                # classname is prefixed
                classname = self._get_iri_from_prefix(classname)
                if classname is None:
                    # DEBUG('iri could not be generated from prefix')
                    return None
        else:
            # DEBUG('classname is neither rdfs object nor string')
            return None
        if classname not in self.objects:
            # DEBUG('classname could not be found in objects')
            return None

        # at this point, classname is definitely in self.objects
        children = []
        class_obj = self.objects[classname]
        if class_obj is None:
            # DEBUG('classname could not be found in objects')
            return None
        # go over each object, check if it has a rdf_type whose value
        # matches the object ; if yes, collect it
        # DEBUG(f'class: {class_obj}')
        for obj in self.objects.values():
            # DEBUG(f'term: {obj} keys: {obj.metadata.keys()}')
            if not 'rdfs_subClassOf' in obj.metadata:
                continue
            parents = obj.rdfs_subClassOf
            # DEBUG(f'term: {obj} parents: {parents}')
            if type(parents) is list:
                if class_obj in parents:
                    children.append(obj)
            elif type(parents) is RDFS_Resource:
                # DEBUG(f'term: {obj} parents: {parents} class: {class_obj} equal: {class_obj == parents}')
                if parents is class_obj:
                    children.append(obj)

        return children
