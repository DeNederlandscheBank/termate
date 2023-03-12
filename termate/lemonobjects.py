# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict, deque
from typing import Union
from rdflib import Graph
from rdflib.term import URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD, Namespace
from .vocab import ONTOLEX, TBX, LEXINFO, DECOMP
import iribaker

# <http://lemon-model.net/lemon>
#     a owl:Ontology ;
#     rdfs:comment "Lemon: The lexicon model for ontologies is designed to allow  for descriptions of lexical information regarding ontological elements and other RDF resources. Lemon covers mapping of lexical decomposition, phrase structure, syntax,  variation, morphology, and lexicon-ontology mapping."@en ;
#     rdfs:label "lemon"@en ;
#     rdfs:seeAlso <http://www.monnet-project.eu/lemon> .


class LemonElement(object):
    pass


class LexicalSense(object):
    pass


class LexicalEntry(object):
    pass


class LemonBase(object):
    """
    A Lemon Base

    :param uri: the uri of the object

    """

    def __init__(self, uri: Union[URIRef, str] = None):
        self.set_uri(uri)

    def __eq__(self, other):
        return self._uri == other._uri

    @property
    def uri(self):
        """
        Returns the uri of the object
        """
        if self._uri is not None:
            return self._uri
        else:
            return None

    def set_uri(self, uri: Union[URIRef, str] = None):
        """
        Sets the uri of the object. If the uri is a string then it is converted to an iri.
        """
        if isinstance(uri, str):
            self._uri = URIRef(iribaker.to_iri(uri))
        else:
            self._uri = uri


