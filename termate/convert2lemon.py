# -*- coding: utf-8 -*-

from rdflib import Graph, URIRef, Literal
from .vocab import *
from lxml import etree
import logging
import iribaker

from syntok.tokenizer import Tokenizer

from .const import NAMESPACES
from .const import XML_LANG
from .const import TBX_HEADER
from .const import TBX_RELAXNG
from .const import TBX_SCHEMA
from .const import TBX_DIALECT
from .const import TBX_STYLE
from .const import FILEDESC
from .const import SOURCEDESC
from .const import TITLESTMT
from .const import TITLE
from .const import PUBLICATIONSTMT
from .const import PUBLICATION
from .const import LANGSEC
from .const import TEXT
from .const import BODY
from .const import QName
from .const import upos2olia


class LemonBase(object):
    def __init__(self, uri: str = None):
        self._uri = uri

    @property
    def uri(self):
        if self._uri is not None:
            return URIRef(iribaker.to_iri(self._uri))
        else:
            return None

    def set_uri(self, uri: str = None):
        self._uri = uri


class LemonHeader(LemonBase):
    def __init__(
        self,
        dc_source: str = None,
        dct_type: str = "TBX-Basic",
        tbx_encodingdesc: str = '<p type="XCSURI">TBXXCS.xcs</p>',
        tbx_sourcedesc: str = None,
        uri: str = None,
    ):
        self.dc_source = dc_source
        self.dct_type = dct_type
        self.tbx_encodingdesc = tbx_encodingdesc
        self.tbx_sourcedesc = tbx_sourcedesc
        super().__init__(uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, TBX.Header)
            yield (self.uri, RDF.type, DCAT.Dataset)
            if self.dc_source is not None:
                yield (self.uri, DC.source, Literal(self.dc_source))
            if self.dct_type is not None:
                yield (self.uri, DCT.type, Literal(self.dct_type))
            if self.tbx_encodingdesc is not None:
                yield (self.uri, TBX.encodingDesc, Literal(self.tbx_encodingdesc))
            if self.tbx_sourcedesc is not None:
                yield (self.uri, TBX.sourceDesc, Literal(self.tbx_sourcedesc))


class LemonConcept(LemonBase):
    def __init__(
        self, 
        subjectField: str = None, 
        narrower: str = None,
        broader: str = None,
        related: list = None,
        xbrlType: str = None,
        prefLabel: list = None,
        altLabel: list = None,
        uri: str = None):
        self.subjectField = subjectField
        self.narrower = narrower
        self.broader = broader
        self.related = related
        self.xbrlType = xbrlType
        self.prefLabel = prefLabel
        self.altLabel = altLabel
        super().__init__(uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, SKOS.Concept)
            if self.subjectField is not None:
                yield (self.uri, TBX.subjectField, Literal(self.subjectField, datatype=XSD.string))
            if self.xbrlType is not None:
                yield (self.uri, TBX.xbrlType, Literal(self.xbrlType, datatype=XSD.string))
            if self.narrower is not None:
                yield (self.uri, SKOS.narrower, URIRef(self.narrower))
                yield (URIRef(self.narrower), SKOS.broader, self.uri)
            if self.broader is not None:
                yield (self.uri, SKOS.broader, URIRef(self.broader))
                yield (URIRef(self.broader), SKOS.narrower, self.uri)
            if self.prefLabel is not None:
                for prefLabel in self.prefLabel:
                    yield (self.uri, SKOS.prefLabel, Literal(prefLabel[0], lang=prefLabel[1]))
            if self.altLabel is not None:
                for altLabel in self.altLabel:
                    yield (self.uri, SKOS.altLabel, Literal(altLabel[0], lang=altLabel[1]))
            if self.related is not None:
                for rel in self.related:
                    yield (self.uri, SKOS.related, URIRef(rel))

class LemonLexicon(LemonBase):
    def __init__(self, language: str = None, uri: str = None):
        self.language = language
        super().__init__(uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, ONTOLEX.Lexicon)
            yield (self.uri, ONTOLEX.language, Literal(self.language))


