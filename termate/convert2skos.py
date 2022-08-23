# -*- coding: utf-8 -*-

"""Convert2skos module.

This module contains SKOS/RDF conversion functions for termate package

"""

import sys
import click
from io import StringIO, BytesIO

from .termate import TbxDocument
from lxml import etree
import rdflib
import logging
import os

XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"


@click.command()
@click.option(
    "--input", default="data/example.tbx", prompt="input file", help="The input file"
)
@click.option(
    "--prefix", default="_", prompt="triple prefix", help="the prefix of the triples"
)
@click.option(
    "--format",
    default="turtle",
    prompt="output format (turtle/xml/json-ld/ntriples/n3/trig)",
    help="The format of the output",
)
def convert2rdf_cli(input: str, prefix: str, format: str) -> None:
    """
    The Command Line Interface function to convert tbx-xml-file to tbx-rdf-file

    Args:
        input: the location of the tbx-xml-file
        prefix: the prefix to be used for the rdf-file
        format: turtle or xml

    Returns:
        None

    """
    doc = TbxDocument().open(input)

    graph = parse2graph(doc=doc, params={"handlerPrefix": prefix})

    if graph is not None:
        output, _ = os.path.splitext(input)
        if format == "turtle":
            extension = ".ttl"
        if format == "xml":
            extension = ".rdf.xml"
        fh = open(output + extension, "w", encoding="utf-8")
        fh.write(g.serialize(format=format))
        fh.close()

    return None


def QName(prefix: str = None, name: str = None):
    """ """
    if prefix is None:
        qname = etree.QName("{urn:iso:std:iso:30042:ed-2}" + name, name)
    else:
        qname = etree.QName("{" + namespaces[prefix] + "}" + name, name)
    return qname


def parse2graph(doc: TbxDocument, params: dict = {}) -> None:
    """
    Main function to convert TBX to RDF

    Args:
        doc: the naf document

    Returns:

    """
    create_params(doc, params)

    processTbx(doc, params)

    return generate_graph(params)


def create_params(doc: TbxDocument, params: dict = {}):
    """
    Function to set up the params dictionary

    Args:
        doc: NafDocument object
        params: dictionary of parameters

    Returns:
        None
    """
    params["namespaces"] = dict()
    params["provenanceNumber"] = 0
    params["depNumber"] = 0
    params["provenance"] = doc.header["fileDesc"]["sourceDesc"]["p"].replace(
        "\\", "\\\\"
    )

    addNamespace("dc", "http://purl.org/dc/elements/1.1/", params)
    addNamespace("xl", "http://www.xbrl.org/2003/XLink/", params)
    addNamespace("xsd", "http://www.w3.org/2001/XMLSchema/", params)
    addNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#", params)
    addNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema/", params)
    addNamespace("tbx", "urn:iso:std:iso:30042:ed-3", params)
    addNamespace("skos", "http://www.w3.org/2004/02/skos/core#", params)

    if params.get("handlerPrefix", "_") != "_":
        if params.get("handlerNamespace", None) is not None:
            addNamespace(
                params["handlerPrefix"],
                params["handlerNamespace"],
                params,
            )
        else:
            addNamespace(
                params["handlerPrefix"],
                "http://rdf.dnb.nl/termbases/" + params["handlerPrefix"] + "/",
                params,
            )

    params["out"] = StringIO()
    params["prefix"] = printNamespaces(params)
    params["doc"] = doc

    return None


def generate_graph(params: dict = {}):
    """
    Main function to generate the content of the rdf-xml conversion

    Args:
        params: dictionary of parameters

    Returns:
        rdflib.Graph object containing the converted NafDocument

    """
    file_content: StringIO = StringIO()
    file_content.write("# RDF triples (turtle syntax)\n\n")
    file_content.write("# TBX URI  '" + params["provenance"] + "'\n")
    file_content.write("\n")
    file_content.write(params["prefix"])
    file_content.write("\n\n")
    file_content.write(params["out"].getvalue().replace("\u2264", ""))

    content = file_content.getvalue()

    graph = rdflib.Graph()

    try:
        graph.parse(data=content, format="turtle")
    except:
        logging.error("Parsing error")
        with open("doc.log", "w", encoding="utf-8") as fh:
            fh.write(content)
        graph = None

    return graph


def isHttpUrl(url: str) -> bool:
    """
    Check is url is http url

    Args:
        url: url to be checked

    Returns:
        bool: True is url is http or https url

    """
    return isinstance(url, str) and (
        url.startswith("http://") or url.startswith("https://")
    )


def addNamespace(prefix: str = None, uri: str = None, params: dict = {}) -> int:
    """Add namespace to list of namespaces

    Args:
        prefix: prefix of the uri
        uri: complete uri of the prefix
        params: dict of params containing the namespaces

    Returns:
        int: 0 if success

    """
    namespaces = params["namespaces"]
    found = namespaces.get(uri, None)
    if found is not None:
        if prefix != found:
            return -1
        del namespaces[uri]
    namespaces[uri] = prefix
    return 0


def printNamespaces(params: dict = {}) -> str:
    """
    Get string of list of namespaces

    Args:
        params: dict of params containing the namespaces

    Returns:
        str: string of namespaces

    """
    namespaces = params["namespaces"]
    res: str = ""
    for uri in namespaces:
        res += "@prefix " + namespaces[uri] + ": <" + uri + ">.\n"
    return res