class LemonElement(object):
    """

    :param Denotes a lexical property of a lexical entry, form, component or MWE node. For the lexical entry this is assumed to be static properties e.g., part of speech and gender and for the others this is assumed to be specific properties e.g., case, number

    """

    def __init__(self, 
                 uri: URIRef = None, 
                 property: URIRef = None):
        self.set_uri(uri)
        self.set_property(property)

    def set_uri(self, uri: URIRef = None):
        self._uri = uri

    def set_property(self, property: URIRef = None):
        self._property = property

    @property
    def uri(self):
        return self._uri

    @property
    def property(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Lexical property"@en, "Lexikaal predikaat"@nl, "Lexikalische Prädikat"@de, "Propiedad léxica"@es, "Propiété lexicale"@fr ;
        return self._property

    def triples(self):
        pass


# class Argument(LemonElement, PhraseElement):
#     """
#     A slot representing a gap that must be filled in realising a lexical entry in a given projection.

#     :param marker: Denotes the marker of a semantic argument. This should generally either be a semantic property i.e., case or another lexical entry e.g., a preposition or particle

#     :param optional: Denotes that the syntactic argument is optional (may be omitted)

#     """
#     # rdfs:label "Actant"@fr, "Argument"@de, "Argument"@en, "Argument"@nl, "Argumento"@es ;
#     # owl:disjointWith :Component, :Form, :Frame, :LexicalEntry, :LexicalSense, :Lexicon, :Node, :PropertyValue, :SenseDefinition, :SynRoleMarker, :UsageExample .

#     def __init__(
#         self,
#         marker: SynRoleMarker = None,
#         optional: Bool = None
#     ):
#         self.set_marker(marker)
#         self.set_optional(optional)
#         LemonElement.__init__()
#         PhraseElement.__init__()

#     def set_marker(self, marker: SynRoleMarker = None):
#         self._marker = marker

#     def set_optional(self, optional: Bool = None):
#         self._optional = optional

#     @property
#     def marker(self):
#         # a rdf:Property, owl:ObjectProperty ;
#         # rdfs:label "Marcador"@es, "Marker"@de, "Marker"@en, "Marqueur"@fr, "Merker"@nl ;
#         return self._marker

#     @property
#     def optional(self):
#         # a rdf:Property, owl:DatatypeProperty ;
#         # rdfs:label "Opcional"@es, "Optional"@de, "Optional"@en, "Optionele"@nl, "Optionnel"@fr ;
#         return self._optional


class PhraseElement(LemonBase, LemonElement):
    """
    A terminal node in a phrase structure graph, i.e., a realisable, lexical element.
    """

    # rdfs:label "Elemento del sintagma"@es, "Elément du syntagme"@fr, "Phrase element"@en, "Phrase-Element"@de, "Zinselement"@nl ;
    def __init__(
        self,
    ):
        self.set_uri(uri=uri)


class Component(PhraseElement, LemonBase, LemonElement):
    """
    A constituent element of a lexical entry. This may be a word in a multi-word lexical
    element or a constituent of a compound word

    param: element: Denotes the lexical entry represented by the component

    """

    # rdfs:label "Bestanddeel"@nl, "Component"@en, "Componente"@es, "Composant"@fr, "Komponente"@de ;
    # rdfs:subClassOf :LemonElement, :PhraseElement, [
    #     a owl:Restriction ;
    #     owl:maxCardinality "1"^^xsd:nonNegativeInteger ;
    #     owl:onProperty :element
    # ] ;
    # owl:disjointWith :Form, :Frame, :LexicalEntry, :LexicalSense, :Lexicon, :Node, :PropertyValue, :SenseDefinition, :SynRoleMarker, :UsageExample .

    def __init__(
        self,
        uri: URIRef = None,
        correspondsTo: list[LexicalEntry] = None,
    ):
        self.set_uri(uri=uri)
        # self.set_PhraseElement(PhraseElement=PhraseElement)
        self.set_correspondsTo(correspondsTo=correspondsTo)

    def string_rep(self, level: int = 0):
        indent = "   " * level
        s = f"(ontolex:Component) uri = {self.uri.n3()}\n"
        if self.correspondsTo is not None:
            for line in self.correspondsTo:
                s += indent + f"  correspondsTo : {line.n3()}\n"
        return s

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.string_rep()

    def set_correspondsTo(self, correspondsTo: list[LexicalEntry] = None):
        self._correspondsTo = correspondsTo

    def add_correspondsTo(self, correspondsTo: LexicalEntry = None):
        if self._correspondsTo is None:
            self._correspondsTo = [correspondsTo]
        else:
            self._correspondsTo.append(correspondsTo)

    @property
    def correspondsTo(self):
        # a rdf:Property, owl:FunctionalProperty, owl:ObjectProperty ;
        # rdfs:label "Element"@de, "Element"@en, "Element"@nl, "Elemento"@es, "Elément"@fr ;
        return self._correspondsTo

    def triples(self):
        yield (self.uri, RDF.type, DECOMP.Component)
        if self.correspondsTo is not None:
            for line in self.correspondsTo:
                yield (self.uri, DECOMP.correspondsTo, line.uri)

    def load(self, graph: Graph = None, uri: URIRef = None):
        self.set_uri(uri)
        self.set_correspondsTo(
            [o for _, _, o in graph.triples((uri, DECOMP.correspondsTo, None))]
        )
        return self


class ComponentList(LemonBase):
    """
    A node within a list of components. This should generally be a blank node, see rdf:List.
    """

    # rdfs:subClassOf rdf:List, [
    #     a owl:Restriction ;
    #     owl:cardinality "1"^^xsd:nonNegativeInteger ;
    #     owl:onProperty rdf:first
    # ], [
    #     a owl:Restriction ;
    #     owl:allValuesFrom :Component ;
    #     owl:onProperty rdf:first
    # ], [
    #     a owl:Restriction ;
    #     owl:cardinality "1"^^xsd:nonNegativeInteger ;
    #     owl:onProperty rdf:rest
    # ], [
    #     a owl:Restriction ;
    #     owl:allValuesFrom [
    #         a rdfs:Class ;
    #         owl:unionOf (:ComponentList
    #             [
    #                 a rdfs:Class ;
    #                 owl:oneOf (rdf:nil
    #                 )
    #             ]
    #         )
    #     ] ;
    #     owl:onProperty rdf:rest
    # ] .

    def __init__(self, uri: URIRef = None, components: list = None):
        self.set_uri(uri=uri)
        self.set_components(components)

    def string_rep(self, level: int = 0):
        indent = "   " * level
        s = f"(ontolex:ComponentList) uri = {self.uri.n3()}\n"
        if self.components is not None:
            for component in self.components:
                s += indent + f"  component : {component.uri.n3()}\n"
        return s

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.string_rep()

    def set_components(self, components: list = None):
        self._components = components

    def add_component(self, component=None):
        if self._components is None:
            self._components = [component]
        else:
            self._components.append(component)

    @property
    def components(self):
        return self._components

    def triples(self):
        comp_uri = BNode()
        yield (self.uri, RDF.List, comp_uri)
        for comp_idx, comp in enumerate(self.components):
            yield (comp_uri, RDF.first, comp.uri)
            if comp_idx < len(self.components) - 1:
                next_comp = BNode()
                yield (comp_uri, RDF.rest, next_comp)
                comp_uri = next_comp
            else:
                yield (comp_uri, RDF.rest, RDF.nil)


class Form(LemonBase, LemonElement):
    """
    A given written or spoken realisation of a lexical entry.

    :param formVariant:

    :param representation: A realisation of a given form

    :param writtenRep: Gives the written representation of a given form

    """

    # rdfs:label "Form"@de, "Form"@en, "Forma"@es, "Forme"@fr, "Vorm"@nl ;
    # rdfs:subClassOf :LemonElement, [
    #     a owl:Restriction ;
    #     owl:minCardinality "1"^^xsd:nonNegativeInteger ;
    #     owl:onProperty :representation
    # ] ;
    # owl:disjointWith :Frame, :LexicalEntry, :LexicalSense, :Lexicon, :Node, :PropertyValue, :SenseDefinition, :SynRoleMarker, :UsageExample .

    def __init__(
        self,
        uri: URIRef = None,
        formVariant: str = None,
        representations: list[str] = None,
        writtenReps: list[str] = None,
    ):
        self.set_uri(uri=uri)
        self.set_formVariant(formVariant)
        self.set_representations(representations)
        self.set_writtenReps(writtenReps)

    def string_rep(self, level: int = 0):
        indent = "   " * level
        s = f"(ontolex:Form) uri = {self.uri.n3()}\n"
        if self.formVariant is not None:
            s += indent + f"  formVariant : {self.formVariant}\n"
        if self.representations is not None:
            for line in self.representations:
                s += indent + f"  representation : {line}\n"
        if self.writtenReps is not None:
            for line in self.writtenReps:
                s += indent + f"  writtenRep : {line}\n"
        return s

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.string_rep()

    def set_formVariant(self, formVariant: str = None):
        self._formVariant = formVariant

    def set_representations(self, representations: list[str] = None):
        self._representations = representations

    def set_writtenReps(self, writtenReps: list[str] = None):
        self._writtenReps = writtenReps

    def add_representation(self, representation: str = None):
        if self._representations is None:
            self._representations = [representation]
        else:
            self._representations.append(representation)

    def add_writtenRep(self, writtenRep=None):
        if self._writtenReps is None:
            self._writtenReps = [writtenRep]
        else:
            self._writtenReps.append(writtenRep)

    @property
    def formVariant(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Form variant"@en, "Form-Variante"@de, "Variante de la forma"@es, "Variante de la forme"@fr, "Vorm variant"@nl ;
        return self._formVariant

    @property
    def representations(self):
        # a rdf:Property, owl:DatatypeProperty ;
        # rdfs:label "Darstellung"@de, "Representación"@es, "Representation"@en, "Représentation"@fr, "Voorstelling"@nl ;
        return self._representations

    @property
    def writtenReps(self):
        # a rdf:Property, owl:DatatypeProperty ;
        # rdfs:label "Representación escrita"@es, "Représentation écrite"@fr, "Schriftelijke voorstelling"@nl, "Schriftliche Darstellung"@de, "Written representation"@en ;
        # rdfs:subPropertyOf :representation .
        return self._writtenReps

    def triples(self):
        yield (
            self.uri,
            ONTOLEX[self._formVariant],
            URIRef(self.uri + "#" + self._formVariant),
        )
        yield (URIRef(self.uri + "#" + self._formVariant), RDF.type, ONTOLEX.Form)
        if self.writtenReps is not None:
            for line in self.writtenReps:
                yield (
                    URIRef(self.uri + "#" + self._formVariant),
                    ONTOLEX.writtenRep,
                    Literal(line),
                )
        if self.representations is not None:
            for line in self.representations:
                yield (
                    URIRef(self.uri + "#" + self._formVariant),
                    ONTOLEX.representation,
                    Literal(line),
                )

    def load(self, graph: Graph = None, uri: URIRef = None):
        self.set_uri(uri)
        self.set_formVariant(uri.split("#")[-1])
        self.set_writtenReps(
            [o for _, _, o in graph.triples((uri, ONTOLEX.writtenRep, None))]
        )
        self.set_representations(
            [o for _, _, o in graph.triples((uri, ONTOLEX.representation, None))]
        )
        return self


# class Frame(LemonElement):
#     """
#     A stereotypical example of the usage of a given lexical entry.
#     The most common example of projections are subcategorization frames which
#     describe the slots taken by the arguments of a verb.

#     :param synArg: Indicates a slot in a syntactic frame

#     """
#     # rdfs:label "Cadre"@fr, "Frame"@en, "Marco"@es, "Raam"@nl, "Rahmen"@de ;
#     # owl:disjointWith :LexicalEntry, :LexicalSense, :Lexicon, :Node, :PropertyValue, :SenseDefinition, :SynRoleMarker, :UsageExample .

#     def __init__(
#        self,
#        synArg: Argument = None
#     ):
#         self.set_synArg(synArg)
#         LemonElement.__init__()

#     def set_synArg(synArg: Argument = None):
#         self._synArg = synArg

#     @property
#     def synArg(self):
#         # a rdf:Property, owl:ObjectProperty ;
#         # rdfs:label "Actant syntaxique"@fr, "Argumento sintáctico"@es, "Syntactic argument"@en, "Syntactisch argument"@nl, "Syntactische Argument"@de ;
#         return self._synArg


class HasLanguage(LemonBase):
    """
    Structural element for all elements that can be tagged with a language.
    """

    def __init__(self, uri: URIRef = None, language: str = None):
        self.set_uri(uri=uri)
        self.set_language(language)

    def set_language(self, language: str = None):
        self._language = language

    @property
    def language(self):
        # a rdf:Property, owl:DatatypeProperty ;
        # rdfs:label "Language"@en, "Langue"@fr, "Lengua"@es, "Sprache"@de, "Taal"@nl ;
        return self._language

    def triples(self):
        yield (self.uri, ONTOLEX.language, Literal(self._language))

    def load(self, graph: Graph = None, uri: URIRef = None):
        for _, _, o in graph.triples((uri, ONTOLEX.language, None)):
            self.set_language(o)
        return self


class HasPattern(LemonBase, LemonElement):
    def __init__(self, uri: URIRef = None, MorphPattern: URIRef = None):
        self.set_uri(uri=uri)
        self.set_MorphPattern(MorphPattern)

    def set_MorphPattern(self, MorphPattern: URIRef = None):
        self._MorphPattern = MorphPattern

    @property
    def MorphPattern(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Muster"@de, "Patron"@fr, "Patroon"@nl, "Patrón"@es, "Pattern"@en ;
        return self._MorphPattern

    def triples(self):
        if self._MorphPattern is not None:
            yield (self.uri, ONTOLEX.MorphPattern, self._MorphPattern)

    def load(self, graph: Graph = None, uri: URIRef = None):
        for _, _, o in graph.triples((uri, ONTOLEX.MorphPattern, None)):
            self.set_MorphPattern(o)
        return self


# class LexicalCondition(LemonElement):
#     """
#     An evaluable condition on when a sense applies.
#     """
#     # rdfs:label "Condición léxica"@es, "Condition lexicale"@fr, "Lexical Condition"@en, "Lexikaal Voorwaarde"@nl, "Lexikonbedingung"@de ;
#     def __init__(
#        self,
#     ):
#         LemonElement.__init__(self)

# class LexicalContext(LemonElement):
#     """
#     Indicates the pragmatic or discourse context in which a sense applies.
#     """
#     # rdfs:label "Contexte lexical"@fr, "Contexto léxico"@es, "Lexical Context"@en, "Lexikaal Context"@nl, "Lexikonkontext"@de ;
#     def __init__(
#        self,
#     ):
#         LemonElement.__init__(self)


class LexicalEntry(HasLanguage, HasPattern, LemonBase, LemonElement):
    """
    An entry in the lexicon. This may be any morpheme, word, compound,
    phrase or clause that is included in the lexicon.

    :param abstractForm: A representation of a lexical entry that should not be considered canonical. This is primarily from a linguistic view for non-realisable forms such as stems but may also include misspellings and other unusual forms

    :param canonicalForm: The canonical ("dictionary") form of the lexical entry. This can be used to indicate the \"lemma\" form of a lexical entry

    :param lexicalForm: Denotes a written representation of a lexical entry

    :param otherForm: A non-preferred ("non-dictionary") representation of a lexical entry. This should be variant that is either a morphological variant, an abbreviation, short form or acronym

    :param lexicalVariant: Indicates a non-semantic relationship between two lexical entries. E.g., a term is derived from another term, such as \"lexical\" and \"lexicalize\"

    :param decomposition: Denotes a component of a lexical entry

    :param phraseRoot: Indicates the head node of a phrase structure or dependency parse graph

    :param sense: Indicates the sense of a lexical entry

    :param label: the rdfs:label of the lexical entry

    :param partOfSpeech: the partOfSpeech tag of the lexical entry

    :param termType: the tbx:termType of the lexical entry

    :param reliabilityCode: the tbx:reliabilityCode of the lexical entry

    """

    # rdfs:label "Entrada léxica"@es, "Entrée lexicale"@fr, "Lexical entry"@en, "Lexikaal item"@nl, "Lexikoneintrag"@de ;
    # rdfs:subClassOf :HasLanguage, :HasPattern, :LemonElement, [
    #     a owl:Restriction ;
    #     owl:minCardinality "1"^^xsd:nonNegativeInteger ;
    #     owl:onProperty :lexicalForm
    # ], [
    #     a owl:Restriction ;
    #     owl:maxCardinality "1"^^xsd:nonNegativeInteger ;
    #     owl:onProperty :canonicalForm
    # ] ;
    # owl:disjointWith :LexicalSense, :Lexicon, :Node, :PropertyValue, :SenseDefinition, :UsageExample .

    def __init__(
        self,
        uri: URIRef = None,
        language: str = None,
        pattern: URIRef = None,
        abstractForms: list[Form] = None,
        canonicalForm: Form = None,
        lexicalForms: list[Form] = None,
        otherForms: list[Form] = None,
        lexicalVariant: list[LexicalEntry] = None,
        constituents: list = None,
        decomposition: ComponentList = None,
        # phraseRoot: Node = None,
        senses: list[LexicalSense] = None,
        # synBehavior: Frame = None
        label: str = None,
        partOfSpeechs: list[str] = None,
        termType: str = None,
        reliabilityCode: int = None,
    ):
        self.set_uri(uri=uri)
        self.set_language(language=language)
        self.set_MorphPattern(MorphPattern=pattern)
        self.set_abstractForms(abstractForms)
        self.set_canonicalForm(canonicalForm)
        self.set_lexicalForms(lexicalForms)
        self.set_otherForms(otherForms)
        self.set_constituents(constituents)
        self.set_decomposition(decomposition)
        self.set_lexicalVariant(lexicalVariant)
        # self.set_phraseRoot(phraseRoot)
        self.set_senses(senses)
        # self.synBehavior(synBehavior)
        self.set_label(label)
        self.set_partOfSpeechs(partOfSpeechs)
        self.set_termType(termType)
        self.set_reliabilityCode(reliabilityCode)

    def string_rep(self, level: int = 0):
        indent = "   " * level
        s = f"(ontolex:LexicalEntry) uri = {self.uri.n3()}\n"
        if self.language is not None:
            s += indent + f"  language : {self.language}\n"
        if self.MorphPattern is not None:
            s += indent + f"  MorphPattern : {self.MorphPattern}\n"
        if self.abstractForms is not None:
            for line in self.abstractForms:
                s += indent + f"  abstractForm : {line.uri.n3()}\n"
        if self.canonicalForm is not None:
            s += indent + "  canonicalForm : "
            s += indent + self.canonicalForm.string_rep(level=1)
        if self.lexicalForms is not None:
            for line in self.lexicalForms:
                s += indent + "  lexicalForm : "
                s += indent + line.string_rep(level=1)
        if self.otherForms is not None:
            for line in self.otherForms:
                s += indent + "  otherForm : "
                s += indent + line.string_rep(level=1)
        if self.senses is not None:
            for line in self.senses:
                s += indent + f"  sense : "
                s += indent + line.string_rep(level=1)
        if self.constituents is not None:
            for line in self.constituents:
                s += indent + f"  constituent : "
                s += indent + line.string_rep(level=1)
        # incomplete
        if self.label is not None:
            s += indent + f"  label : {self.label}\n"
        if self.partOfSpeechs is not None and self.partOfSpeechs != []:
            p = ", ".join(self.partOfSpeechs)
            s += indent + f"  partOfSpeech : {p}\n"
        if self.termType is not None:
            s += indent + f"  termType : {self.termType}\n"
        if self.reliabilityCode is not None:
            s += indent + f"  reliabilityCode : {self.reliabilityCode}\n"
        return s

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.string_rep()

    def set_abstractForms(self, abstractForms: list[Form] = None):
        self._abstractForms = abstractForms

    def set_canonicalForm(self, canonicalForm: Form = None):
        self._canonicalForm = canonicalForm

    def set_constituents(self, constituents: list = None):
        self._constituents = constituents

    def set_decomposition(self, decomposition: ComponentList = None):
        self._decomposition = decomposition

    def set_lexicalForms(self, lexicalForms: list[Form] = None):
        self._lexicalForms = lexicalForms

    def set_lexicalVariant(self, lexicalVariant: list[LexicalEntry] = None):
        self._lexicalVariant = lexicalVariant

    def set_otherForms(self, otherForms: list[Form] = None):
        if otherForms != []:
            self._otherForms = otherForms

    def add_abstractForm(self, abstractForm: Form = None):
        if self._abstractForms is None:
            self._abstractForms = [abstractForm]
        else:
            self._abstractForms.append(abstractForm)

    def add_canonicalForm(self, canonicalForm: Form = None):
        self._canonicalForm = canonicalForm

    def add_lexicalForm(self, lexicalForm: Form = None):
        if self._lexicalForms is None:
            self._lexicalForms = [lexicalForm]
        else:
            self._lexicalForms.append(lexicalForm)

    def add_otherForm(self, otherForm: Form = None):
        if self._otherForms is None:
            self._otherForms = [otherForm]
        else:
            self._otherForms.append(otherForm)

    def add_lexicalVariant(self, lexicalVariant: LexicalEntry = None):
        if self._lexicalVariant is None:
            self._lexicalVariant = [lexicalVariant]
        else:
            self._lexicalVariant.append(lexicalVariant)

    # def set_phraseRoot(self, phraseRoot: Node = None):
    #     self._phraseRoot = phraseRoot

    def set_senses(self, senses: list[LexicalSense] = None):
        self._senses = senses

    def add_sense(self, sense: LexicalSense = None):
        if self._senses is None:
            self._senses = [sense]
        else:
            self._senses.append(sense)

    # def synBehavior(self, synBehavior: Frame = None):
    #     self._synBehavior = synBehavior

    def set_label(self, label: str = None):
        self._label = label

    def set_termType(self, termType: str = None):
        self._termType = termType

    def set_partOfSpeechs(self, partOfSpeechs: str = None):
        self._partOfSpeechs = partOfSpeechs

    def add_partOfSpeech(self, partOfSpeech: str = None):
        if self._partOfSpeechs is None:
            self._partOfSpeechs = [partOfSpeech]
        else:
            self._partOfSpeechs.append(partOfSpeech)

    def set_reliabilityCode(self, reliabilityCode: int = None):
        self._reliabilityCode = reliabilityCode

    @property
    def abstractForms(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Abstract form"@en, "Abstracte vorm"@nl, "Abstrakte Form"@de, "Forma abstracta"@es, "Forme abstraite"@fr ;
        # rdfs:subPropertyOf :lexicalForm .
        return self._abstractForms

    @property
    def canonicalForm(self):
        # a rdf:Property, owl:FunctionalProperty, owl:ObjectProperty ;
        # rdfs:label "Canonical form"@en, "Canonieke vorm"@nl, "Forma canónica"@es, "Forme canonique"@fr, "Kanonische Form"@de ;
        # rdfs:subPropertyOf :lexicalForm .
        return self._canonicalForm

    @property
    def constituents(self):
        return self._constituents

    @property
    def decomposition(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Decompositie"@nl, "Decomposition"@en, "Dekompositum"@de, "Descomposición"@es, "Décomposition"@fr ;
        return self._decomposition

    @property
    def lexicalForms(self):
        # a rdf:Property, owl:InverseFunctionalProperty, owl:ObjectProperty ;
        # rdfs:label "Forma léxica"@es, "Forme lexicale"@fr, "Lexical form"@en, "Lexikaal vorm"@nl, "Lexikalische Form"@de ;
        return self._lexicalForms

    @property
    def lexicalVariant(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Lexical variant"@en, "Lexikaal variant"@nl, "Lexikalische Variante"@de, "Variante lexicale"@fr, "Variante léxica"@es ;
        return self._lexicalVariant

    @property
    def otherForms(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Andere Form"@de, "Andere vorm"@nl, "Autre forme"@fr, "Other form"@en, "Otra forma"@es ;
        # rdfs:subPropertyOf :lexicalForm .
        return self._otherForms

    @property
    def phraseRoot(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Base de la syntagme"@fr, "Phrase root"@en, "Phrasewurzel"@de, "Raíz del sintagma"@es, "Zinsdeel wortel"@nl ;
        return self._phraseRoot

    @property
    def senses(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Acepción"@es, "Sense"@en, "Signification"@fr, "Sinn"@de, "Zin"@nl ;
        return self._senses

    @property
    def synBehavior(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Conduite syntaxique"@fr, "Funcionamiento sintáctico"@es, "Syntactic behavior"@en, "Syntactisch optreden"@nl, "Syntactische Verhalten"@de ;
        return self._synBehavior

    @property
    def label(self):
        return self._label

    @property
    def partOfSpeechs(self):
        return self._partOfSpeechs

    @property
    def termType(self):
        return self._termType

    @property
    def reliabilityCode(self):
        return self._reliabilityCode

    def triples(self):
        yield (self.uri, RDF.type, ONTOLEX.LexicalEntry)
        for triple in HasLanguage.triples(self):
            yield triple
        for triple in HasPattern.triples(self):
            yield triple
        if self.abstractForms is not None:
            for line in self.abstractForms:
                for triple in line.triples():
                    yield triple
        if self.canonicalForm is not None:
            for triple in self.canonicalForm.triples():
                yield triple
        if self.lexicalForms is not None:
            for line in self.lexicalForms:
                for triple in line.triples():
                    yield triple
        if self.otherForms is not None:
            for line in self.otherForms:
                for triple in line.triples():
                    yield triple
        if self.lexicalVariant is not None:
            for line in self.lexicalVariant:
                for triple in line.triples():
                    yield triple
        if self.constituents is not None:
            for constituent in self.constituents:
                for triple in constituent.triples():
                    yield triple
        if self.decomposition is not None:
            for triple in self.decomposition.triples():
                yield triple
        # if self.phraseRoot is not None:
        #     for triple in self.phraseRoot.triples()
        if self.senses is not None:
            for line in self.senses:
                for triple in line.triples():
                    yield triple
        # if self.synBehavior is not None:
        #     for triple in self.synBehavior.triples()
        if self.label is not None:
            yield (self.uri, RDFS.label, Literal(self.label, self.language))
        if self.partOfSpeechs is not None:
            for line in self.partOfSpeechs:
                yield (
                    self.uri,
                    LEXINFO.partOfSpeech,
                    line,
                )
        if self.termType is not None:
            yield (self.uri, TBX.termType, Literal(self.termType, self.language))
        if self.reliabilityCode is not None:
            yield (
                self.uri,
                TBX.reliabilityCode,
                Literal(self.reliabilityCode, datatype=XSD.nonNegativeInteger),
            )

    def load(self, graph: Graph = None, uri: URIRef = None):
        self.set_uri(uri)
        HasLanguage.load(self, graph, uri)
        HasPattern.load(self, graph, uri)
        forms = [
            Form().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.abstractForm, None))
        ]
        self.set_abstractForms(forms)
        forms = [
            Form().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.canonicalForm, None))
        ]
        if len(forms) > 1:
            logging.error(
                "More than one canonicalForms of LexicalEntry [" + str(uri) + "]"
            )
        else:
            for form in forms:
                self.set_canonicalForm(form)
        forms = [
            Form().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.lexicalForm, None))
        ]
        self.set_lexicalForms(forms)
        forms = [
            Form().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.otherForm, None))
        ]
        self.set_otherForms(forms)
        variants = [
            LexicalVariant().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.lexicalVariant, None))
        ]
        self.set_lexicalVariant(variants)
        constituents = [
            Component().load(graph, o)
            for _, _, o in graph.triples((uri, DECOMP.constituent, None))
        ]
        self.set_constituents(constituents)
        decompositions = [
            LexicalVariant().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.componentList, None))
        ]
        for decomposition in decompositions:
            self.set_decomposition(decomposition)
        senses = [
            LexicalSense().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.lexicalSense, None))
        ]
        self.set_senses(senses)
        for _, _, o in graph.triples((uri, RDFS.label, None)):
            self.set_label(o)
        self.set_partOfSpeechs(
            [o for _, _, o in graph.triples((uri, LEXINFO.partOfSpeech, None))]
        )
        for _, _, o in graph.triples((uri, TBX.termType, None)):
            self.set_termType(o)
        for _, _, o in graph.triples((uri, TBX.reliabilityCode, None)):
            self.set_reliabilityCode(o)
        return self