class LemonLexicalEntry(LemonBase):
    def __init__(
        self,
        lexicon: LemonLexicon = None,
        reliabilityCode: int = None,
        termType: str = None,
        canonicalForm: str = None,
        otherForm: str = None,
        partOfSpeech: str = None,
        reference: str = None,
        uri: str = None,
    ):
        self.lexicon = lexicon
        self.reliabilityCode = reliabilityCode
        self.termType = termType
        self.canonicalForm = canonicalForm
        self.otherForm = otherForm
        self.partOfSpeech = partOfSpeech
        self.reference = reference
        super().__init__(uri)

    def triples(self):
        """
        Generates all the triples
        """

        if self.uri is not None:
            yield (self.lexicon.uri, ONTOLEX.entry, self.uri)
            yield (self.uri, RDF.type, ONTOLEX.LexicalEntry)

            tok = Tokenizer()
            if len(self.canonicalForm.split(" ")) > 1:
                yield (self.uri, RDF.type, ONTOLEX.MultiWordExpression)
            else:
                if self.partOfSpeech is not None:
                    if isinstance(self.partOfSpeech, URIRef):
                        yield (self.uri, LEXINFO.partOfSpeech, self.partOfSpeech)
                if self.termType is not None:
                    if self.termType == "abbreviation":
                        yield (self.uri, RDF.type, ONTOLEX.Acronym)
                    else:
                        yield (self.uri, RDF.type, ONTOLEX.Word)
                else:
                    yield (self.uri, RDF.type, ONTOLEX.Word)
            if self.reliabilityCode is not None:
                yield (self.uri, TBX.reliabilityCode, Literal(self.reliabilityCode, datatype=XSD.nonNegativeInteger))
            if self.termType is not None:
                yield (self.uri, TBX.termType, Literal(self.termType))
            yield (self.uri, ONTOLEX.language, Literal(self.lexicon.language))

            if self.canonicalForm is not None:
                yield (
                    self.uri,
                    ONTOLEX.canonicalForm,
                    URIRef(self.uri + "#canonicalForm"),
                )
                yield (URIRef(self.uri + "#canonicalForm"), RDF.type, ONTOLEX.Form)
                yield (
                    URIRef(self.uri + "#canonicalForm"),
                    ONTOLEX.writtenRep,
                    Literal(self.canonicalForm, lang=self.lexicon.language),
                )
                yield (
                    URIRef(self.uri + "#canonicalForm"),
                    RDFS.label,
                    Literal(self.canonicalForm, datatype=XSD.string),
                )
            if self.otherForm is not None and self.canonicalForm is not None:
                if self.otherForm != self.canonicalForm:
                    yield (
                        self.uri,
                        ONTOLEX.otherForm,
                        URIRef(self.uri + "#otherForm"),
                    )
                    yield (URIRef(self.uri + "#otherForm"), RDF.type, ONTOLEX.Form)
                    yield (
                        URIRef(self.uri + "#otherForm"),
                        ONTOLEX.writtenRep,
                        Literal(self.otherForm, lang=self.lexicon.language),
                    )
                    yield (
                        URIRef(self.uri + "#otherForm"),
                        RDFS.label,
                        Literal(self.otherForm, datatype=XSD.string),
                    )

            if self.reference is not None:
                yield (self.uri, ONTOLEX.sense, URIRef(self.uri + "#Sense"))
                yield (
                    URIRef(self.uri + "#Sense"),
                    ONTOLEX.reference,
                    URIRef(self.reference),
                )


# :Zust%C3%A4ndigkeit+der+Mitgliedstaaten-de#ComponentList decomp:identifies
#     :Zust%C3%A4ndigkeit+der+Mitgliedstaaten-de ;
#   decomp:constituent :component1, :component2, :component3 .

# :component1 decomp:correspondsTo :Zust%C3%A4ndigkeit-de .
# :component2 decomp:correspondsTo :der-de .
# :component3 decomp:correspondsTo :Mitgliedstaaten-de .

# :Zust%C3%A4ndigkeit-de
#   a                      ontolex:LexicalEntry ;
#   rdfs:label             "Zuständigkeit"@de ;
#   tbx:grammaticalNumber  tbx:singular ;
#   tbx:partOfSpeech       tbx:noun.

# :der-de
#   a                 ontolex:LexicalEntry ;
#   rdfs:label        "der"@en ;
#   tbx:partOfSpeech  tbx:other.

# :Mitgliedstaaten-de
#   a                 ontolex:LexicalEntry ;
#   rdfs:label        "Mitgliedstaat"@en ;
#   tbx:partOfSpeech  tbx:singular ;
#   tbx:grammaticalNumber tbx:plural