def processTbx(tbx: etree.Element, params: dict = {}) -> None:
    """
    Function to process elements of TBX file to RDF

    Args:
        tbx: etree.element
        params: dict of params to store results

    Returns:
        None

    """
    provenance = genProvenanceName(params)
    for child in params["doc"].getroot():
        child_name: str = etree.QName(child).localname
        if child_name == "tbxHeader":
            processHeader(child, params)
        if child_name == "text":
            processConceptEntry(child, params)
    return None


def attrib2pred(s: str) -> str:
    """Function to convert attribute to RDF predicate

    Args:
        s: the attribute

    Returns:
        str: the RDF predicate

    """
    return "has" + s[0].upper() + s[1:]


def processHeader(element: etree.Element, params: dict = {}) -> None:
    """Function to convert TBX header layer to RDF

    Args:
        element: element containing the header layer
        params: dict of params to store results

    Returns:
        None

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    output.write(prefix + ":tbxHeader ")

    for item in element:
        output.write("a tbx:header ;\n")
        if etree.QName(item.tag).localname == "fileDesc":
            output.write("    tbx:hasFileDesc [\n")
            for item2 in item:
                if etree.QName(item2).localname == "sourceDesc":
                    output.write("        tbx:hasSourceDesc [\n")
                    output.write(
                        "            tbx:hasText"
                        + ' """'
                        + item2[0].text.replace("\\", "\\\\")
                        + '"""^^rdf:XMLLiteral ;\n'
                    )
                    output.write("        ] ;\n")
            output.write("    ]")
        if item == element[-1]:
            output.write(" .\n")
        else:
            output.write(" ;\n")
    output.write("\n")
    return None


def processConceptEntry(element: etree.Element, params: dict = {}) -> None:
    """Function to convert conceptEntry entities layer to RDF

    Args:
        element: element

    Returns:
        None

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    for concept in element[0]:
        if concept.attrib.get("id", None)[0:4] == "http":
            concept_id = "<" + concept.attrib.get("id", None) + ">"
        else:
            concept_id = prefix + ":" + concept.attrib.get("id", None)
        output.write(concept_id + " ")
        for item in concept:
            if item.tag == QName(name="descrip"):
                if item.attrib.get("type", None) == "subjectField":
                    output.write('    skos:inScheme "' + item.text + '" ;\n')
                elif item.attrib.get("type", None) == "relatedConcept":
                    output.write("    skos:related <" + item.text + "> ;\n")
                elif item.attrib.get("type", None) == "subordinateConceptGeneric":
                    output.write("    skos:narrower <" + item.text + "> ;\n")
                elif item.attrib.get("type", None) == "superordinateConceptGeneric":
                    output.write("    skos:broader <" + item.text + "> ;\n")
            if item.tag == QName(name="langSec"):
                language = item.attrib[XML_LANG]
                for term_sec in item:
                    term_type = ""
                    term_frequency = ""
                    for element in term_sec:
                        if (
                            element.tag == QName(name="termNote")
                            and element.attrib.get("type", None) == "termType"
                        ):
                            term_type = element.text
                        if (
                            element.tag == QName(name="termNote")
                            and element.attrib.get("type", None) == "termFrequency"
                        ):
                            term_frequency = element.text
                    for element in term_sec:
                        if (
                            element.tag == QName(name="term")
                            and element.text is not None
                        ):
                            if term_type == "fullForm":
                                output.write(
                                    '    skos:prefLabel """'
                                    + element.text.replace("\\", "\\\\")
                                    + '"""@'
                                    + language.lower()
                                )
                            elif term_type == "abbreviation":
                                output.write(
                                    '    skos:literalForm """'
                                    + element.text.replace("\\", "\\\\")
                                    + '"""@'
                                    + language.lower()
                                )
                            else:
                                output.write(
                                    '    skos:literalForm """'
                                    + element.text.replace("\\", "\\\\")
                                    + '"""@'
                                    + language.lower()
                                )
                            output.write(" ;\n")
                        if element.tag == QName(name="termNote"):
                            output.write(
                                '    skos:note "['
                                + element.attrib.get("type", "")
                                + "]"
                                + element.text
                                + '"'
                            )
                            output.write(" ;\n")
        output.write("    a skos:Concept .\n")
        output.write("\n")
    return None


def genProvenanceName(params: dict) -> str:
    """Function to produce the provenance in RDF

    Args:
        element: element containing the header layer
        params: dict of params to store results

    Returns:
        str: name of provenance

    """
    output = params["out"]
    params["provenanceNumber"] += 1
    prefix = params.get("handlerPrefix", "_")
    name: str = prefix + ":provenance" + str(params["provenanceNumber"])
    output.write("# provenance for data from same tbx-file\n")
    output.write(name + " \n")
    output.write(
        '    xl:instance """'
        + params["provenance"].replace("\\", "\\\\")
        + '"""^^rdf:XMLLiteral .\n\n'
    )
    return name


def genDepName(params: dict) -> str:
    """Function to generate dependency name in RDF

    Args:
        params: dict of params to store results

    Returns:
        str: name of dependency

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    params["depNumber"] += 1
    name: str = prefix + ":dep" + str(params["depNumber"])
    output.write(name + " \n")
    return name


if __name__ == "__main__":
    sys.exit(convert2rdf())
