# -*- coding: utf-8 -*-

"""Convert2skos module.

This module contains conversion functions for the determinator package

"""

# conceptEntry <-> skos:Concept

# skos:broader -> tbx /superordinate*
# skos:narrower -> tbx /subordinate*
# skos:broaderTransitive -> tbx /broaderConcept*/
# skos:narrowerTransitive -> tbx /narrowerConcept*/
# skos:related -> tbx /relatedConcept


# skos:inScheme -> tbx /subjectfield

from lxml import etree
import rdflib

from .const import NAMESPACES
from .const import XML_LANG
from .const import RELAXNG_TBX_BASIC
from .const import SCHEMA_TBX_BASIC
from .const import TBX_HEADER
from .const import FILEDESC
from .const import SOURCEDESC
from .const import TEXT
from .const import BODY
from .const import TITLE
from .const import QName
from .determinator import TbxDocument

def get_concepts(g: rdflib.Graph = None):

	query = """
	SELECT DISTINCT ?c
	WHERE {
	    ?c a <http://www.w3.org/2004/02/skos/core#Concept> .
	}"""
	return list(g.query(query))

def retrieve_skos(g: rdflib.Graph = None, concept: str = "", item: str = ""):

    query = """
        SELECT DISTINCT ?b
        WHERE {
            """+concept+""" <http://www.w3.org/2004/02/skos/core#"""+item+"""> ?b .
    }"""
    qres = list(g.query(query))
    if len(qres) > 0:
        return qres
    else:
        return None

def create_tbx(t: TbxDocument = None, g: rdflib.Graph = None):

    concepts = get_concepts(g)

    for concept in concepts:

        concept_id = concept[0]

        body = t.find(TEXT + "/" + BODY, namespaces=NAMESPACES)

        concept_entry = etree.SubElement(
            body, QName(name="conceptEntry"), attrib={"id": concept_id.replace("http://data.jrc.ec.europa.eu/ontology/cybersecurity/", "frc:")}
        )

        inScheme = retrieve_skos(g, concept[0].n3(), "inScheme")
        if inScheme is not None:
            for item in inScheme:
                element = etree.SubElement(
                    concept_entry, QName(name="descrip"), attrib={"type": "subjectField"}
                )
                element.text = str(item[0]).replace("http://data.jrc.ec.europa.eu/ontology/cybersecurity/", "frc:")

        broader = retrieve_skos(g, concept[0].n3(), "broader")
        if broader is not None:
            for item in broader:
                element = etree.SubElement(
                    concept_entry, QName(name="descrip"), attrib={"type": "superordinateConceptGeneric"}
                )
                element.text = str(item[0]).replace("http://data.jrc.ec.europa.eu/ontology/cybersecurity/", "frc:")

        narrower = retrieve_skos(g, concept[0].n3(), "narrower")
        if narrower is not None:
            for item in narrower:
                element = etree.SubElement(
                    concept_entry, QName(name="descrip"), attrib={"type": "subordinateConceptGeneric"}
                )
                element.text = str(item[0]).replace("http://data.jrc.ec.europa.eu/ontology/cybersecurity/", "frc:")

        notation = retrieve_skos(g, concept[0].n3(), "notation")

        prefLabel = retrieve_skos(g, concept[0].n3(), "prefLabel")
        if prefLabel is not None:
            for item in prefLabel:
                lang_sec = etree.SubElement(
                    concept_entry,
                    QName(name="langSec"),
                    attrib={XML_LANG: item[0].language},
                )
                term_sec = etree.SubElement(
                    lang_sec,
                    QName(name="termSec"),
                    attrib={},
                )
                term = etree.SubElement(
                    term_sec,
                    QName(name="term"),
                    attrib={},
                )
                term.text = item[0].value
                term = etree.SubElement(
                    term_sec,
                    QName(name="termNote"),
                    attrib={},
                )
                term.text = "fullForm"

                altLabel = retrieve_skos(g, concept[0].n3(), "altLabel")
                if altLabel is not None:
                    for item2 in altLabel:
                        term_sec = etree.SubElement(
                            lang_sec,
                            QName(name="termSec"),
                            attrib={},
                        )
                        term = etree.SubElement(
                            term_sec,
                            QName(name="term"),
                            attrib={},
                        )
                        term.text = item2[0].value
                        term = etree.SubElement(
                            term_sec,
                            QName(name="termNote"),
                            attrib={},
                        )
                        if item2[0].upper() == item2[0]:
                            term.text = "abbreviation"
                        else:
                            term.text = "variant"

                