class LemonComponentList(LemonBase):
    def __init__(
        self,
        lexicalEntry: LemonLexicalEntry = None,
        components: list = None,
        uri: str = None,
    ):
        self.lexicalEntry = lexicalEntry
        self.components = list()
        super().__init__(uri)

    def triples(self):
        """
        Generates all the triples
        """
        # yield(self.uri, DECOMP.identifies, URIRef(self.lexicalEntry.uri))
        for component in self.components:
            yield (self.uri, DECOMP.constituent, component.uri)
            for triple in component.triples():
                yield triple


class LemonComponent(LemonBase):
    def __init__(
        self,
        term: str = None,
        language: str = None,
        lexicalEntry: LemonLexicalEntry = None,
        uri: str = None,
    ):
        self.term = term
        self.language = language
        self.lexicalEntry = lexicalEntry
        super().__init__(uri)

    def triples(self):
        """
        Generates all the triples
        """
        yield (self.uri, RDF.type, DECOMP.Component)
        yield (self.uri, DECOMP.correspondsTo, self.lexicalEntry.uri)
        for triple in self.lexicalEntry.triples():
            yield triple


class tbx2lemon(object):
    def __init__(self, uri: str = None, termbase: etree._ElementTree = None):
        self.graph = Graph()
        self.graph.bind("tbx", TBX)
        self.graph.bind("ontolex", ONTOLEX)
        self.graph.bind("lexinfo", LEXINFO)
        self.graph.bind("decomp", DECOMP)
        self.graph.bind("skos", SKOS)
        self.graph.bind("dc", DC)
        self.graph.bind("dcterms", DCT)

        tbx_sourcedesc = None
        for child in termbase.find(TBX_HEADER, namespaces=NAMESPACES):
            if child.tag == QName(name=FILEDESC):
                for child2 in child:
                    if child2.tag == QName(name=SOURCEDESC):
                        for child3 in child2:
                            if child3.tag == QName(name="p"):
                                tbx_sourcedesc = child3.text

        dct_type = termbase.getroot().attrib.get("type", "TBX-Basic")
        tbx_style = termbase.getroot().attrib.get("style", "dca")
        tbx_language = termbase.getroot().attrib.get(XML_LANG, "en")

        lemon_header = LemonHeader(
            uri=uri + "/header", dct_type=dct_type, tbx_sourcedesc=tbx_sourcedesc
        )

        languages = set()

        lemon_concepts = list()
        lemon_entries = list()
        lemon_lexicons = dict()
        for concept in termbase.findall(
            "text/body/conceptEntry", namespaces=NAMESPACES
        ):

            concept_id = concept.attrib["id"]

            subjectField = None
            broader = None
            narrower = None
            xbrlType = None
            prefLabel = list()
            altLabel = list()
            related = list()
            for element in concept:
                if (
                    element.tag == QName(name="descrip")
                    and element.attrib.get("type", "") == "subjectField"
                ):
                    subjectField = element.text
                if (
                    element.tag == QName(name="descrip")
                    and element.attrib.get("type", "") == "superordinateConceptGeneric"
                ):
                    narrower = element.attrib.get("target", None)
                if (
                    element.tag == QName(name="descrip")
                    and element.attrib.get("type", "") == "subordinateConceptGeneric"
                ):
                    broader = element.attrib.get("target", None)
                if (
                    element.tag == QName(name="descrip")
                    and element.attrib.get("type", "") == "xbrlType"
                ):
                    xbrlType = element.text
                if (
                    element.tag == QName(name="ref")
                    and element.attrib.get("type", "") == "crossReference"
                    and element.attrib.get("match", "") == "fullMatch"):
                    related.append(element.text)

                if element.tag == QName(name="langSec"):
                    lang = element.attrib.get(XML_LANG, None)
                    for termSecs in element:
                        term_text = None
                        term_type = None
                        for termSec in termSecs:
                            if termSec.tag == QName(name="term"):
                                term_text = termSec.text
                            elif (
                                termSec.tag == QName(name="termNote") 
                                and termSec.attrib.get("type", None) == "termType"):
                                term_type = termSec.text
                        if term_type == "fullForm":
                            prefLabel.append((term_text, lang))
                        elif term_type == "shortForm":
                            altLabel.append((term_text, lang))
                        elif term_type == "abbreviation":
                            altLabel.append((term_text, lang))

            lemon_concepts.append(
                LemonConcept(
                    uri=concept_id, 
                    subjectField=subjectField,
                    narrower=narrower,
                    broader=broader,
                    related=related,
                    xbrlType=xbrlType,
                    prefLabel=prefLabel,
                    altLabel=altLabel)
            )

            for langSec in concept:
                if langSec.tag == QName(name="langSec"):
                    lang = langSec.attrib.get(XML_LANG, None)

                    if lang not in lemon_lexicons.keys():
                        lemon_lexicons[lang] = LemonLexicon(
                            uri=uri + "/lexicon/" + lang, language=lang
                        )

                    for termSec in langSec:
                        term_text = None
                        term_lemma = None
                        termnote_type = None
                        lexicalEntry = LemonLexicalEntry(
                            lexicon=lemon_lexicons[lang]
                        )
                        lexicalEntry.reference = concept_id
                        for element in termSec:
                            if element.tag == QName(name="term"):
                                term_text = element.text
                            elif element.tag == QName(name="termNote"):
                                termnote_type = element.attrib.get("type", None)
                                if termnote_type == "termType":
                                    lexicalEntry.termType = element.text
                                elif termnote_type == "termLemma":
                                    term_lemma = element.text
                                elif termnote_type == "partOfSpeech":
                                    lexicalEntry.partOfSpeech = [upos2olia.get(el.upper(), "UNKNOWN") for el in element.text.split(", ")]
                                # administrativeStatus not yet done
                            elif element.tag == QName(name="descrip"):
                                descrip_type = element.attrib.get("type", None)
                                if descrip_type == "reliabilityCode":
                                    lexicalEntry.reliabilityCode = element.text
                                else:
                                    logging.warning(
                                        "descrip type not found: " + descrip_type
                                    )
                            else:
                                logging.warning(
                                    "termSec element not found: " + element.tag
                                )

                        tok = Tokenizer()
                        if lexicalEntry.termType == "abbreviation":
                            # if abbreviation then no lemma in tbx
                            tokens = [t.value for t in tok.tokenize(term_text)]
                            lemon_entry_uri = (
                                uri
                                +"/lexicon/"+lang+"/"
                                +"+".join(tokens)
                            )
                            lexicalEntry.set_uri(lemon_entry_uri)
                            lexicalEntry.canonicalForm = term_text
                        elif term_lemma is not None:
                            tokens = term_lemma.split(" ")
                            lemon_entry_uri = (
                                uri
                                +"/lexicon/"+lang+"/"
                                +"+".join(tokens)
                            )
                            lexicalEntry.set_uri(lemon_entry_uri)
                            lexicalEntry.canonicalForm = term_lemma
                            if term_lemma != term_text:
                                lexicalEntry.otherForm = term_text
                        else:
                            tokens = [t.value for t in tok.tokenize(term_text)]
                            lemon_entry_uri = (
                                uri
                                +"/lexicon/"+lang+"/"
                                +"+".join(tokens)
                            )
                            lexicalEntry.set_uri(lemon_entry_uri)
                            lexicalEntry.canonicalForm = term_text

                        lemon_entries.append(lexicalEntry)

                        components = lexicalEntry.canonicalForm.split(" ")
                        if len(components) > 1:
                            component_list = LemonComponentList(
                                # uri=lexicalEntry.uri+"#ComponentList",
                                uri=lexicalEntry.uri,
                                lexicalEntry=lexicalEntry,
                            )
                            for idx, component in enumerate(components):
                                component_lexicalEntry = LemonLexicalEntry(
                                    uri=uri+"/lexicon/"+lang+"/"+component,
                                    lexicon=lemon_lexicons[lang],
                                    canonicalForm=component,
                                    partOfSpeech=lexicalEntry.partOfSpeech[idx]
                                    if lexicalEntry.partOfSpeech is not None
                                    else None,
                                )
                                lemon_component = LemonComponent(
                                    uri=lexicalEntry.uri
                                    + "#component"
                                    + str(idx + 1),
                                    term=component,
                                    lexicalEntry=component_lexicalEntry,
                                )
                                component_list.components.append(lemon_component)
                            lemon_entries.append(component_list)
                # elif langSec.tag==QName(name="ref"):
                # elif langSec.tag==QName(name="descrip"):
                # else:
                #     logging.warning("conceptEntry element not found: " + langSec.tag)

        for triple in lemon_header.triples():
            self.graph.add(triple)

        for lexicon in lemon_lexicons.values():
            for triple in lexicon.triples():
                self.graph.add(triple)

        for concept in lemon_concepts:
            for triple in concept.triples():
                self.graph.add(triple)

        for entry in lemon_entries:
            for triple in entry.triples():
                self.graph.add(triple)

        # to do: abbreviations
