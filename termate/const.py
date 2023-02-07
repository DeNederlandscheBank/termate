# -*- coding: utf-8 -*-

"""
This module contains constants from termate

"""

from lxml import etree
from rdflib.term import URIRef


NAMESPACES = {
    None: "urn:iso:std:iso:30042:ed-2",
}
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
TBX_RELAXNG = "relaxng_tbx"
TBX_SCHEMA = "schema_tbx"
TBX_DIALECT = "dialect"
TBX_STYLE = "style"
TBX_HEADER = "tbxHeader"
FILEDESC = "fileDesc"
TITLESTMT = "titleStmt"
PUBLICATIONSTMT = "publicationStmt"
SOURCEDESC = "sourceDesc"
TEXT = "text"
BODY = "body"
TITLE = "title"
PUBLICATION = "publication"
LANGSEC = "langSec"

upos2olia = {
    "SYM": URIRef("http://purl.org/olia/olia.owl#Symbol"),
    "ADJ": URIRef("http://purl.org/olia/olia.owl#Adjective"),
    "X": URIRef("http://purl.org/olia/olia-top.owl#Word"),
    "ADV": URIRef("http://purl.org/olia/olia.owl#Adverb"),
    "PUNCT": URIRef("http://purl.org/olia/olia.owl#Punctuation"),
    "AUX": URIRef("http://purl.org/olia/olia.owl#AuxiliaryVerb"),
    "ADP": URIRef("http://purl.org/olia/olia.owl#Adposition"),
    "NUM": URIRef("http://purl.org/olia/olia.owl#Quantifier"),
    "PROPN": URIRef("http://purl.org/olia/olia.owl#ProperNoun"),
    "INTJ": URIRef("http://purl.org/olia/olia.owl#Interjection"),
    "CONJ": URIRef("http://purl.org/olia/olia.owl#CoordinatingConjunction"),
    # possibly an error in Stanza with CCONJ (does not exist in Olia):
    "CCONJ": URIRef("http://purl.org/olia/olia.owl#CoordinatingConjunction"),
    "DET": URIRef("http://purl.org/olia/olia.owl#Determiner"),
    "PART": URIRef("http://purl.org/olia/olia.owl#Particle"),
    "SCONJ": URIRef("http://purl.org/olia/olia.owl#SubordinatingConjunction"),
    "PRON": URIRef("http://purl.org/olia/olia.owl#Pronoun"),
    "NOUN": URIRef("http://purl.org/olia/olia.owl#CommonNoun"),
    "VERB": URIRef("http://purl.org/olia/olia.owl#Verb"),
}

def QName(prefix: str = None, name: str = None):
    """ """
    if prefix is None:
        qname = etree.QName("{urn:iso:std:iso:30042:ed-2}" + name, name)
    else:
        qname = etree.QName("{" + namespaces[prefix] + "}" + name, name)
    return qname