class LexicalSense(LemonBase, LemonElement):
    """
    Represents the intersection in meaning between the lexical entry and the ontology entity.
    This is used as the ontology entity and lexical entry may not be in one-to-one
    correspondence as such the existence of a sense between them states meerly that
    there are some cases when this lexical entry refer to the ontology entity and vica
    versa. Mapping elements can be used to further specify this relation.

    :param altRef: The sense of a non-preferred but admissible lexicalization of a given ontology entity
    :param broader: Denotes that one sense is broader than another. From a lexical point of view  this means replacing one lexical entry with another generalizes the meaning of the phrase. From an ontological point of view this property makes not strong assertions. From a mapping point of view if the broader sense applies the narrower sense must also
    :param narrower: Denotes that one sense is narrower than another. From a lexical point of view  this means replacing one lexical entry with another specializes the meaning of the phrase. From an ontological point of view this property makes not strong assertions. From a mapping point of view if the broader sense applies the narrower sense must also
    :param condition: Indicates an evaluable test, the is necessary for this sense to apply
    :param context: Denotes the pragmatic or discursive context of a sense mapping or a constraint on the mapping by syntactic or semantic properites
    :param definition: Indicates a natural language definition. Note there is a pseudo-node to allow for further description of the definition (e.g., source, creation date etc.). The value property should be used to indicate the string value of the definition.
    :param equivalent: Indicates that two senses are equivalent. From a lexical point of view , this indicates that the lexical entries can be substituted for each other with no change in meaning. From an ontological point of view it means that the two references are not disjoint. From a mapping point of view it means if one mapping apply the other must necessarily apply
    :param example
    :param incompatible: Says that the two senses are disjoint. From a lexical point of view, this means substituting the lexical entries must change the meaning of the phrase. From an ontological point of view, this property is implied if both references are also disjoint, but does not imply disjointness, but non-equivalence of the references. For the mapping point of view  there is not instance when both mappings are valid.
    :param isA: Denotes that the single argument of a class predicate is represented in the lexicon by the given semantic argument. That is Class(?x) or ?x rdf:type Class
    :param isReferenceOf: Indicate that a reference has a given sense
    :param isSenseOf: Indicate that a sense is realised by the given lexical entry
    :param objOfProp: Indicates the semantic argument which represents the objects (ranges) of the property referred to by this sense
    :param reference: A reference to an external resource
    :param propertyDomain: Indicates a restrictions on the domain of the property. That is, this sense only applies if the property the sense refers to has a subject in the class referred to by this property
    :param propertyRange: Indicates a restrictions on the range of the property. That is, this sense only applies if the property the sense refers to has a object in the class referred to by this property
    :param semArg: Denotes a semantic argument slot of a semantic unit
    :param senseRelation: Denotes a relationship between senses
    :param subsense: Indicates that the relation between a compound sense and its atomic subsenses
    :param subjOfProp: Indicates the semantic argument which represents the subjects (domain) of the property referred to by this sense

    """

    # rdfs:label "Acepción léxica"@es, "Lexical sense"@en, "Lexikaal zin"@nl, "Lexikonsinn"@de, "Signification lexicale"@fr ;
    # rdfs:subClassOf :LemonElement, [
    #     a rdfs:Class ;
    #     owl:unionOf ([
    #             a owl:Restriction ;
    #             owl:minCardinality "1"^^xsd:nonNegativeInteger ;
    #             owl:onProperty :subsense
    #         ]
    #         [
    #             a owl:Restriction ;
    #             owl:cardinality "1"^^xsd:nonNegativeInteger ;
    #             owl:onProperty :reference
    #         ]
    #     )
    # ] ;
    # owl:disjointWith :Lexicon, :Node, :PropertyValue, :SenseDefinition, :SynRoleMarker, :UsageExample .

    def __init__(
        self,
        uri: URIRef = None,
        altRef: LexicalSense = None,
        broader: LexicalSense = None,
        narrower: LexicalSense = None,
        # condition: LexicalCondition = None,
        # context: LexicalContext = None,
        # definition: SenseDefinition = None,
        equivalent: LexicalSense = None,
        # example: UsageExample = None,
        incompatible: LexicalSense = None,
        # isA: Argument = None,
        isReferenceOf: LexicalSense = None,
        isSenseOf: LexicalEntry = None,
        # objOfProp: Argument = None,
        # reference = None,
        # propertyDomain = None,
        # propertyRange = None,
        # semArg: Argument = None,
        senseRelation: LexicalSense = None,
        subsense: LexicalSense = None,
        # subjOfProp: Argument = None
    ):
        self.set_uri(uri=uri)
        self.set_altRef(altRef)
        self.set_broader(broader)
        self.set_narrower(narrower)
        # self.set_condition(condition)
        # self.set_context(context)
        # self.set_definition(definition)
        self.set_equivalent(equivalent)
        # self.set_example(example)
        self.set_incompatible(incompatible)
        # self.set_isA(isA)
        self.set_isReferenceOf(isReferenceOf)
        self.set_isSenseOf(isSenseOf)
        # self.set_objOfProp(objOfProp)
        # self.set_reference(reference)
        # self.set_propertyDomain(propertyDomain)
        # self.set_propertyRange(propertyRange)
        # self.set_semArg(semArg)
        self.set_senseRelation(senseRelation)
        self.set_subsense(subsense)
        # self.set_subjOfProp(subjOfProp)

    def string_rep(self, level: int = 0):
        indent = "   " * level
        s = f"(ontolex:LexicalSense) uri = {self.uri.n3()}\n"
        if self.altRef is not None:
            s += indent + f"  altRef : {self.altRef.uri.n3()}\n"
        if self.broader is not None:
            s += indent + f"  broader : {self.broader.uri.n3()}\n"
        if self.narrower is not None:
            s += indent + f"  narrower : {self.narrower.uri.n3()}\n"
        if self.equivalent is not None:
            s += indent + f"  equivalent : {self.equivalent.uri.n3()}\n"
        if self.incompatible is not None:
            s += indent + f"  incompatible : {self.incompatible.uri.n3()}\n"
        if self.isReferenceOf is not None:
            s += indent + f"  isReferenceOf : {self.isReferenceOf.uri.n3()}\n"
        if self.isSenseOf is not None:
            s += indent + f"  isSenseOf : {self.isSenseOf.uri.n3()}\n"
        if self.senseRelation is not None:
            s += indent + f"  senseRelation : {self.senseRelation.uri.n3()}\n"
        if self.subsense is not None:
            s += indent + f"  subsense : {self.subsense.uri.n3()}\n"
        return s

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.string_rep()

    def set_altRef(self, altRef: LexicalSense = None):
        self._altRef = altRef

    def set_broader(self, broader: LexicalSense = None):
        self._broader = broader

    def set_narrower(self, narrower: LexicalSense = None):
        self._narrower = narrower

    # def set_condition(self, condition: LexicalCondition = None):
    #     self._condition = condition

    # def set_context(self, context: LexicalContext = None):
    #     self._context = context

    # def set_definition(self, definition: SenseDefinition = None):
    #     self._definition = definition

    def set_equivalent(self, equivalent: LexicalSense = None):
        self._equivalent = equivalent

    # def set_example(self, example: UsageExample = None):
    #     self._example = example

    def set_incompatible(self, incompatible: LexicalSense = None):
        self._incompatible = incompatible

    # def set_isA(self, isA: Argument = None):
    #     self._isA = isA

    def set_isReferenceOf(self, isReferenceOf: LexicalSense = None):
        self._isReferenceOf = isReferenceOf

    def set_isSenseOf(self, isSenseOf: LexicalEntry = None):
        self._isSenseOf = isSenseOf

    # def set_objOfProp(self, objOfProp: Argument = None):
    #     self._objOfProp = objOfProp

    # def set_reference(self, reference = None):
    #     self._reference = reference

    # def set_propertyDomain(self, propertyDomain = None):
    #     self._propertyDomain = propertyDomain

    # def set_propertyRange(self, propertyRange = None):
    #     self._propertyRange = propertyRange

    # def set_semArg(self, semArg: Argument = None):
    #     self._semArg = semArg

    def set_senseRelation(self, senseRelation: LexicalSense = None):
        self._senseRelation = senseRelation

    def set_subsense(self, subsense: LexicalSense = None):
        self._subsense = subsense

    # def set_subjOfProp(self, subjOfProp: Argument = None):
    #     self._subjOfProp = subjOfProp

    @property
    def altRef(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Alternatieve referentie van"@nl, "Alternative Referenz von"@de, "Alternative reference of"@en, "Referencia alternativa de"@es, "Référence alternative de"@fr ;
        # rdfs:subPropertyOf :isReferenceOf .
        return self._altRef

    @property
    def broader(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Breder"@nl, "Breiter"@de, "Broader"@en, "Más amplio"@es, "Plus large"@fr ;
        # rdfs:subPropertyOf :senseRelation ;
        # owl:inverseOf :narrower .
        return self._broader

    @property
    def narrower(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Enger"@de, "Enger"@nl, "Más estrecho"@es, "Narrower"@en, "Plus restreint"@fr ;
        # rdfs:subPropertyOf :senseRelation .
        return self._narrower

    # @property
    # def condition(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Bedingung"@de, "Condición"@es, "Condition"@en, "Condition"@fr, "Voorwaarde"@nl ;
    #     return self._condition

    # @property
    # def context(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Context"@en, "Context"@nl, "Contexte"@fr, "Contexto"@es, "Kontext"@de ;
    #     return self._context

    # @property
    # def definition(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Definición"@es, "Definitie"@nl, "Definition"@de, "Definition"@en, "Définition"@fr ;
    #     return self._definition

    @property
    def equivalent(self):
        # a rdf:Property, owl:ObjectProperty, owl:SymmetricProperty, owl:TransitiveProperty ;
        # rdfs:label "Equivalent"@en, "Equivalent"@fr, "Equivalent"@nl, "Equivalente"@es, "Äquivalent"@de ;
        # rdfs:subPropertyOf :senseRelation .
        return self._equivalent

    # @property
    # def example(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Beispiel"@de, "Ejemplo"@es, "Example"@en, "Exemple"@fr, "Voorbeeld"@nl ;
    #     return self._example

    @property
    def incompatible(self):
        # a rdf:Property, owl:ObjectProperty, owl:SymmetricProperty ;
        # rdfs:label "Incompatible"@en, "Incompatible"@es, "Incompatible"@fr, "Inkompatibel"@de, "Onverenigbaar"@nl ;
        # rdfs:subPropertyOf :senseRelation .
        return self._incompatible

    # @property
    # def isA(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Instance de"@fr, "Instance of"@en, "Instancia de"@es, "Instantie van"@nl, "Instanz von"@de ;
    #     # rdfs:subPropertyOf :semArg .
    #     return self._isA

    @property
    def isReferenceOf(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Reference of"@en, "Referencia de"@es, "Referentie van"@nl, "Referenz von"@de, "Référence de"@fr ;
        # owl:inverseOf :reference .
        return self._isReferenceOf

    @property
    def isSenseOf(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Acepción de"@es, "Sense of"@en, "Signfication de"@fr, "Sinn von"@de, "Zin van"@nl ;
        # owl:inverseOf :sense .
        return self._isSenseOf

    # @property
    # def objOfProp(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Complemento de la propiedad"@es, "Complément de la propiété"@fr, "Object of property"@en, "Object van predikaat"@nl, "Objekt von Prädikat"@de ;
    #     # rdfs:subPropertyOf :semArg .
    #     return self._objOfProp

    # @property
    # def reference(self):
    #     # a rdf:Property, owl:FunctionalProperty, owl:ObjectProperty ;
    #     # rdfs:label "Reference"@en, "Referencia"@es, "Referentie"@nl, "Referenz"@de, "Référence"@fr .
    #     return self._reference

    # @property
    # def propertyDomain(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Domein van het predikaat"@nl, "Dominio de la propiedad"@es, "Ensemble de la propiété"@fr, "Property domain"@en, "Prädikatsbereich"@de ;
    #     # rdfs:subPropertyOf :condition .
    #     return self._propertyDomain

    # @property
    # def propertyRange(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Bereik van het predikaat"@nl, "Image de la propiété"@fr, "Property range"@en, "Prädikatszielmenge"@de, "Rango de la propiedad"@es ;
    #     # rdfs:subPropertyOf :condition .
    #     return self._propertyRange

    # @property
    # def semArg(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Actant sémantique"@fr, "Argumento semántico"@es, "Semantic argument"@en, "Semantisch argument"@nl, "Semantische Argument"@de ;
    #     return self._semArg

    @property
    def senseRelation(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Relación de Acepción"@es, "Relation de Signification"@fr, "Sense relation"@en, "Sinn-Relation"@de, "Zin relatie"@nl ;
        return self._senseRelation

    @property
    def subsense(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Deel van de zin"@nl, "Parte del acepción"@es, "Signification composante"@fr, "Subsense"@en, "Teil des Sinnes"@de ;
        return self._subsense

    # @property
    # def subjOfProp(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Onderwerp van predikaat"@nl, "Subject of property"@en, "Subjekt von Prädikat"@de, "Sujet de la propiété"@fr, "Sujeto de la propiedad"@es ;
    #     # rdfs:subPropertyOf :semArg .
    #     return self._subjOfProp

    def triples(self):
        yield (self.uri, ONTOLEX.sense, URIRef(self.uri + "#Sense"))
        if self.isSenseOf is not None:
            yield (
                URIRef(self.uri + "#Sense"),
                ONTOLEX.isSenseOf,
                URIRef(self.isSenseOf.uri),
            )
        if self.altRef is not None:
            yield (URIRef(self.uri + "#Sense"), ONTOLEX.altRef, URIRef(self.altRef.uri))
        if self.broader is not None:
            yield (
                URIRef(self.uri + "#Sense"),
                ONTOLEX.broader,
                URIRef(self.broader.uri),
            )
        if self.narrower is not None:
            yield (
                URIRef(self.uri + "#Sense"),
                ONTOLEX.narrower,
                URIRef(self.narrower.uri),
            )
        if self.equivalent is not None:
            yield (
                URIRef(self.uri + "#Sense"),
                ONTOLEX.equivalent,
                URIRef(self.equivalent.uri),
            )
        if self.incompatible is not None:
            yield (
                URIRef(self.uri + "#Sense"),
                ONTOLEX.incompatible,
                URIRef(self.incompatible.uri),
            )
        if self.isReferenceOf is not None:
            yield (
                URIRef(self.uri + "#Sense"),
                ONTOLEX.isReferenceOf,
                URIRef(self.isReferenceOf.uri),
            )
        if self.senseRelation is not None:
            yield (
                URIRef(self.uri + "#Sense"),
                ONTOLEX.senseRelation,
                URIRef(self.senseRelation.uri),
            )
        if self.subsense is not None:
            yield (
                URIRef(self.uri + "#Sense"),
                ONTOLEX.subsense,
                URIRef(self.subsense.uri),
            )

    def load(self, graph: Graph = None, uri: URIRef = None):
        self.set_uri(uri)
        isSenseOfs = [
            LexicalEntry().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.isSenseOf, None))
        ]
        for isSenseOf in isSenseOfs:
            self.set_isSenseOf(isSenseOf)
        altRefs = [
            LexicalSense().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.altRef, None))
        ]
        for altRef in altRefs:
            self.set_altRef(altRef)
        broaders = [
            LexicalSense().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.broader, None))
        ]
        for broader in broaders:
            self.set_broader(broaders)
        narrowers = [
            LexicalSense().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.narrower, None))
        ]
        for narrower in narrowers:
            self.set_narrower(narrower)
        equivalents = [
            LexicalSense().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.equivalent, None))
        ]
        for equivalent in equivalents:
            self.set_equivalent(equivalent)
        incompatibles = [
            LexicalSense().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.incompatible, None))
        ]
        for incompatible in incompatibles:
            self.set_incompatible(incompatible)
        isReferenceOfs = [
            LexicalSense().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.isReferenceOf, None))
        ]
        for isReferenceOf in isReferenceOfs:
            self.set_isReferenceOf(isReferenceOf)
        senseRelations = [
            LexicalSense().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.senseRelation, None))
        ]
        for senseRelation in senseRelations:
            self.set_senseRelation(senseRelation)
        subsenses = [
            LexicalSense().load(graph, o)
            for _, _, o in graph.triples((uri, ONTOLEX.subsense, None))
        ]
        for subsense in subsenses:
            self.set_subsense(subsense)


