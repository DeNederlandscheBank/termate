# -*- coding: utf-8 -*-

from rdflib import Graph, URIRef, Literal
from .vocab import *
from lxml import etree
import logging

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

class LemonBase(object):

    def __init__(self, uri: str=None):
        self._uri = uri

    @property
    def uri(self):
        if self._uri is not None:
            return URIRef(clean_uri(self._uri))
        else:
            return None

    def set_uri(self, uri: str=None):
        self._uri = uri

class LemonHeader(LemonBase):

    def __init__(self,
                 dc_source: str = None, 
                 dct_type: str = "TBX-Basic",
                 tbx_encodingdesc: str = "<p type=\"XCSURI\">TBXXCS.xcs</p>",
                 tbx_sourcedesc: str = None,
                 uri: str=None):
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

    def __init__(self,
                 subjectField: str=None,
                 uri: str=None):
        self.subjectField = subjectField
        super().__init__(uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield(self.uri, RDF.type, SKOS.Concept)
            if self.subjectField is not None:
                yield(self.uri, TBX.subjectField, Literal(self.subjectField))

class LemonLexicon(LemonBase):

    def __init__(self,
                 language: str=None,
                 uri: str=None):
        self.language = language
        super().__init__(uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield(self.uri, RDF.type, ONTOLEX.Lexicon)
            yield(self.uri, ONTOLEX.language, Literal(self.language))


class LemonLexicalEntry(LemonBase):

    def __init__(self,
                 lexicon: LemonLexicon=None,
                 term: str=None,
                 reliabilityCode: int=None,
                 termType: str=None,
                 termLemma: str=None,
                 partOfSpeech: str=None,
                 reference: str=None,
                 uri: str=None):
        self.lexicon = lexicon
        self.reliabilityCode = reliabilityCode
        self.termType = termType
        self.termLemma = termLemma
        self.partOfSpeech = partOfSpeech
        self.term = term
        self.reference = reference
        super().__init__(uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield(self.lexicon.uri, ONTOLEX.entry, self.uri)
            yield(self.uri, RDF.type, ONTOLEX.LexicalEntry)

            if len(self.term.split(" "))>1:
                yield(self.uri, RDF.type, ONTOLEX.MultiWordExpression)
            else:
                if self.partOfSpeech is not None:
                    yield(self.uri, LEXINFO.partOfSpeech, Literal(self.partOfSpeech))
                if self.termType is not None:
                    if self.termType=="abbreviation":
                        yield(self.uri, RDF.type, ONTOLEX.Acronym)
                    else:
                        yield(self.uri, RDF.type, ONTOLEX.Word)
                else:
                    yield(self.uri, RDF.type, ONTOLEX.Word)
            if self.reliabilityCode is not None:
                yield(self.uri, TBX.reliabilityCode, Literal(self.reliabilityCode))
            if self.termType is not None:
                yield(self.uri, TBX.termType, Literal(self.termType))
            yield(self.uri, ONTOLEX.language, Literal(self.lexicon.language))

            # the canonical form for single words is the lemma of that word
            if self.termLemma is not None:
                yield(self.uri, ONTOLEX.canonicalForm, URIRef(self.uri+"#CanonicalForm"))
                yield(URIRef(self.uri+"#CanonicalForm"), RDF.type, ONTOLEX.Form)
                yield(URIRef(self.uri+"#CanonicalForm"), ONTOLEX.writtenRep, Literal(self.termLemma, lang=self.lexicon.language))

            if self.reference is not None:
                yield(self.uri, ONTOLEX.sense, URIRef(self.uri+"#Sense"))
                yield(URIRef(self.uri+"#Sense"), ONTOLEX.reference, URIRef(self.reference))

            yield(self.uri, RDFS.label, Literal(self.term, self.lexicon.language))

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

    def __init__(self,
                 lexicalEntry: LemonLexicalEntry=None,
                 components: list=None,
                 uri: str=None):
        self.lexicalEntry = lexicalEntry
        self.components = list()
        super().__init__(uri)


    def triples(self):
        """
        Generates all the triples
        """
        # yield(self.uri, DECOMP.identifies, URIRef(self.lexicalEntry.uri))
        for component in self.components:
            yield(self.uri, DECOMP.constituent, component.uri)
            for triple in component.triples():
                yield triple

class LemonComponent(LemonBase):
    def __init__(self,
                 term: str=None,
                 language: str=None,
                 lexicalEntry: LemonLexicalEntry=None,
                 uri: str=None):
        self.term = term
        self.language = language
        self.lexicalEntry = lexicalEntry
        super().__init__(uri)

    def triples(self):
        """
        Generates all the triples
        """
        yield(self.uri, RDF.type, DECOMP.Component)
        yield(self.uri, DECOMP.correspondsTo, self.lexicalEntry.uri)
        for triple in self.lexicalEntry.triples():
            yield triple

def clean_uri(uri: str=""):
    uri = uri.replace('`', '')
    uri = uri.replace('"', '')
    uri = uri.replace('<i>', '')
    uri = uri.replace('</i>', '')
    uri = uri.replace('<small>', '')
    uri = uri.replace('</small>', '')
    return uri

class tbx2lemon(object):

    def __init__(self,
                 uri: str=None,
                 termbase: etree._ElementTree=None):
        self.graph = Graph()
        self.graph.bind("tbx", TBX)
        self.graph.bind("ontolex", ONTOLEX)
        self.graph.bind("lexinfo", LEXINFO)
        self.graph.bind("decomp", DECOMP)

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

        lemon_header = LemonHeader(uri=uri,
                                   dct_type=dct_type,
                                   tbx_sourcedesc=tbx_sourcedesc)

        languages = set()

        lemon_concepts = list()
        lemon_entries = list()
        lemon_lexicons = dict()
        for concept in termbase.findall("text/body/conceptEntry", namespaces=NAMESPACES):

            concept_id = concept.attrib["id"]

            if "http" not in concept_id:

                subjectField = None
                for element in concept:
                    if element.tag==QName(name="descrip") and element.attrib.get("type", "")=="subjectField":
                        subjectField = element.text

                lemon_concepts.append(LemonConcept(uri=uri+"/"+concept_id,
                                                   subjectField=subjectField))

                for langSec in concept:
                    if langSec.tag==QName(name="langSec"):
                        lang = langSec.attrib.get(XML_LANG, None)

                        if lang not in lemon_lexicons.keys():
                            lemon_lexicons[lang] = LemonLexicon(uri=uri+"/lexicon/"+lang, language=lang)

                        for termSec in langSec:
                            lexicalEntry = LemonLexicalEntry(lexicon=lemon_lexicons[lang])
                            lexicalEntry.reference = uri+"/"+concept_id
                            for element in termSec:
                                if element.tag==QName(name="term"):
                                    lemon_entry_uri = uri+"/"+"+".join(element.text.split(" "))+"-"+lang
                                    lexicalEntry.set_uri(lemon_entry_uri)
                                    lexicalEntry.term = element.text
                                elif element.tag==QName(name="termNote"):
                                    termnote_type = element.attrib.get("type", None)
                                    if termnote_type=="termType":
                                        lexicalEntry.termType = element.text
                                    elif termnote_type=="termLemma":
                                        lexicalEntry.termLemma = element.text
                                    elif termnote_type=="partOfSpeech":
                                        lexicalEntry.partOfSpeech = element.text
                                    # administrativeStatus not yet done
                                elif element.tag==QName(name="descrip"):
                                    descrip_type = element.attrib.get("type", None)
                                    if descrip_type=="reliabilityCode":
                                        lexicalEntry.reliabilityCode = element.text
                                    else:
                                        logging.warning("descrip type not found: " + descrip_type)
                                else:
                                    logging.warning("termSec element not found: " + element.tag)

                            lemon_entries.append(lexicalEntry)

                            components = lexicalEntry.term.split(" ")
                            if len(components) > 1:
                                component_list = LemonComponentList(
                                    # uri=lexicalEntry.uri+"#ComponentList",
                                    uri=lexicalEntry.uri,
                                    lexicalEntry=lexicalEntry)
                                for idx, component in enumerate(components):
                                    component_lexicalEntry = LemonLexicalEntry(
                                        uri=uri+"/"+component+"-"+lang,
                                        lexicon=lemon_lexicons[lang],
                                        term=component,
                                        partOfSpeech=lexicalEntry.partOfSpeech.split(", ")[idx] if lexicalEntry.partOfSpeech is not None else None)
                                    lemon_component = LemonComponent(
                                        uri=lexicalEntry.uri+"#component"+str(idx+1),
                                        term=component,
                                        lexicalEntry=component_lexicalEntry)
                                    component_list.components.append(lemon_component)
                                lemon_entries.append(component_list)
                    # elif langSec.tag==QName(name="ref"):
                    # elif langSec.tag==QName(name="descrip"):
                    else:
                        logging.warning("conceptEntry element not found: " + langSec.tag)


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