# class LexicalTopic(LemonElement):
#     """
#     Indicates the topic of a lexicon or a lexical entry.
#     """
#     # rdfs:label "Lexical Topic"@en, "Lexikaal Thema"@nl, "Lexikonthema"@de, "Tema léxica"@es, "Thème lexicale"@fr ;
#     def __init__(
#        self,
#     ):
#         LemonElement.__init__(self)


class Lexicon(HasLanguage, HasPattern, LemonBase, LemonElement):
    """
    The lexicon object. This object is specific to the given language and/or domain it describes.

    :param entry: Indicates an entry in a lexicon

    :param language: the language of the lexicon

    :param pattern:

    """

    # rdfs:label "Lexicon"@en, "Lexicon"@nl, "Lexicón"@es, "Lexikon"@de, "Lexique"@fr ;
    # rdfs:subClassOf :HasLanguage, :HasPattern, :LemonElement, [
    #     a owl:Restriction ;
    #     owl:minCardinality "1"^^xsd:nonNegativeInteger ;
    #     owl:onProperty :entry
    # ], [
    #     a owl:Restriction ;
    #     owl:cardinality "1"^^xsd:nonNegativeInteger ;
    #     owl:onProperty :language
    # ] ;
    # owl:disjointWith :Node, :PropertyValue, :SenseDefinition, :SynRoleMarker, :UsageExample .

    def __init__(
        self,
        uri: URIRef = None,
        entries: list = None,
        language: str = None,
        pattern: URIRef = None,
    ):
        self.set_uri(uri=uri)
        self.set_language(language=language)
        self.set_MorphPattern(MorphPattern=pattern)
        self.set_entries(entries)

    def string_rep(self, level: int = 0):
        indent = "   " * level
        s = f"(ontolex:Lexicon) uri = {self.uri.n3()}\n"
        if self.language is not None:
            s += indent + f"  language : {self.language}\n"
        if self.MorphPattern is not None:
            s += indent + f"  MorphPattern : {self.MorphPattern}\n"
        for entry in self.entries[0:10]:
            s += indent + f"  entry : {entry.uri.n3()}\n"
        if len(self.entries) >= 10:
            s += indent + "  entry : ...\n"
        return s

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.string_rep()

    def __getitem__(self, key):
        if not isinstance(key, URIRef):
            key = URIRef(key)
        return self._entries.get(key, None)

    def set_entries(self, entries: list = None):
        if entries is not None:
            self._entries = {entry.uri: entry for entry in entries}
        else:
            self._entries = {}

    @property
    def entries(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Eintrag"@de, "Entrada"@es, "Entry"@en, "Entrée"@fr, "Item"@nl ;
        return list(self._entries.values())

    def add_entry(self, entry: LexicalEntry = None):
        self._entries[entry.uri] = entry

    def triples(self):
        yield (self.uri, RDF.type, ONTOLEX.Lexicon)
        for triple in HasLanguage.triples(self):
            yield triple
        for triple in HasPattern.triples(self):
            yield triple
        if self.entries is not None:
            for entry in self.entries:
                yield (self.uri, ONTOLEX.entry, entry.uri)
                for triple in entry.triples():
                    yield triple

    def load(self, graph: Graph = None, uri: URIRef = None):
        self.set_uri(uri)
        self.set_entries(
            [
                LexicalEntry().load(graph, o)
                for _, _, o in graph.triples((uri, ONTOLEX.entry, None))
            ]
        )
        HasLanguage.load(self, graph, uri)
        HasPattern.load(self, graph, uri)
        return self


# class MorphPattern(LemonElement):
#     """
#     """
#     # rdfs:label "Morphological pattern"@en, "Morphologisch Patroon"@nl, "Morphologische Muster"@de, "Patron morphologique"@fr, "Patrón morfológico"@es ;
#     # rdfs:subClassOf :HasLanguage, :LemonElement .

#     def __init__(
#         self,
#         transform: MorphTransform = None,
#     ):
#         self.set_transform(transform)
#         LemonElement.__init__(self)

#     def set_transform(self, transform: MorphTransform = None):
#         self._transform = transform

#     @property
#     def transform(self):
#         # a rdf:Property, owl:ObjectProperty ;
#         # rdfs:label "Transform"@en, "Transformación"@es, "Transformatie"@nl, "Transformation"@de, "Transformation"@fr ;
#         return self._transform


# class MorphTransform(LemonElement):
#     """
#     """
#     # rdfs:label "Morphological Transform"@en, "Morphologisch transformatie"@nl, "Morphologische Transformation"@de, "Transformación morfológica"@es, "Transformation morphologique"@fr ;

#     def __init__(
#         self,
#         generates: Prototype = None,
#         nextTransform: MorphTransform = None,
#         rule: str = None
#     ):
#         self.set_generates(generates)
#         self.set_nextTransform(nextTransform)
#         self.set_rule(rule)
#         LemonElement.__init__(self)

#     def set_generates(self, generates: Prototype = None):
#         self._transform = transform

#     def set_nextTransform(self, nextTransform: MorphTransform = None):
#         self._nextTransform = nextTransform

#     def set_rule(self, rule: str = None):
#         self._rule = rule

#     @property
#     def generates(self):
#         # a rdf:Property, owl:ObjectProperty ;
#         # rdfs:label "Erzeugt"@de, "Genera"@es, "Generates"@en, "Genereert"@nl, "Génère"@fr ;
#         # rdfs:subClassOf [
#         #     a owl:Restriction ;
#         #     owl:minCardinality "1"^^xsd:nonNegativeInteger ;
#         #     owl:onProperty :rule
#         # ] .
#         return self._generates

#     @property
#     def nextTransform(self):
#         # a rdf:Property, owl:ObjectProperty ;
#         # rdfs:label "Folgende Transformation"@de, "Next transform"@en, "Transformación siguiente"@es, "Transformation suivante"@fr, "Volgende transformatie"@nl ;
#         return self._nextTransform

#     @property
#     def rule(self):
#         # a rdf:Property, owl:DatatypeProperty ;
#         # rdfs:label "Regel"@de, "Regel"@nl, "Regla"@es, "Rule"@en, "Règle"@fr ;
#         return self._rule


class NodeConstituent(LemonElement):
    """
    The class of constituents, that is types applied to nodes in a phrase structure graph.
    """

    # rdfs:label "Constituent"@en, "Constituent"@fr, "Constituent"@nl, "Constituyente"@es, "Konstituent"@de ;
    def __init__(self, uri: URIRef = None):
        self.set_uri(uri)


class Node(LemonElement):
    """
    A node in a phrase structure or dependency parse graph.

    :param edge: Denotes the relation between a node in a multi-word expression structure and an edge

    :param leaf: Denotes the component referred to by the lex (pre-terminal) of the phrase structure

    :param separator: Indicates the graphical element used to seperate the subnodes of this phrase structure. It is generally recommended that you use a string value with the language tag used to indicate script, (i.e., using ISO-15924 codes, such as \"Latn\"), as orthographic features may change with script.

    """

    # rdfs:label "Knoten"@de, "Node"@en, "Nœud"@fr, "Punt"@nl, "Vértice"@es ;
    # rdfs:subClassOf :LemonElement, [
    #     a rdfs:Class ;
    #     owl:unionOf ([
    #             a owl:Restriction ;
    #             owl:minCardinality "1"^^xsd:nonNegativeInteger ;
    #             owl:onProperty :edge
    #         ]
    #         [
    #             a owl:Restriction ;
    #             owl:minCardinality "1"^^xsd:nonNegativeInteger ;
    #             owl:onProperty :leaf
    #         ]
    #     )
    # ] ;
    # owl:disjointWith :PropertyValue, :SenseDefinition, :SynRoleMarker, :UsageExample .

    def __init__(
        self,
        uri: URIRef = None,
        constituent: NodeConstituent = None,
        # edge: Node = None,
        # leaf: str = None,
        # separator: str = None
    ):
        self.set_uri(uri)
        self.set_constituent(constituent)
        # self.set_edge(edge)
        # self.set_leaf(leaf)
        # self.set_separator(separator)

    def string_rep(self, level: int = 0):
        indent = "   " * level
        s = f"(ontolex:Node) uri = {self.uri.n3()}\n"
        if self.constituent is not None:
            s += indent + f"  constituent : {self.constituent.uri.n3()}\n"
        return s

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.string_rep()

    def set_constituent(self, constituent: NodeConstituent = None):
        self._constituent = constituent

    # def set_edge(self, edge: Node = None):
    #     self._edge = edge

    # def set_leaf(self, leaf: str = None):
    #     self._leaf = leaf

    # def set_separator(self, separator: str = None):
    #     self._separator = separator

    @property
    def constituent(self):
        # a rdf:Property, owl:ObjectProperty ;
        # rdfs:label "Constituent"@en, "Constituent"@nl, "Constitutif"@fr, "Constituyente"@es, "Konstituent"@de ;
        # rdfs:subPropertyOf owl:topObjectProperty .
        return self._constituent

    # @property
    # def edge(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Arista"@es, "Edge"@en, "Kante"@de, "Lien"@fr, "Lijn"@nl ;
    #     return self._edge

    # @property
    # def leaf(self):
    #     # a rdf:Property, owl:ObjectProperty ;
    #     # rdfs:label "Blad"@nl, "Blatt"@de, "Feuille"@fr, "Hoja"@es, "Leaf"@en ;
    #     return self._leaf

    # @property
    # def separator(self):
    #     # a rdf:Property, owl:DatatypeProperty ;
    #     # rdfs:label "Afscheider"@nl, "Separador"@es, "Separator"@de, "Separator"@en, "Séparateur"@fr ;
    #     return self._separator

    def triples(self):
        yield (self.uri, RDF.type, DECOMP.Constituent)

    def load(self, graph: Graph = None, uri: URIRef = None):
        self.set_uri(uri)
        return self


# class Part(LexicalEntry):
#     """
#     An affix is a morpheme that is attached to a word stem to form a new word.
#     Use this for lexical entries with only abstract forms.
#     """
#     # rdfs:label "Deel van een woord"@nl, "Part of word"@en, "Parte de la palabra"@es, "Partie du mot"@fr, "Wortteil"@de ;
#     def __init__(
#         self,
#     ):
#         LexicalEntry.__init__(self)


# class Phrase(LexicalEntry):
#     """
#     A phrase in lemon is defined in the looser sense of a sequence of words,
#     it does not have to a fully grammatical phrase.
#     """
#     # rdfs:label "Phrase"@de, "Phrase"@en, "Sintagma"@es, "Syntagme"@fr, "Zinsdeel"@nl ;
#     # rdfs:subClassOf :LexicalEntry, [
#     #     a owl:Restriction ;
#     #     owl:minCardinality "1"^^xsd:nonNegativeInteger ;
#     #     owl:onProperty :decomposition
#     # ] .
#     def __init__(
#         self,
#     ):
#         LexicalEntry.__init__(self)

# # class PropertyValue(LemonElement):
# #     """
# #     A value that can be used in the range of linguistic property.
# #     """
# #     # rdfs:label "Property Value"@en, "Prädikatswert"@de, "Valeur de la propriété"@fr, "Valor de la propiedad"@es, "Waarde van het predikaat"@nl ;
# #     # owl:disjointWith :SenseDefinition, :UsageExample .
# #     def __init__(
# #         self,
# #     ):
# #         LemonElement.__init__(self)

# class Prototype(LemonElement):
#     # rdfs:label "Prototipo"@es, "Prototyp"@nl, "Prototype"@en, "Prototype"@fr, "Prototype"@nl ;
#     def __init__(
#         self,
#     ):
#         LemonElement.__init__(self)

# class SenseCondition(LemonElement):
#     """
#     Indicates a logical condition that is used indicate when a particular term has the given meaning.
#     """
#     # rdfs:label "Bedingung"@de, "Condición"@es, "Condition"@en, "Condition"@fr, "Voorwaarde"@nl ;
#     def __init__(
#         self,
#     ):
#         LemonElement.__init__(self)

# class SenseContext(LemonElement):
#     """
#     Indicates the context in which a term is to be used.
#     The context refers not to the immediate syntactic context, but the document and
#     register the document is used in.
#     """
#     # rdfs:label "Context"@en, "Context"@nl, "Contexte"@fr, "Contexto"@es, "Kontext"@de ;
#     def __init__(
#         self,
#     ):
#         LemonElement.__init__(self)

# class SenseDefinition(LemonElement):
#     """
#     A definition of a sememe, that is the a text describing the exact meaning of the
#     lexical entry when its sense is the given ontology reference.
#     """
#     # rdfs:label "Definición"@es, "Definitie"@nl, "Definition"@de, "Definition"@en, "Définition"@fr ;
#     # rdfs:subClassOf :LemonElement, [
#     #     a owl:Restriction ;
#     #     owl:minCardinality "1"^^xsd:nonNegativeInteger ;
#     #     owl:onProperty :value
#     # ] ;
#     # owl:disjointWith :SynRoleMarker, :UsageExample .
#     def __init__(
#         self,
#     ):
#         LemonElement.__init__(self)

# class SynRoleMarker(LemonElement):
#     """
#     The indicator of a given syntactic argument, normally a preposition or other
#     particle marker or a linguistic property such as case.
#     """
#     # rdfs:label "Marcador de la función sintáctica"@es, "Marqueur du rôle syntaxique"@fr, "Syntactic role marker"@en, "Syntactisch rol merker"@nl, "Syntactische Rolle-Marker"@de ;
#     # rdfs:subClassOf :LemonElement, [
#     #     a rdfs:Class ;
#     #     owl:unionOf (:LexicalEntry
#     #         :PropertyValue
#     #     )
#     # ] ;
#     # owl:disjointWith :UsageExample .
#     def __init__(
#         self,
#     ):
#         LemonElement.__init__(self)

# class UsageExample(LemonElement):
#     """
#     An example of the usage of a lexical entry when refering to the ontology entity
#     given by the sememe's reference. This should in effect be an example of the form
#     used in context. E.g., \"this is a *usage example*\".
#     """
#     # rdfs:label "Anwendungsbeispiel"@de, "Ejemplo de uso"@es, "Exemple d'utilisation"@fr, "Usage Example"@en, "Voorbeeld van het gebruik"@nl ;
#     # rdfs:subClassOf :LemonElement, [
#     #     a owl:Restriction ;
#     #     owl:minCardinality "1"^^xsd:nonNegativeInteger ;
#     #     owl:onProperty :value
#     # ] .
#     def __init__(
#         self,
#     ):
#         LemonElement.__init__(self)

# class Word(LexicalEntry):
#     """
#     A word is a single unit of writing or speech. In languages written in Latin, Cyrillic,
#     Greek, Arabic scripts etc. these are assumed to be separated by white-space characters.
#     For Chinese, Japanese, Korean this should correspond to some agreed segmentation scheme.
#     """
#     # rdfs:label "Mot"@fr, "Palabra"@es, "Woord"@nl, "Word"@en, "Wort"@de ;
#     def __init__(
#         self,
#     ):
#         LexicalEntry.__init__(self)

# # not processed yet

# # :extrinsicArg
# #     a rdf:Property, owl:ObjectProperty ;
# #     rdfs:comment "A raisable semantic argument is not in fact the semantic argument of the current frame-sense but instead is \"raised\" into a frame-sense used for an argument. For example the phrase \"John seemed to be happy\", is interpreted as \"it seemed that X\" where X is \"John is happy\", hence the subject of \"seem\" is a raisable argument."@en ;
# #     rdfs:label "Actant extrinsèque"@fr, "Argumento extrínseco"@es, "Extrinsic argument"@en, "Extrinsiek argument"@nl, "Äußerliche Argument"@de ;
# #     rdfs:subPropertyOf :semArg .

# # :hiddenRef
# #     a rdf:Property, owl:ObjectProperty ;
# #     rdfs:comment "The sense of a non-admissible lexicalization for a ontology entity. This is used to denote incorrect or deprecated language that may be useful for information extraction but not generation"@en ;
# #     rdfs:label "Hidden reference of"@en, "Referencia oculta de"@es, "Référence cachée de"@fr, "Verborgen referentie van"@nl, "Verborgene Referenz von"@de ;
# #     rdfs:range :LexicalSense ;
# #     rdfs:subPropertyOf :isReferenceOf .

# # :prefRef
# #     a rdf:Property, owl:ObjectProperty ;
# #     rdfs:comment "The sense of the preferred lexicalization of a given ontology entity"@en ;
# #     rdfs:label "Bevorzugte Referenz von"@de, "Preferred reference of"@en, "Referencia preferida de"@es, "Référence préféré de"@fr, "Voorkeursreferentie van"@nl ;
# #     rdfs:range :LexicalSense ;
# #     rdfs:subPropertyOf :isReferenceOf .

# # :topic
# #     a rdf:Property, owl:ObjectProperty ;
# #     rdfs:comment "Indicates the topic of the overall lexicon, this is property is sometimes called \"subject field\". Note that in addition to the topic of a lexicon each lexical entry may belong to a given domain, this can be modelled as equal or not equal to the topic of the associated lexicon"@en ;
# #     rdfs:domain [
# #         a rdfs:Class ;
# #         owl:unionOf (:LexicalEntry
# #             :Lexicon
# #         )
# #     ] ;
# #     rdfs:label "Tema"@es, "Thema"@de, "Thema"@nl, "Thème"@fr, "Topic"@en ;
# #     rdfs:range :LexicalTopic .

# # :tree
# #     a rdf:Property, owl:ObjectProperty ;
# #     rdfs:label "Arbre"@fr, "Baum"@de, "Boom"@nl, "Tree"@en, "Árbol"@es .

# # :value
# #     a rdf:Property, owl:DatatypeProperty ;
# #     rdfs:comment "This indicates the value of a pseudo-data node. An example of this is definition where the value would generally be a string but it would not be possible to add further annotations, such as source or creation date."@en ;
# #     rdfs:label "Valeur"@fr, "Valor"@es, "Value"@en, "Waarde"@nl, "Wert"@de .
